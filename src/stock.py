from flask import Flask, request, abort
import yahoo_finance

app = Flask(__name__)

@app.route("/stock/health", methods=['GET'])
def health():
    return "OK"

@app.route("/stock/current/<stock_code>", methods=['GET'])
def current(stock_code):
    return str(yahoo_finance.get_latest_stock_price(stock_code))
