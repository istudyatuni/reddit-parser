import json
import requests
from json_html import json_to_html

subreddit = 'memes'
sorting = 'hot'
limit = '500'

print('Subreddit: r/' + subreddit + '\nSorting:', sorting + '\nLimit =', limit)

url = 'https://www.reddit.com/r/' + subreddit + '/' + sorting + '.json?limit=' + limit
print('url: ', url)

user_agent = {'User-agent': 'Mozilla/5.0'}
responce = json.loads(requests.get(url, headers = user_agent).text)

# json['data']['children'][0]['data']['preview']['images'][0]['source']['url']

# ------------------------------------------

json_to_html(subreddit, sorting, responce)
