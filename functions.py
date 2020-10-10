import os
import requests
import shutil # to save image locally

style = '''<style>
    body {
        font-family: Noto Sans, Arial, sans-serif;
        background-color: #4a4a4a;
        color: white;
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

def write_style(file):
    file.write(style)

def url_to_i_reddit_link(jpg):
    # print(jpg)
    return 'https://i.redd.it/' + jpg

def add_link_to_html_file(title, ups, html_file, folder, file_name):
    a = '<p>' + title + '</p><p>' + str(ups) + ' upvotes</p>\n<img src="' + folder + '" alt="' + file_name + '">\n'
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

def write_if_not_exist_in_csv(name, title, writer, titles):
    for row in titles:
        if row == name:
            return

    writer.writerow([name, title])
