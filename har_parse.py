import json
from pprint import pprint
from typing import Dict, List

from PyInquirer import prompt


def to_har(har_file: str) -> List[Dict]:
    with open(har_file, 'rt') as f:
        har_list = json.load(f)
    return har_list.get('log').get('entries')


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


def format_to_python(raw: list, pretty=True) -> None:
    py_format = {}
    for entry in raw:
        py_format[entry['name']] = entry['value']
    if pretty:
        pprint(py_format)
    else:
        print(py_format)


def main():
    try:
        har_file = prompt(format_question('input', 'What the is har file extension?', 'har_file'))
        if '.har' not in har_file.get('har_file'):
            raise ValueError('File must be a .har file')
        hars = [har for har in to_har(har_file.get('har_file'))]
        har_choices = [har.get('request').get('url') for har in to_har(har_file.get('har_file'))]
        ans = prompt(format_question('list', 'Which request?', 'har', choices=har_choices))
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
        info_choice = prompt(format_question('list', 'What do you want to get?', 'type', choices=info_choices))
        pprint_choice = prompt(format_question('confirm', 'Pretty print?', 'pretty'))

        if res_or_req.get('res_or_req') == 'request':
            if info_choice.get('type') == 'headers':
                format_to_python(chosen_har.get('request').get('headers'), pprint_choice.get('pretty'))
            elif info_choice.get('type') == 'cookies':
                format_to_python(chosen_har.get('request').get('cookies'), pprint_choice.get('pretty'))
        else:
            if info_choice.get('type') == 'headers':
                format_to_python(chosen_har.get('response').get('headers'), pprint_choice.get('pretty'))
            elif info_choice.get('type') == 'cookies':
                format_to_python(chosen_har.get('response').get('cookies'), pprint_choice.get('pretty'))
            elif info_choice.get('type') == 'text':
                if pprint_choice.get('pretty'):
                    pprint(chosen_har.get('response').get('content').get('text'))
                else:
                    print(chosen_har.get('response').get('content').get('text'))
    except FileNotFoundError:
        raise Exception("File does not exist")


if __name__ == '__main__':
    main()
