import re
import json
from datetime import datetime as dt
import requests # to get image from the web
import shutil # to save it locally
import os

subreddit = 'pikabu'
sorting = 'hot'
limit = '50'

style = '''<style>
	body {
		font-family: Noto Sans, Arial, sans-serif;
	}
	img {
		width: 40em;
		margin: auto auto 2em 20%;
	}
	p {
		margin-left: 20%;
	}
	.fix {
		position: fixed;
		bottom: 1em;
		right: 5em;
	}
</style>\n'''

def url_to_i_reddit_link(jpg):
	# print(jpg)
	return 'https://i.redd.it/' + jpg

def add_link_to_html_file(title, html_file, folder, file_name):
	a = '<p>' + title + '</p>\n<img src="' + folder + '" alt="' + file_name + '">\n'
	html_file.write(a)

error_file = open('errors.txt', 'a')
user_agent = {'User-agent': 'Mozilla/5.0'}

def down_image(image_url, folder, filename):
	path = folder + '/' + filename
	if os.path.exists(path):
		return

	# set stream to True, this will return the stream content.
	r = requests.get(image_url, stream = True, headers = user_agent)


	# Check if the image was retrieved successfully
	if r.status_code == 200:
	    # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
	    r.raw.decode_content = True

	    # wb ( write binary )
	    with open(path,'wb') as f:
	        shutil.copyfileobj(r.raw, f)
	else:
		error_file.write('Image couldn\'t be retreived: ' + filename + '\n')


print('Subreddit: r/' + subreddit + '\nSorting:', sorting + '\nLimit =', limit)

url = 'https://www.reddit.com/r/' + subreddit + '/' + sorting + '.json?limit=' + limit
print('url: ', url)
regexp = '/[0-z\.]{5,20}\.(?:jpg|png)' # like '/jh234lkj32.jpg' or .png

folder = subreddit + '-' + sorting
if not os.path.exists(folder):
	os.makedirs(folder)

memes = json.loads(requests.get(url, headers = user_agent).text)

# json['data']['children'][0]['data']['preview']['images'][0]['source']['url']

# ------------------------------------------

memes_file = open(subreddit + '-' + sorting + '.html', 'w', encoding='utf8')
memes_file.write(style)

params = []
count = 0
for element in memes['data']['children']:
	title = element['data']['title']

	try:
		url = element['data']['preview']['images'][0]['source']['url']
	except Exception as e: pass

	jpg = re.search(regexp, url)
	if jpg == None:
		continue
	jpg = jpg[0].replace('/', '')

	param = { 'title': title, 'filename': jpg }
	params.append(param)

	link = url_to_i_reddit_link(jpg)
	down_image(link, folder, jpg)
	add_link_to_html_file(title, memes_file, folder + '/' + jpg, jpg)
	count += 1
	print('Download\t' + str(count), end='\r')

print('Complete\t' + str(count))

images = os.listdir(folder)

for image in images:
	# add_link_to_html_file()
	pass

memes_file.write('<span class="fix">'+ str(count) + ' posts</span>\n')
memes_file.close()
