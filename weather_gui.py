import requests
import tkinter as tk

API_KEY='ab21e99fd9e01412b13763720ed7f79f'

root=tk.Tk()

entry=tk.Entry(root,width=20)
entry.pack(pady=10)

def get_weather():
    city=entry.get()
    url=f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=ja"
    response=requests.get(url)
    data=response.json()

    if response.status_code !=200:
        result_label.config(text='都市名が正しくないか、データ取得に失敗しました。')
        return

    weather=data['weather'][0]['description']
    temp=data['main']['temp']
    result=f'{city}の天気：{weather}\n気温：{temp}℃'
    result_label.config(text=result)

#GUI構成
root.title('現在の天気')
root.geometry('300x200')

btn=tk.Button(root,text='天気を調べる',command=get_weather)
btn.pack(pady=5)

result_label=tk.Label(root,text='')
result_label.pack(pady=10)

root.mainloop()