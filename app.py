from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
import certifi

ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.xvik0of.mongodb.net/Cluster0?retryWrites=true&w=majority',
                     tlsCAFile=ca)
db = client.dbsparta

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

total = []

for num in range(1, 5):
    data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&ymd=20221026&hh=18&rtm=Y&pg=' + str(num),
                        headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    music = soup.select('#body-content > div.newest-list > div > table > tbody > tr')

    for i in music:
        title = i.select_one('td.info > a.title.ellipsis').text.strip()
        rank = i.select_one('td.number').text[0:3].strip()
        artist = i.select_one('td.info > a.artist.ellipsis').text.strip()
        if "19금" in title:
            title = title.replace("\n", "");
            title = title.replace("  ", "");

        total.append({'title': title, 'rank': rank, 'artist': artist})


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/chart')
def chart():
    return render_template('chart.html')


@app.route('/grade')
def grade():
    return render_template('grade.html')


@app.route("/music", methods=['GET'])
def music_post():
    return total


@app.route("/grade1", methods=['POST'])
def list_post():
    url_receive = request.form['url_give']
    star_receive = request.form['star_give']
    comment_receive = request.form['comment_give']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    m1title = soup.select_one('meta[property="og:title"]')['content'].strip('- geine')
    image = soup.select_one('meta[property="og:image"]')['content']

    doc = {
        'title': m1title,
        'image': image,
        'star': star_receive,
        'comment': comment_receive
    }
    db.music.insert_one(doc)
    return jsonify({'msg': '등록완료'})


@app.route('/grade1', methods=['GET'])
def list_get():
    music_list = list(db.music.find({},{'_id':False}))
    return jsonify({'music': music_list})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
