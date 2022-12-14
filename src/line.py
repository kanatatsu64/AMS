from flask import Flask, request, abort
import json
import requests

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

with open('secret.json') as f:
    cred = json.load(f)["Line"]

line_bot_api = LineBotApi(cred["ChannelAccessToken"])
handler = WebhookHandler(cred["ChannelSecret"])

@app.route("/line/health", methods=['GET'])
def health():
    return 'OK'

@app.route("/line/webhook", methods=['POST'])
def webhook():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    r = requests.get('https://amscloud.biz/stock/current/' + text)
    price = r.text

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=price))
