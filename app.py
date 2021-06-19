from flask import Flask, request, abort

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

line_bot_api = LineBotApi('hTCawAYzf8KKR2oJPybcnq8GxmfpExob8PkHjh3TbTOufH5Q/CSyzBXmq79cZ2xNie+Ex+D3jVhtk3sRBLe0a+KuJHtGDlboz8apRr090Iy984+BmjXLzwPZ5cfAICX87ErxJGBnLb8Qcwv6g3afNwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('24fd6690d66019a1d083617f3f657a0d')


@app.route("/callback", methods=['POST'])
def callback():
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
    msg = event.message.text
    s = 'hi 我是聊天機器人'
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=s))


if __name__ == "__main__":
    app.run()
