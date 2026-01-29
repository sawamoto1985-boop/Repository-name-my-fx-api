
from flask import Flask, jsonify
import requests

app = Flask(__name__)

# さっき取得したAPIキーをここに入れる
FINNHUB_API_KEY = "d5to79pr01qtjet0lh90d5to79pr01qtjet0lh9g"
@app.route('/calendar')
def get_calendar():
    try:
        # Finnhubの経済指標エンドポイント（米国などの主要指標）
        url = f"https://finnhub.io/api/v1/calendar/economic?token={FINNHUB_API_KEY}"
        response = requests.get(url)
        data = response.json()
        
        # 経済指標リスト（economicCalendar）を取り出す
        events = data.get('economicCalendar', [])
        
        # 直近10件だけを返すように整理
        return jsonify(events[:10])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
