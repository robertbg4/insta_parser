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
    html = '<div class="post">'.encode('utf16')
    html += geo_bin + image_bin + likes_bin + date_bin + text_bin
    html += '</div>'.encode('utf16')
    return html


def text_to_bin_html(text):
    html = '<span>' + text.replace('\n', '<br>') + '</span>'
    return html.encode('utf16')


def image_to_bin_html(image_url):
    print('gettting image', image_url)
    image = base64.b64encode(requests.get(image_url).content).decode('utf8')
    html = f'<img class="photo" src="data:image/jpg;base64, {image}">'
    return html.encode('utf16')


def likes_to_bin_html(likes):
    html = f"""
        <div class="likes">
            <img src="data:image/png;base64, iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAVlpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IlhNUCBDb3JlIDUuNC4wIj4KICAgPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICAgICAgPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIKICAgICAgICAgICAgeG1sbnM6dGlmZj0iaHR0cDovL25zLmFkb2JlLmNvbS90aWZmLzEuMC8iPgogICAgICAgICA8dGlmZjpPcmllbnRhdGlvbj4xPC90aWZmOk9yaWVudGF0aW9uPgogICAgICA8L3JkZjpEZXNjcmlwdGlvbj4KICAgPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KTMInWQAAAiZJREFUSA3FlU9IVEEcx+c3m0qY6E4s0U26RFeFCDwK7rrRRdpdkaBLFGTQpUToXqLgzUAhUIjI9yA2yPXZoVNXuxV0CLp1kH2WJYW079f399yXb13WfUNIc5j5/fl8f7/hze6MUsc8KF5/Kzt2VlPHPUXqilJ8DrltrO8U0RNTcVzALDwm8nOlq4qCGzAHEDJYPyniV0Ht91xm48UX4WT8bVDNFbPwVhHrDTPNUyXo+DXOO12cOknC5ZuRMPINOyid9pwN8cIG/mhxCLt6A78zRFpO/Ho/RSMtkf3EHjEPG899S1wodPo/6CPi/W1EtunP5hSf19XvauIYistm+qW2xgGO2W4tMY/aGodwMbHAEkTtQQ3NGUudDZ6RBjs2Ckv2pzR4bymywT/IGby0UdiwqF3W1LW3CFHVRpiQ9bU+saTT5fJXYrqTUJQYQ83JvrVn23IGynirzxXTfGJ1G5BYLYQ1wYUNhDeXLtzHn25Z7H8aqJHu4btRDZzDwcC9lPJ3aQG34a2DqIVFatF08yS5bi1SNTSQoNz11XzpIW7D6QhKsuKzPEp7zgMUDN+MSNPUIErgCp8COQO/JVNnGcC0WXdmI218PVLsjxZusqLHEKTiophdI8W3zbq7FIs1mEc2EBJP4zgTr8A8/BjhUaHr0a+loWrMadtAWD9XzOM7ODC769pdfPOi8ZxK3W+5JGog6q3LhUHN+qnYAQXXMmvuptj/ffwBu7eUeETPmVcAAAAASUVORK5CYII=">
            <span>{likes}</span>
        </div>"""
    return html.encode('utf16')


def date_to_bin_html(date: datetime):
    html = f'<div class="date"><span>{date.strftime("%m.%d.%Y")}</span></div>'
    return html.encode('utf16')


def geo_to_bin_html(geo):
    if not geo:
        return b''
    html = f"""
        <div class="geo">
            <img src="data:image/png;base64, iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAVlpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IlhNUCBDb3JlIDUuNC4wIj4KICAgPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICAgICAgPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIKICAgICAgICAgICAgeG1sbnM6dGlmZj0iaHR0cDovL25zLmFkb2JlLmNvbS90aWZmLzEuMC8iPgogICAgICAgICA8dGlmZjpPcmllbnRhdGlvbj4xPC90aWZmOk9yaWVudGF0aW9uPgogICAgICA8L3JkZjpEZXNjcmlwdGlvbj4KICAgPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KTMInWQAAArdJREFUSA2VVkuLE0EQ3snDgCF6iCJGPGQzk5DND/BoxMdBUHISjIK7B1HQi4gHzc0Vve5eXdlVcH3sVVw8eFCPogfBGPIwg4GNBGQvCR7My6+WnqG7pvPYgdBV9X1fVXdNd0+MmQmPaZrH/X7/leFweAzUo4LeMAzjc7/ff1ar1T6OS2GMAtPp9GEkWAVuIdkK7DewfxIf/qzP5zuPolfxqwUCgYVSqfSbMP5oC2DWc0iwCfJaMBh8VCwW/3Eh+ZlMZk+3270Lc2EwGJzFan7oeEoMyQ8mk8mGZVnzCjDGIS5pSMtpPh5Av5ew7JfVavUpx0b5xCUNVr3MOUoBag2Ip0F8wImTfKE5STlkrlIAs58HuFoul9syaRpbaNZEDleiFMDsTwB566KqYaDX+VQqdQlh7eaAflPkcJVKAUStUCj03UUlA4nz2J7rSPCcbAlyzV6vV4ZjugEYvMC+aDS66/Y4CW3b/gN7v+PTGJAd2NutVusIxl8sPoMev8DMd8Jkc5z8RCIRxbAtY7xAGQdmFgRPAcSGSLwui7mNQzkHfUmO8xZ9QI/PyITd2EhO2k+yhhfYwIvMZ7NZvjJZo7WF5jLADZmgFKhUKt8AbjWbzYsyaRpbaLZEDleiFBDR+xgLdJG5rAmG4BZAW+RUTwG8yHcg2bglb3PyKF9wbcyebmDl8RQgFAfmGoZb/F5RlMLB6U4TF1fEdR2uLVCv1xsg38MF9ioWi+3VCSlGGDbFa5gFfHB0W9tzkt1cWO4TiL9EIpEVBHV3jxEOhx8D+woucbSPdgUOs91u38S5SOBj8tCJOSPFMAGz0+nccGK6cWwBbL2/ODznIMyh13ecBMLOEUYcJ64bdUv38OLx+CF82N/jnewcIiS+gI1wCpdby0NmgakKkAYtOYCBtiH9Acih73RzTnz+A5nL/84LAG6sAAAAAElFTkSuQmCC">
            <span>{geo}</span>
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
    image_url = post['display_url']
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
                <style>
                    body {
                        font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
                        font-size:14px;
                        line-height:18px
                    }
                    span {
                        font-weight: 200;
                        vertical-align: 4px;
                    }
                    .post {
                        width: 640px;
                        padding: 0 20px 20px 20px;
                        margin: 0 0 40px 40px;
                    }
                    .geo {
                        margin-bottom: -16px;
                        font-size: 24px;
                    }
                    .photo {
                        margin-top: 20px;
                        width: 100%;
                    }
                    .likes {
                        font-size: 24px;
                        display: inline-block;
                        width: 50%;
                        height: 24px;
                    }
                    .date {
                        font-size: 24px;
                        text-align: right;
                        display: inline-block;
                        width: 49%;
                        height: 24px;
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
