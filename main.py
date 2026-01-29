from flask import Flask, jsonify
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

FINNHUB_API_KEY = "d5to79pr01qtjet0lh90d5to79pr01qtjet0lh9g"

@app.route('/calendar')
def get_calendar():
    try:
        # 今日の日付から、前後1週間の範囲を設定
        today = datetime.now()
        start_date = (today - timedelta(days=7)).strftime('%Y-%m-%d')
        end_date = (today + timedelta(days=7)).strftime('%Y-%m-%d')

        # 日付範囲を指定してリクエスト
        url = f"https://finnhub.io/api/v1/calendar/economic?from={start_date}&to={end_date}&token={FINNHUB_API_KEY}"
        response = requests.get(url)
        data = response.json()
        
        events = data.get('economicCalendar', [])
        
        # もしそれでも空なら、テスト用のメッセージを返す
        if not events:
            return jsonify([{"event": "No events found for this week", "country": "N/A"}])
            
        return jsonify(events)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

