from flask import Flask, jsonify
import investpy
import pandas as pd

app = Flask(__name__)

@app.route('/calendar')
def get_calendar():
    try:
        # 日本とアメリカの経済指標を取得
        df = investpy.economic_calendar(countries=['japan', 'united states'])
        return jsonify(df.to_dict(orient='records'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

