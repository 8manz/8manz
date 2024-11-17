import re
import sys
import pathlib
from collections import Counter

import requests

def language_stats(api_url: str, token: str, readme_path: str) -> None:
    headers = {
        'Authorization': f'token {token}'
    }

    request = requests.get(api_url, headers=headers, timeout=3)
    json = request.json()

    # languages to add that aren't auto-added
    # due to no repos using them
    # that you want to add
    whitelist_languages = [
            'Julia',
            'Haskell',
            'Zig',
            'Rust'
    ]

    blacklist_languages = [
            'Dockerfile'
    ]

    languages_found_in_repos: dict = Counter()
    for repo in json:
        lang = repo.get('language')
        if lang is not None and lang not in blacklist_languages:
            languages_found_in_repos[lang] += 1

    for lang in whitelist_languages:
        if lang not in languages_found_in_repos.keys():
            languages_found_in_repos[lang] = 0

    formatted_language_list : str = ''
    for index, (lang, count) in enumerate(languages_found_in_repos.items()):
        if index % 4 == 0:
            formatted_language_list += '\n'
        formatted_language_list += f'[{lang.lower()}: {count}]'

    update_content(formatted_language_list, readme_path)

def update_content(formatted_language_list: str, readme_path: str) -> None:
    updated_content = f'''
```python
 ___
( _ )_ __  __ _ _ _  ___
/ _ \ '  \/ _` | ' \|_ /
\___/_|_|_\__,_|_||_/__|

{formatted_language_list}
```

<img src="https://github.com/8manz/8manz/actions/workflows/main.yml/badge.svg" alt="ci"> <img src="assets/winter.gif" alt="winter">
'''

    with open (readme_path, 'r', encoding="utf-8") as readme:
        readme_content = readme.read()

    new_content = re.sub(r'(?<=<!\-\- start \-\->)[\s\S]*(?=<!\-\- end \-\->)', f'\n{updated_content}\n', readme_content)

    with open (readme_path, 'w', encoding="utf-8") as readme:
        readme.write(new_content)

if __name__ == '__main__':
    API_URL = 'https://api.github.com/user/repos'
    TOKEN = sys.argv[1]
    ROOT_PATH = pathlib.Path(__file__).parent.resolve()
    README_PATH = f'{ROOT_PATH}/README.md'
    language_stats(API_URL, TOKEN, README_PATH)
