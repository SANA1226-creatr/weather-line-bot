
import requests

API_KEY='ab21e99fd9e01412b13763720ed7f79f'

def get_weather(city):
    url=f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=ja'
    response=requests.get(url)
    data=response.json()

    if response.status_code !=200:
        print('エラー都市名が正しくない可能性があります！')
        return

    weather=data['weather'][0]['description']
    temp=data['main']['temp']
    print(f'{city}の天気:{weather}、気温:{temp}℃')

#実行部分
city=input('都市名を入力してください（例：Tokyo）')
get_weather(city)

