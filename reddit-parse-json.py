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

old_count = json_to_html(subreddit, sorting, responce)

while True:
	cont = input('Do you want to continue? y, n: ')
	if cont == 'y':
		new_url = url + '&after=' + responce['data']['after']
		responce = json.loads(requests.get(new_url, headers = user_agent).text)
		old_count = json_to_html(subreddit, sorting, responce, True, old_count)
	elif cont == 'n':
		print('Stopped')
		break
	else:
		print('Invalid. Stopped')
		break
