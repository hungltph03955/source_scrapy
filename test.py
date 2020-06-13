import json
import re

with open('xxx.json') as f:
    data = json.load(f)

for i in data:
    print(i['content'])
