import re
import os
import csv
from functions import url_to_i_reddit_link, add_link_to_html_file, down_image, write_if_not_exist_in_csv, write_style, write_header

def delete_span_fix(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    with open(filename, 'w') as f:
        for line in lines:
            if re.search('class=\"fix\"', line) == None:
                f.write(line)

def json_to_html(subreddit, sorting, json_data, cont = False, count = 0):
    regexp = '/[0-z\.]{5,20}\.(?:jpg|png)' # like '/jh234lkj32.jpg' or .png
    folder = subreddit + '-' + sorting
    if not os.path.exists('web/' + folder):
        os.makedirs('web/' + folder)

    file = 'web/' + folder + '.html'
    if cont == True:
        delete_span_fix(file)
        posts_file = open(file, 'a', encoding='utf8', newline='\n')
    else:
        posts_file = open(file, 'w', encoding='utf8', newline='\n')
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
            titles.append(row[1])
        except Exception as e: pass

    for element in json_data['data']['children']:
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

        link = url_to_i_reddit_link(jpg)
        permalink = link
        permalink = 'https://reddit.com' + element['data']['permalink']

        write_if_not_exist_in_csv(jpg, title, ups, permalink, title_writer, titles)

        down_image(link, 'web/' + folder, jpg)
        add_link_to_html_file(title, ups, posts_file, folder + '/' + jpg, permalink)
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
    return count
