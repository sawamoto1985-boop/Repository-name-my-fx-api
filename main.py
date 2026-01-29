from flask import Flask, jsonify
from flask_cors import CORS
import requests
import xml.etree.ElementTree as ET

app = Flask(__name__)

# 重要：これでWebサイトからの直接アクセスを許可します
CORS(app)

# JSONの日本語化け（\u7c73）をサーバー側でも抑制する設定
app.config['JSON_AS_ASCII'] = False

@app.route('/')
def home():
    return "FX News API is Running!"

@app.route('/calendar')
def get_calendar():
    try:
        # Yahoo!ニュース（経済総合）のRSSを取得
        rss_url = "https://news.yahoo.co.jp/rss/categories/business.xml"
        response = requests.get(rss_url)
        response.encoding = 'utf-8'
        
        # XMLの解析
        root = ET.fromstring(response.text)
        news_list = []
        
        for item in root.findall('.//item'):
            title = item.find('title').text
            link = item.find('link').text
            pub_date = item.find('pubDate').text
            
            news_list.append({
                "title": title,
                "url": link,
                "date": pub_date
            })
            
        # 最新20件をJSONで返す
        return jsonify(news_list[:20])
        
    except Exception as e:
        # エラー発生時もJSON形式で返す
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Renderなどのホスティング環境で動かすための設定
    app.run(host='0.0.0.0', port=5000)
