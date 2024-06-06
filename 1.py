#!/usr/bin/env python3

import sys
import requests
import time

def add_scheme_if_missing(url):
    if not url.startswith(('http://', 'https://')):
        return 'http://' + url
    return url

def check_http_server(url):
    try:
        start_time = time.time()
        response = requests.get(url)
        response_time = time.time() - start_time

        if response.status_code != 200:
            print("Critical: Server returned status code", response.status_code)
            return 2

        if response_time > 2.0:  # Response time threshold set to 2 seconds
            print("Warning: Response time is too high:", response_time)
            return 1

        print("OK: Server is up and running. Response time:", response_time)
        return 0

    except requests.exceptions.RequestException as e:
        print("Critical: Failed to reach the server:", e)
        return 2

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python 1.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    url = add_scheme_if_missing(url)
    exit_code = check_http_server(url)
    sys.exit(exit_code)
