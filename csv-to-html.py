import re
import csv

from functions import write_style, add_link_to_html_file, url_to_i_reddit_link

subreddit = 'pikabu'
sorting = 'hot'

regexp = '/[0-z\.]{5,20}\.(?:jpg|png)'

csv_file = open('csv/' + subreddit + '-' + sorting + '-titles.csv', 'r')
html_file = open('web/' + subreddit + '-' + sorting + '.html', 'w')
write_style(html_file)

count = 0
title_reader = csv.reader(csv_file, delimiter='|')
folder = subreddit + '-' + sorting
for row in title_reader:
    file = row[0]
    title = row[1]
    ups = row[2]
    permalink = row[3]

    add_link_to_html_file(title, ups, html_file, folder + '/' + file, permalink)
    count += 1

html_file.write('<span class="fix">'+ str(count) + ' posts</span>\n')
