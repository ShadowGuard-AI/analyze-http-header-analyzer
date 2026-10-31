![Banner](banner.png)

# analyze-http-header-analyzer
Analyzes HTTP headers fetched from a live URL, identifying potential security vulnerabilities or misconfigurations such as missing security headers or insecure cookies, and reports the server version string from the Server header. - Focused on Data analysis and reporting

## Install
`git clone https://github.com/ShadowGuardAI/analyze-http-header-analyzer`

## Usage
`./analyze-http-header-analyzer [params]`

## Parameters
- `-h`: Show help message and exit
- `--output`: No description provided
- `--user-agent`: Custom User-Agent string to use. Default: HTTPHeaderAnalyzer/1.0
- `--timeout`: Timeout for the HTTP request in seconds. Default: 10
- `--insecure`: No description provided

## License
Copyright (c) ShadowGuardAI
