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
    if msg in ['在嗎', 'Hi', 'hi', 'もしもし', 'おはよ', 'ohayo', '你好', '早安', '哈囉', '妳好', '午安', '晚安']:
        s = 'Hi 我在，我是 うた 的點餐機器人'
    elif msg in ['我想點餐', '我要點餐', '注文', '注文する', '點餐', '注文します']:
        s = '沒問題，想吃什麼?'
    elif msg in ['我愛你', 'i love u', 'I love you', 'love u', '好き', '大好き']:
        s = '我也愛你'
    else: 
        s = '好的' + msg + '一份'
        s += '有任何問題請聯絡 佐々木旬 !, \n電話番号: +886937209347, \nemail: linooohon@gmail.com, \n 回覆有誤的話，請見諒, 只是小小練習機器人, love you ❤️'
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=s))


if __name__ == "__main__":
    app.run()
