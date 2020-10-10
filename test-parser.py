from bs4 import BeautifulSoup as BS
from selenium import webdriver as wdriver
import re
from datetime import datetime as dt
# import logging as log

# log.basicConfig(level=log.DEBUG)

def to_i_reddit_link(jpg):
	return 'https://i.redd.it' + jpg

time_stamp_log = '\n----    ' + dt.now().strftime('%Y-%m-%d %H:%M:%S') + '    ----\n'
url = 'https://www.reddit.com/'
chromedriver_path = r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'

browser = wdriver.Chrome(executable_path=chromedriver_path)
browser.set_page_load_timeout(20)
browser.get(url)

html = browser.page_source
browser.quit()
html = BS(html, 'html.parser')

preview_file = open('previews.txt', 'a')
preview_file.write(time_stamp_log)

links = []

for el in html.select('img.ImageBox-image'):
	link = el.get('src')
	links.append(link)
	print(el)

previews = []

for link in links:
	preview = re.search('/[A-z0-9\.]{5,20}\.(?:jpg|png)', link)
	preview_file.write(preview[0] + '\n' if preview else 'Not found')
	if preview:
		previews.append(preview[0])

preview_file.close()
link_file = open('links.txt', 'a')
link_file.write(time_stamp_log)

for jpg in previews:
	print('jpg1: ', jpg)
	jpg = to_i_reddit_link(jpg)
	print('jpg2: ', jpg)
	link_file.write(jpg + '\n')

link_file.close()
