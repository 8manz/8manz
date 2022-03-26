import re
import sys
import pathlib
import requests

def language_stats(url, token, readme_path):
  headers = {
      'Authorization': f'token {token}'
  }

  request = requests.get(url, headers=headers)
  json = request.json()

  python = 0
  bash = 0
  go = 0
  c = 0

  for language in json:
      lang_name = language['language']
      if lang_name == 'Python':
        python += 1
      elif lang_name == 'Go':
        go += 1
      elif lang_name == 'Shell':
        bash += 1
      elif lang_name == 'C':
        c += 1
      else:
        pass

  updated_content = f'''
```python
                  _____       | | |
_ _ _ _ ____ ____ |   | _  _  |_|_|           Python: {python}
| | | | [__  |___ |   | |\ |    |             Bash: {bash}
|_|_| | ___] |___ |___| | \|    |             Go: {go}
                                |             C: {c}

```
  '''

  with open (readme_path, 'r') as readme:
    readme_content = readme.read()

  new_content = re.sub(r'(?<=<!\-\- start \-\->)[\s\S]*(?=<!\-\- end \-\->)', f'\n{updated_content}\n', readme_content)

  with open (readme_path, 'w') as readme:
    readme.write(new_content)

if __name__ == '__main__':
  url = 'https://api.github.com/user/repos'
  token = sys.argv[1]
  root_path = pathlib.Path(__file__).parent.resolve()
  readme_path = f'{root_path}/README.md'
  language_stats(url, token, readme_path)


