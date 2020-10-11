import os
import requests
import shutil # to save image locally

def write_style(file):
    a = '<meta content="width=device-width, initial-scale=1" name="viewport" />\n'
    a += '<meta name="theme-color" content="#4a4a4a" />\n'
    a += '<link rel="stylesheet" href="style.css">\n'
    file.write(a)

def write_header(file, sub, sort):
    a = '<h2><span class="sub">'+ sub + '</span> ' + sort + '</h2>'
    file.write(a)

def url_to_i_reddit_link(jpg):
    # print(jpg)
    return 'https://i.redd.it/' + jpg

def add_link_to_html_file(title, ups, html_file, path, alt):
    a = '<a href="' + alt + '" target="_blank"><span class="ups">' + str(ups) + ' upvotes</span>' + title + '</a>\n'
    a += '<img src="' + path + '" alt="' + alt + '">\n'
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

def write_only_file(name):
    pass

def write_if_not_exist_in_csv(name, title, ups, permalink, writer, titles):
    for row in titles:
        if title == name:
            return

    writer.writerow([name, title, ups, permalink])
