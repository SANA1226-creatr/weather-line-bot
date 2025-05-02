from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import requests
import os

app = Flask(__name__)

# LINE Botの設定
LINE_CHANNEL_SECRET = '65caa9c1ad0f9aeb8fed4c84d6e849a4'
LINE_CHANNEL_ACCESS_TOKEN = '5vsLzylYyE6hwyPdaLldvgGqF+aaDiEVdA49O0sacnTSRnwBFmxlR3h5yIp4rPkNDCI5YF3Gp7qRbuHBDbvrm2YHCCNG+lh/aPNufUrBr1QCJCsfnmEUN0hD9bXpLwdnLq03tLm7jIjnbjhlHTZzygdB04t89/1O/w1cDnyilFU='

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 天気API設定
API_KEY = 'ab21e99fd9e01412b13763720ed7f79f'

# メッセージ受信時の処理
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except LineBotApiError as e:
        print(f"Error: {e}")
        abort(400)
    
    return 'OK'

# メッセージ処理
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("handle_message が呼ばれました")
    print("受信メッセージ:", event.message.text)

    message = event.message.text
    city = message.strip()

    # 天気情報を取得
    weather_info = get_weather(city)

    # 天気情報を返信
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=weather_info)
    )


def get_weather(city):
    print(f"get_weather呼び出し: city = {city}")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=ja"
    response = requests.get(url)
    print("ステータスコード:", response.status_code)
    print("レスポンス内容:", response.text)

    if response.status_code != 200:
        return f"{city} の天気情報が見つかりませんでした。→英語で送ってください！"

    data = response.json()
    weather = data['weather'][0]['description']
    temp = data['main']['temp']
    return f"{city}の天気は{weather}、気温は{temp}°Cです。"



if __name__ == "__main__":
    # 環境変数で指定されたポート
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)

