from flask import Flask, jsonify
import requests
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route('/')
def home():
    return "Japan Economic News API is Running!"

@app.route('/calendar')
def get_calendar():
    try:
        # Yahoo!ニュース（経済総合）のRSSを取得
        rss_url = "https://news.yahoo.co.jp/rss/categories/business.xml"
        response = requests.get(rss_url)
        response.encoding = 'utf-8'
        
        # XMLを解析
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
            
        # 最新の10件を返す
        return jsonify(news_list[:20])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

