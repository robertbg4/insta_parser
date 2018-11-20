import requests
import json
import base64
import sys
from datetime import datetime
from flask import Flask, request

app = Flask(__name__, static_folder='/home/ubuntu/server_host/')
app.config.from_object(__name__)

@app.route('/instagram/<nick>')
def index_1(nick):
    def get_posts(nick):
        r = requests.get(f'https://www.instagram.com/{nick}/')
        if r.status_code != 200:
            print(r.text)
        res = r.content.decode('utf-8').split('window._sharedData = ')[1].split(';</script>')[0]
        data = json.loads(res)
        page = data['entry_data']['ProfilePage']
        if not len(page):
            return
        posts = page[0]['graphql']['user']['edge_owner_to_timeline_media']['edges']
        return posts
    def get_post_info(post):
        post = post['node']
        image_url = post['display_url']
        print('gettting image', image_url)
        image = base64.b64encode(requests.get(image_url).content).decode('utf8')
        text_edges = post['edge_media_to_caption']['edges']
        date = str(datetime.fromtimestamp(post['taken_at_timestamp']))
        text = ''
        if text_edges:
            text = text_edges[0]['node']['text']
        encoded_text = None
        while encoded_text == None:
            try:
                print(datetime.now(), 'encoding', post['owner'], post['id'])
                encoded_text = text.encode('cp1251')
            except Exception as e:
                print(e)
                text = text.replace(text[e.start], '')
        likes = post['edge_media_preview_like']['count']
        post_html = f'<img src="data:image/jpg;base64, {image}"><br><p>'.encode('utf8')
        post_html += text.encode('utf8')
        post_html += f'</p><p>Likes: {likes}<br>Publication date: {date}</p><br><br>'.encode('utf8')
        return post_html

    html = '<!DOCTYPE html><html><body>'.encode('utf8')
    posts = get_posts(nick)
    if not posts:
        return 'Закрытый профиль:('
    for post in posts:
        html += get_post_info(post)
    html += '</body></html>'.encode('utf8')
    file = open(f'{nick}.html', 'w')
    file.write(html.decode('utf8'))
    file.close()
    print(request)
    return app.send_static_file(f'{nick}.html')

if __name__ == '__main__':
    #app.run(debug=True, host='172.26.9.28', port=8009)
    app.run(debug=False, port=5000)

