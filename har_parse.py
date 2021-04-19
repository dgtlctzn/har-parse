import json
import sys
from typing import List
from pprint import pprint

from haralyzer import HarParser
from PyInquirer import prompt


def to_har(har_file: str) -> HarParser.pages:
    with open(har_file, 'rt') as f:
        har_parser = HarParser(json.loads(f.read()))
    return har_parser.pages


def format_question(_type: str, message: str, name: str, choices=None) -> List[dict]:
    question = [
        {
            'type': _type,
            'message': message,
            'name': name,
        }
    ]
    if choices:
        question[0]['choices'] = choices
    return question


def clean_headers(raw_headers: list) -> dict:
    headers = {}
    for header in raw_headers:
        headers[header['name']] = header['value']
    return headers


def clean_cookies(raw_cookies: list) -> dict:
    cookies = {}
    for cookie in raw_cookies:
        cookies[cookie['name']] = cookie['value']
    return cookies


def main():
    try:
        har_file = prompt(format_question('input', 'What the is har file extension?', 'har_file'))
        if '.har' not in har_file.get('har_file'):
            raise ValueError('File must be a .har file')
        hars = [{'name': val} for val in to_har(har_file.get('har_file'))[0].entries]
        har_choices = [{'name': str(val)} for val in to_har(har_file.get('har_file'))[0].entries]
        ans = prompt(format_question('list', 'which request?', 'har', choices=har_choices))
        chosen_har = hars[har_choices.index({'name': ans.get('har')})]
        res_or_req = prompt(format_question('list', 'request or response?', 'res_or_req', choices=[{'name': 'response'}, {'name': 'request'}]))
        get = prompt(format_question('list', 'what do you want to get?', 'type', choices=[{'name': 'headers'}, {'name': 'cookies'}]))

        if res_or_req.get('res_or_req') == 'request':
            if get.get('type') == 'headers':
                pprint(clean_headers(chosen_har.get('name').request.headers))
            elif get.get('type') == 'cookies':
                pprint(clean_cookies(chosen_har.get('name').request.cookies))
        else:
            if get.get('type') == 'headers':
                pprint(clean_headers(chosen_har.get('name').response.headers))
            elif get.get('type') == 'cookies':
                pprint(clean_cookies(chosen_har.get('name').response.cookies))
    except FileNotFoundError as fe:
        raise Exception("File does not exist")


if __name__ == '__main__':
    main()
