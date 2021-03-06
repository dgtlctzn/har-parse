import json
from pprint import pprint
from typing import Dict, List

from PyInquirer import prompt


def to_har(har_file: str) -> List[Dict]:
    with open(har_file, 'rt') as f:
        har_list = json.load(f)
    return har_list.get('log').get('entries')


def har_str(har: Dict) -> str:
    req = har.get('request')
    res = har.get('response')

    url = req.get('url')
    method = req.get('method')
    mime = res.get('content').get('mimeType')
    return f'{method} - {mime}: {url}'


def format_question(_type: str, message: str, name: str, choices=None) -> List[Dict]:
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


def format_to_python(raw: list, pretty=True, no_cookies=False) -> None:
    py_format = {}
    for entry in raw:
        py_format[entry['name']] = entry['value']
    if no_cookies:
        py_format.pop('Cookie', None)
        py_format.pop('cookie', None)
        py_format.pop('Set-Cookie', None)
    if pretty:
        pprint(py_format)
    else:
        print(py_format)


def main():
    try:
        har_file = prompt(format_question('input', 'What the is har file extension?', 'har_file'))
        if '.har' not in har_file.get('har_file'):
            raise ValueError('File must be a .har file')
        har_entries = to_har(har_file.get('har_file'))
        hars = [har for har in har_entries]
        har_choices = [har_str(har) for har in har_entries]
        ans = prompt(format_question('list', 'Which page?', 'har', choices=har_choices))
        chosen_har = hars[har_choices.index(ans.get('har'))]
        res_or_req = prompt(
            format_question(
                'list',
                'Request or response?',
                'res_or_req',
                choices=[{'name': 'response'}, {'name': 'request'}]
            )
        )
        info_choices = [{'name': 'headers'}, {'name': 'cookies'}]
        if res_or_req.get('res_or_req') == 'response':
            info_choices.append({'name': 'text'})
        else:
            info_choices.extend([{'name': 'query params'}, {'name': 'post data'}])
        info_choice = prompt(format_question('list', 'What do you want to get?', 'type', choices=info_choices))
        pprint_choice = prompt(format_question('confirm', 'Pretty print?', 'pretty'))


        if res_or_req.get('res_or_req') == 'request':
            if info_choice.get('type') == 'headers':
                exclude_cookies = prompt(format_question('confirm', 'Exclude Cookies?', 'exclude'))
                format_to_python(
                    chosen_har.get('request').get('headers'), 
                    pprint_choice.get('pretty'), 
                    no_cookies=exclude_cookies.get('exclude')
                )
            elif info_choice.get('type') == 'cookies':
                format_to_python(chosen_har.get('request').get('cookies'), pprint_choice.get('pretty'))
            elif info_choice.get('type') == 'query params':
                format_to_python(chosen_har.get('request').get('queryString'), pprint_choice.get('pretty'))
            elif info_choice.get('type') == 'post data':
                format_to_python(chosen_har.get('request').get('postData').get('params'), pprint_choice.get('pretty'))
        else:
            if info_choice.get('type') == 'headers':
                exclude_cookies = prompt(format_question('confirm', 'Exclude Cookies?', 'exclude'))
                format_to_python(
                    chosen_har.get('response').get('headers'), 
                    pprint_choice.get('pretty'), 
                    no_cookies=exclude_cookies.get('exclude')
                )
            elif info_choice.get('type') == 'cookies':
                format_to_python(chosen_har.get('response').get('cookies'), pprint_choice.get('pretty'))
            elif info_choice.get('type') == 'text':
                if pprint_choice.get('pretty'):
                    pprint(chosen_har.get('response').get('content').get('text'))
                else:
                    print(chosen_har.get('response').get('content').get('text'))
    except FileNotFoundError:
        raise Exception("File does not exist")
    except EOFError:
        print("Done")


if __name__ == '__main__':
    main()
