import re
import json
import requests
import os
import csv

from functions import url_to_i_reddit_link, add_link_to_html_file, down_image, write_if_not_exist_in_csv, write_style, write_header

subreddit = 'memes'
sorting = 'hot'
limit = '500'

print('Subreddit: r/' + subreddit + '\nSorting:', sorting + '\nLimit =', limit)

url = 'https://www.reddit.com/r/' + subreddit + '/' + sorting + '.json?limit=' + limit
print('url: ', url)
regexp = '/[0-z\.]{5,20}\.(?:jpg|png)' # like '/jh234lkj32.jpg' or .png

folder = subreddit + '-' + sorting
if not os.path.exists('web/' + folder):
	os.makedirs('web/' + folder)

user_agent = {'User-agent': 'Mozilla/5.0'}
memes = json.loads(requests.get(url, headers = user_agent).text)

# json['data']['children'][0]['data']['preview']['images'][0]['source']['url']

# ------------------------------------------

posts_file = open('web/' + folder + '.html', 'w', encoding='utf8', newline='\n')
write_style(posts_file)
write_header(posts_file, 'r/' + subreddit, sorting)

if not os.path.exists('csv'):
	os.makedirs('csv')

titles_w = open('csv/' + folder + '-titles.csv', 'a', newline='\n')
title_writer = csv.writer(titles_w, delimiter='|')

titles_r = open('csv/' + folder + '-titles.csv', 'r')

titles = []
for row in csv.reader(titles_r, delimiter='|'):
	try:
		titles.append(row[0])
	except Exception as e: pass

count = 0
for element in memes['data']['children']:
	title = element['data']['title']
	ups = element['data']['ups']

	try:
		url = element['data']['preview']['images'][0]['source']['url']
	except Exception as e: pass

	jpg = 'No image'
	jpg = re.search(regexp, url)
	if jpg == None:
		continue
	jpg = jpg[0].replace('/', '')

	write_if_not_exist_in_csv(jpg, title, title_writer, titles)

	link = url_to_i_reddit_link(jpg)
	down_image(link, 'web/' + folder, jpg)
	add_link_to_html_file(title, ups, posts_file, folder + '/' + jpg, link)
	count += 1
	print('Download\t' + str(count), end='\r')

print('Complete\t' + str(count))

# images = os.listdir(folder)

# for image in images:
	# add_link_to_html_file()
	# pass

posts_file.write('<span class="fix">'+ str(count) + ' posts</span>\n')
posts_file.close()
titles_w.close()
