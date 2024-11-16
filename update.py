import re
import sys
import pathlib
from typing import NamedTuple
from collections import Counter

import requests

class LanguageNames(NamedTuple):
    lang_python: int
    lang_bash: int
    lang_go: int
    lang_c: int
    lang_cplusplus: int
    lang_julia: int
    lang_haskell: int
    lang_zig: int
    lang_rust: int

def language_stats(api_url, token, readme_path):
    headers = {
        'Authorization': f'token {token}'
    }

    request = requests.get(api_url, headers=headers, timeout=3)
    json = request.json()

    language_name_list = [
            'Python',
            'Go',
            'Shell',
            'C',
            'C++',
            'Julia',
            'Haskell',
            'Zig',
            'Rust'
    ]

    language_found_in_repos_list = Counter([language['language'] for language in json if language['language'] in language_name_list])

    names = LanguageNames(
            language_found_in_repos_list['Python'], language_found_in_repos_list['Shell'],
            language_found_in_repos_list['Go'], language_found_in_repos_list['C'],
            language_found_in_repos_list['C++'], language_found_in_repos_list['Julia'],
            language_found_in_repos_list['Haskell'], language_found_in_repos_list['Zig'],
            language_found_in_repos_list['Rust']
    )

    update_content(names, readme_path)

def update_content(names: LanguageNames, readme_path):
    updated_content = f'''
```python
 ___
( _ )_ __  __ _ _ _  ___
/ _ \ '  \/ _` | ' \|_ /
\___/_|_|_\__,_|_||_/__|

[python: {names.lang_python}][bash: {names.lang_bash}][golang: {names.lang_go}][c: {names.lang_c}]
[c++: {names.lang_cplusplus}][julia: {names.lang_julia}][haskell: {names.lang_haskell}][zig: {names.lang_zig}]
[rust: {names.lang_rust}]

<img src="assets/winter.gif" alt="winter">
```
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
