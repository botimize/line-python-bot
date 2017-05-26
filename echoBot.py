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

from botimize import Botimize

app = Flask(__name__)

line_bot_api = LineBotApi('MmmCH2ehgjHJTC8C5NWsPgO1fNcFyn5Xk1N5QftSpJMaukLkJ2WIsGHIMWFmYD2w8rDIe9zIz58GyoLJGMirKODWIu19Ly2H8m58iXwPgd7YLloa1QdDC45G3Rg8/Jw+jECIwVe7/RIMnSobbMPthAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('68df133d3d1261f064763a439ff3f268')
botimize = Botimize('13CIVSYVFO85N1EI116G6J3O3E93IXZY',"line")

@app.route("/", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    event = request.get_json()
    botimize.log_incoming(event)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    outgoingLog = {
        'receiver': {
          'id': 'Adam',
          'name': 'USER_SCREEN_NAME'
        },
        'content': {
          'type': 'text', 
          'text': 'hello'
        }
    };
    botimize.log_outgoing(outgoingLog)

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()