from flask import Flask, jsonify
from flask_cors import CORS
import requests
import xml.etree.ElementTree as ET
import urllib.parse
import re

app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False

def get_trending_keywords():
    """今、経済圏で話題の単語をGoogleトレンド的に抽出する"""
    try:
        # ビジネスニュースのトップRSSを取得
        trend_rss = "https://news.google.com/rss/sections/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNR3B6YldIU2FpSklieG9LQUFQAQ?hl=ja&gl=JP&ceid=JP:ja"
        resp = requests.get(trend_rss)
        root = ET.fromstring(resp.text)
        
        # タイトルからFXに関係しそうな2文字以上の単語を抽出
        titles = [item.find('title').text for item in root.findall('.//item')[:10]]
        full_text = " ".join(titles)
        
        # FXに影響を与えそうな重要キーワード（動的な抽出元）
        potential_words = ["金利", "介入", "急騰", "急落", "日銀", "FRB", "雇用", "物価", "円安", "円高"]
        found_keywords = [word for word in potential_words if word in full_text]
        
        return " OR ".join(found_keywords) if found_keywords else "為替"
    except:
        return "為替"

@app.route('/dynamic-fx-news')
def get_dynamic_news():
    try:
        # 1. 今、話題のキーワードを動的に取得
        dynamic_query = get_trending_keywords()
        
        # 2. ベースとなるFXワードと合体させる
        base_query = "ドル円 OR 為替"
        final_query = f"({base_query}) AND ({dynamic_query})"
        
        encoded_query = urllib.parse.quote(final_query)
        rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ja&gl=JP&ceid=JP:ja"
        
        response = requests.get(rss_url, timeout=10)
        root = ET.fromstring(response.text)
        
        news_list = []
        for item in root.findall('.//item')[:20]:
            news_list.append({
                "title": item.find('title').text,
                "url": item.find('link').text,
                "date": item.find('pubDate').text,
                "source": item.find('source').text if item.find('source') is not None else "経済速報"
            })
            
        return jsonify({
            "current_keywords": dynamic_query, # 今何のワードで探したかを表示
            "news": news_list
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
