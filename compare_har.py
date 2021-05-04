from typing import Dict
from pprint import pprint
from urllib.parse import urlunparse


def same(
    headers: Dict[str, str], 
    compare: Dict[str, str], 
    url_encoded: bool = False,
    remove_cookies: bool = False
    ) -> bool:
    if remove_cookies:
        headers = _remove_cookies(headers)
        compare = _remove_cookies(compare)
    return headers == compare


def difference(
    headers: Dict[str, str], 
    compare: Dict[str, str], 
    url_encoded: bool = False,
    remove_cookies: bool = False
    ) -> Dict[str, dict]:
    if remove_cookies:
        headers = _remove_cookies(headers)
        compare = _remove_cookies(compare)
    shared, headers_only, compare_only = {}, {}, {}
    for h1, val1 in headers.items():
        if h1 in compare:
            if compare.get(h1) == val1:
                shared[h1] = val1
            else:
                headers_only[h1] = val1
        else:
            headers_only[h1] = val1
    for h2, val2 in compare.items():
        if h2 not in headers:
            compare_only[h2] = val2
        else:
            if headers.get(h2) != val2:
                compare_only[h2] = val2 
    return {
        'shared': shared,
        'headers_only': headers_only,
        'compare_only': compare_only
    }


def _remove_cookies(headers: Dict[str, str]) -> Dict[str, str]:
    if 'cookie' in headers or 'Cookie' in headers:
        headers.pop('cookie', None)
        headers.pop('Cookie', None)
    return headers


def _url_parse(url_str: str) -> Dict[str, str]:
    pass


if __name__ == '__main__':
    headers1 = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '42',
        'Content-Type': 'application/json;charset=UTF-8',
        'Cookie': '_csrf=ZPQEwbEwm_j3Hl2xMwVg-06i',
        'Host': 'ciphr.dev',
        'Origin': 'https://ciphr.dev',
        'Referer': 'https://ciphr.dev/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 '
                    'Safari/537.36',
        'X-CSRF-Token': 'sQO7M0t7-bc40LNcWldIqQzGJ5ZHE80JT5YA',
        'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A '
                    'Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'guy': 'Joe'
    }

    headers2 = {
        'If-Modified-Since': 'Tue, 23 Feb 2021 20:08:00 GMT',
        'If-None-Match': 'W/"1e79-177d0817100"',
        'Referer': 'https://ciphr.dev/',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 '
                    'Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A '
                    'Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'guy': 'John'
    }

    # pprint(difference(headers1, headers2, remove_cookies=True))
    # print(same_headers(headers1, headers2, remove_cookies=True))