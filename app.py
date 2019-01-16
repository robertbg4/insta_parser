import requests
import json
import base64
import sys

from datetime import datetime
from flask import Flask, request
import werkzeug.exceptions as exc

app = Flask(__name__, static_folder='/home/ubuntu/server_host/html/')
app.config.from_object(__name__)


def create_post(image_url, text, likes, date, geo):
    geo_bin = geo_to_bin_html(geo)
    image_bin = image_to_bin_html(image_url)
    likes_bin = likes_to_bin_html(likes)
    date_bin = date_to_bin_html(date)
    text_bin = text_to_bin_html(text)
    html = '<div class="post">'.encode('utf16') + image_bin
    html += '<div class="text">'.encode('utf16')
    html += geo_bin + likes_bin + date_bin + text_bin
    html += '</div></div>'.encode('utf16')
    return html


def text_to_bin_html(text):
    html = text.replace('\n', '<br>')
    return html.encode('utf16')


def image_to_bin_html(image_url):
    html = f'<img class="photo" src="{image_url}">'
    return html.encode('utf16')


def likes_to_bin_html(likes):
    html = f"""
        <div class="likes">
            ❤️{likes}
        </div>"""
    return html.encode('utf16')


def date_to_bin_html(date: datetime):
    html = f'<div class="date">{date.strftime("%m.%d.%Y")}</div>'
    return html.encode('utf16')


def geo_to_bin_html(geo):
    if not geo:
        return b''
    html = f"""
        <div class="geo">
            📍{geo}
        </div>"""
    return html.encode('utf16')


def get_posts(nick):
    r = requests.get(f'https://www.instagram.com/{nick}/')
    if r.status_code != 200:
        print(r.text)
    sharedData = r.content.decode('utf-8').split('window._sharedData = ')
    if len(sharedData) < 2:
        raise exc.NotFound('Nickname not found')
    res = sharedData[1].split(';</script>')[0]
    data = json.loads(res)
    page = data['entry_data']['ProfilePage']
    if not len(page):
        raise exc.Forbidden('This account is private')
    user = page[0]['graphql']['user']
    media = user['edge_owner_to_timeline_media']
    after = media['page_info']['end_cursor']
    variables = {'id': user['id'], 'first': 12, 'after': after}
    query_hash = '50d3631032cf38ebe1a2d758524e3492'
    params = {'query_hash': query_hash, 'variables': variables}
    # q = requests.get('https://www.instagram.com/graphql/query/', params=params)
    posts = media['edges']
    return posts


def get_post_info(post):
    post = post['node']
    resourses = post['thumbnail_resources']
    image_url = resourses[len(resourses) - 1]['src']
    date = datetime.fromtimestamp(post['taken_at_timestamp'])
    text_edges = post['edge_media_to_caption']['edges']
    text = ''
    if text_edges:
        text = text_edges[0]['node']['text']
    likes = post['edge_media_preview_like']['count']
    location = post['location']
    geo = None
    if location:
        geo = location['name']
    post_html = create_post(image_url, text, likes, date, geo)
    return post_html


@app.route('/instagram/<nick>')
def index_1(nick):
    html = """
        <!DOCTYPE html>
        <html>
            <head>
                <meta charset="utf-16">
                <style type="text/css" media="all">
                    @page {
                        size: A4 portrait;
                    }
                    body {
                        font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
                        font-size:12pt;
                        font-weight: 200;
                    }
                    span {
                        font-weight: 200;
                        vertical-align: 4px;
                    }
                    .post {
                        height: 7.8cm;
                    }
                    .text {
                        width: calc(100% - 8.1cm);
                        margin-left: 2mm;
                        display: inline-block;
                        height: 100%;
                        overflow-y: hidden;
                        vertical-align: top;
                    }
                    .geo {
                        font-size: 1.3em;
                        height: 1.5em;
                        text-overflow: ellipsis;
                        white-space: nowrap;
                        overflow: hidden;
                        margin-top: -4mm;
                    }
                    .photo {
                        height: 100%;
                        display: inline-block;
                    }
                    .likes {
                        font-size: 1.3em;
                        display: inline-block;
                        width: 49%;
                    }
                    .date {
                        font-size: 1.3em;
                        text-align: right;
                        display: inline-block;
                        width: 49%;
                    }
                </style>
            </head>
            <body>""".encode('utf16')
    posts = get_posts(nick)
    if not posts:
        raise exc.Forbidden('This account is private')
    for post in posts:
        html += get_post_info(post)
    html += '</body></html>'.encode('utf16')
    file = open(f'html/{nick}.html', 'w')
    file.write(html.decode('utf-16'))
    file.close()
    print(request)
    return app.send_static_file(f'{nick}.html')

if __name__ == '__main__':
    app.run(debug=False, port=5000)
