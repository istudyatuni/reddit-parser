import re
import csv

from functions import write_style, add_link_to_html_file

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
    title = row[1]
    file = row[0]
    add_link_to_html_file(title, '-', html_file, folder + '/' + file, folder + '/' + file)
    count += 1

html_file.write('<span class="fix">'+ str(count) + ' posts</span>\n')
