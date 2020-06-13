import json
import re
def replace_fig(content):
    cont = re.match("<p><img(.+?)</p>", content)
    if cont is not None:
        a = f"<figure><img {cont.group(1)} </figure>"
        return a
        content.replace(cont.group(0), a)
with open('xxx.json') as f:
    data = json.load(f)

for i in data:
    content = i['content']
    cont = re.match("<p><img(.+?)</p>", content)
    if cont is not None:
        a = f"<figure><img {cont.group(1)} </figure>"
        i['content'] = content.replace(cont.group(0), a)

    print(i['content'])
