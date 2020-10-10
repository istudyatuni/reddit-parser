import json
import requests

url = 'https://www.reddit.com/r/memes/hot.json?limit=500'
user_agent = {'User-agent': 'Mozilla/5.0'}
memes = json.loads(requests.get(url, headers = user_agent).text)
file = open('some.json', 'w')
file.write(json.dumps(memes, indent=3))
