import re
import sys
import pathlib
import requests

def language_stats(api_url, token, readme_path):
    headers = {
        'Authorization': f'token {token}'
    }

    request = requests.get(api_url, headers=headers, timeout=3)
    json = request.json()

    lang_python = 0
    lang_bash = 0
    lang_go = 0
    lang_c = 0

    for language in json:
        lang_name = language['language']
        if lang_name == 'Python':
            lang_python += 1
        elif lang_name == 'Go':
            lang_go += 1
        elif lang_name == 'Shell':
            lang_bash += 1
        elif lang_name == 'C':
            lang_c += 1

    updated_content = f'''
```python
                  _____       | | |
_ _ _ _ ____ ____ |   | _  _  |_|_|           Python: {lang_python}
| | | | [__  |___ |   | |\ |    |             Bash: {lang_bash}
|_|_| | ___] |___ |___| | \|    |             Go: {lang_go}
                                |             C: {lang_c}

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
