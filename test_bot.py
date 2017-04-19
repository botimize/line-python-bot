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

line_bot_api = LineBotApi(<YOUR_CHANNEL_ACCESS_TOKEN>)
handler = WebhookHandler(<YOUR_CHANNEL_SECRET>)
botimize = Botimize(<YOUR_BOTIMIZE_APIKEY>,"line")

@app.route("/callback", methods=['POST'])
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