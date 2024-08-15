from flask import Flask, render_template, jsonify
from datetime import datetime
import yfinance as yf
from google.cloud import firestore
from google.cloud import secretmanager
import pytz

app = Flask(__name__)
db = firestore.Client()


def get_btc_data():
    try:
        btc = yf.Ticker("BTC-USD")
        data = {
            'prevclose': btc.info['previousClose'],
            'open': btc.info['open'],
            'high': btc.info['dayHigh'],
            'low': btc.info['dayLow'],
            'volume': btc.info['volume']
        }
        # Store data in Firestore
        doc_ref = db.collection('btc_data').document(datetime.now(pytz.UTC).strftime("%Y-%m-%d %H:%M:%S"))
        doc_ref.set(data)
        return data
    except Exception as e:
        app.logger.error(f"Error fetching BTC data: {str(e)}")
        return None

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/get_btc_data", methods=['GET'])
def fetch_btc_data():
    btc_data = get_btc_data()
    if btc_data is None:
        return jsonify({"error": "Failed to fetch BTC data"}), 500
    
    utc_time = datetime.now(pytz.UTC)
    ist_time = utc_time.astimezone(pytz.timezone('Asia/Kolkata'))
    
    return jsonify({
        "timestamp": ist_time.strftime("%Y-%m-%d %H:%M:%S"),
        "btc_data": btc_data
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)

    