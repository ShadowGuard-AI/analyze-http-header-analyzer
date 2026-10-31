import argparse
import logging
import requests
import pandas as pd
import sys
from urllib.parse import urlparse

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_argparse():
    """
    Sets up the argument parser for the command-line interface.

    Returns:
        argparse.ArgumentParser: The configured argument parser.
    """
    parser = argparse.ArgumentParser(description='Analyze HTTP headers for security vulnerabilities and misconfigurations.')
    parser.add_argument('url', type=str, help='The URL to analyze.')
    parser.add_argument('--output', type=str, help='The output file to write results to (CSV). If not specified, prints to console.', required=False)
    parser.add_argument('--user-agent', type=str, default='HTTPHeaderAnalyzer/1.0', help='Custom User-Agent string to use. Default: HTTPHeaderAnalyzer/1.0')
    parser.add_argument('--timeout', type=int, default=10, help='Timeout for the HTTP request in seconds. Default: 10')
    parser.add_argument('--insecure', action='store_true', help='Disable SSL certificate verification (INSECURE!).')
    return parser

def validate_url(url):
    """
    Validates that the input URL is a valid and well-formed URL.

    Args:
        url (str): The URL to validate.

    Returns:
        bool: True if the URL is valid, False otherwise.
    """
    try:
        result = urlparse(url)
        # The scheme whitelist matters: urlparse alone also passes ftp or
        # file URLs, which the requests call below is not meant to fetch.
        return result.scheme in ("http", "https") and bool(result.netloc)
    except Exception:
        return False


def _get_header(headers, name):
    # analyze_headers returns dict(response.headers), and the plain dict
    # loses the case-insensitive lookup the requests object had. A server
    # answering with a lower case header name would otherwise be reported
    # as missing a header it did send.
    lowered = name.lower()
    for key, value in headers.items():
        if key.lower() == lowered:
            return value
    return None


def analyze_headers(url, user_agent='HTTPHeaderAnalyzer/1.0', timeout=10, insecure=False):
    """
    Analyzes the HTTP headers from a given URL.

    Args:
        url (str): The URL to analyze.
        user_agent (str): The User-Agent string to use for the request.
        timeout (int): Timeout for the HTTP request in seconds.
        insecure (bool): Disable SSL certificate verification.

    Returns:
        dict: A dictionary containing the header names and values.  Returns None on error.
    """
    try:
        headers = {'User-Agent': user_agent}
        logging.info(f"Sending request to {url} with User-Agent: {user_agent}, timeout: {timeout}, verify: {not insecure}")
        response = requests.get(url, headers=headers, timeout=timeout, verify=not insecure)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return dict(response.headers)
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return None

def assess_security_headers(headers):
    """
    Assesses the presence and configuration of common security headers.

    Args:
        headers (dict): A dictionary containing the HTTP headers.

    Returns:
        dict: A dictionary containing the assessment results for each security header.
    """
    assessment = {}

    # Strict-Transport-Security (HSTS)
    hsts = _get_header(headers, 'Strict-Transport-Security')
    if hsts:
        assessment['HSTS'] = 'Present'
        if 'max-age' not in hsts:
            assessment['HSTS_max_age'] = 'Missing max-age directive'
        else:
            assessment['HSTS_max_age'] = 'OK'

        if 'includeSubDomains' not in hsts:
            assessment['HSTS_includeSubDomains'] = 'Missing includeSubDomains directive'
        else:
            assessment['HSTS_includeSubDomains'] = 'OK'

        if 'preload' not in hsts:
            assessment['HSTS_preload'] = 'Missing preload directive'
        else:
            assessment['HSTS_preload'] = 'OK'
    else:
        assessment['HSTS'] = 'Missing'

    # Content-Security-Policy (CSP)
    csp = _get_header(headers, 'Content-Security-Policy')
    if csp:
        assessment['CSP'] = 'Present'
        if 'default-src' not in csp:
            assessment['CSP_default_src'] = 'Missing default-src directive. Potentially very insecure.'
        else:
            assessment['CSP_default_src'] = 'OK'
    else:
        assessment['CSP'] = 'Missing'

    # X-Frame-Options
    xfo = _get_header(headers, 'X-Frame-Options')
    if xfo:
        assessment['XFO'] = 'Present'
    else:
        assessment['XFO'] = 'Missing'

    # X-Content-Type-Options
    xcto = _get_header(headers, 'X-Content-Type-Options')
    if xcto:
        assessment['XCTO'] = 'Present'
        if xcto.lower() == 'nosniff':
            assessment['XCTO_nosniff'] = 'OK'
        else:
            assessment['XCTO_nosniff'] = 'Invalid value'
    else:
        assessment['XCTO'] = 'Missing'

    # Referrer-Policy
    rp = _get_header(headers, 'Referrer-Policy')
    if rp:
        assessment['Referrer-Policy'] = 'Present'
    else:
        assessment['Referrer-Policy'] = 'Missing'

    # Permissions-Policy (formerly Feature-Policy)
    pp = _get_header(headers, 'Permissions-Policy') or _get_header(headers, 'Feature-Policy')  # Check both
    if pp:
        assessment['Permissions-Policy'] = 'Present'
    else:
        assessment['Permissions-Policy'] = 'Missing'

    return assessment

def analyze_server_version(headers):
    """
    Reports the server version string from the Server header, if one was sent.

    Args:
        headers (dict): A dictionary containing the HTTP headers.

    Returns:
        str: A string describing the server version.
    """
    server = _get_header(headers, 'Server')
    if server:
        return f"Server: {server}"
    else:
        return "Server information not disclosed."

def analyze_cookies(headers):
    """
    Analyzes cookies for security flags like HttpOnly and Secure.

    Args:
        headers (dict): A dictionary containing the HTTP headers.

    Returns:
        list: A list of strings describing the cookie security status.
    """
    cookies = _get_header(headers, 'Set-Cookie')
    cookie_analysis = []

    if cookies:
        # Splitting a combined Set-Cookie value on ', ' is approximate: an
        # Expires date contains that same comma and space, so one cookie can
        # be read as two. The flag checks below still land on the right
        # pieces for the common shapes, but treat the split as a heuristic.
        for cookie in cookies.split(', '):  # Handle multiple cookies in one header
            cookie = cookie.strip()
            if 'HttpOnly' not in cookie:
                cookie_analysis.append(f"Cookie '{cookie.split(';')[0]}' missing HttpOnly flag")
            if 'Secure' not in cookie:
                cookie_analysis.append(f"Cookie '{cookie.split(';')[0]}' missing Secure flag")
    else:
        cookie_analysis.append("No cookies set")

    return cookie_analysis

def main():
    """
    Main function to orchestrate the HTTP header analysis.
    """
    parser = setup_argparse()
    args = parser.parse_args()

    if not validate_url(args.url):
        logging.error("Invalid URL provided.")
        print("Error: Invalid URL provided.")
        sys.exit(1)

    headers = analyze_headers(args.url, args.user_agent, args.timeout, args.insecure)

    if headers is None:
        print("Failed to retrieve headers.")
        sys.exit(1)

    security_assessment = assess_security_headers(headers)
    server_info = analyze_server_version(headers)
    cookie_info = analyze_cookies(headers)

    data = {
        'Header': list(headers.keys()) + ['Server Analysis', 'Cookie Analysis'] + list(security_assessment.keys()),
        'Value': list(headers.values()) + [server_info] + [', '.join(cookie_info)] + list(security_assessment.values())
    }

    df = pd.DataFrame(data)

    if args.output:
        try:
            df.to_csv(args.output, index=False)
            logging.info(f"Results saved to {args.output}")
            print(f"Results saved to {args.output}")
        except Exception as e:
            logging.error(f"Error writing to file: {e}")
            print(f"Error writing to file: {e}")
            sys.exit(1)
    else:
        print(df.to_string())

if __name__ == "__main__":
    main()
