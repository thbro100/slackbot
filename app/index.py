import slack
import os
from pathlib import Path
from dotenv import load_dotenv
import schedule
import time
import requests

# response = {
#     "coord": {
#         "lon": -111.9666,
#         "lat": 43.4696
#     },
#     "weather": [{
#         "id": 800,
#         "main": "Clear",
#         "description": "clear sky",
#         "icon": "01n"
#     }],
#     "base": "stations",
#     "main": {
#         "temp": 48.9,
#         "feels_like": 48.9,
#         "temp_min": 45.34,
#         "temp_max": 54.1,
#         "pressure": 1022,
#         "humidity": 50
#     },
#     "visibility": 10000,
#     "wind": {
#         "speed": 0,
#         "deg": 0
#     },
#     "clouds": {
#         "all": 1
#     },
#     "dt": 1633145564,
#     "sys": {
#         "type": 2,
#         "id": 2001801,
#         "country": "US",
#         "sunrise": 1633094735,
#         "sunset": 1633136943
#     },
#     "timezone": -21600,
#     "id": 5583997,
#     "name": "Ammon",
#     "cod": 200
# }

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
top_temp = 75
top_temp_bool = True
bottom_temp_bool = True
lastMessage = {'text':''}
bottom_temp = 65
city = 5583997
url = f"http://api.openweathermap.org/data/2.5/weather?units=imperial&id={city}&APPID={os.environ['WEATHER_APP_ID']}"

def get_weather():
    response = requests.get(url).json()
    if response['main']['temp'] >= top_temp:
        text = "Time to close the windows! It's getting to hot."
        if lastMessage['text']!=text:
            lastMessage['text'] = text
            print(lastMessage)
            client.chat_postMessage(channel='#slacknotifications',text=text)

    elif response['main']['temp'] <= bottom_temp:
            text = "Time to close the windows! It's getting to cold."
            if lastMessage['text']!=text:
                lastMessage['text'] = text
                client.chat_postMessage(channel='#slacknotifications',text=text)
    else:
        text = "Time to open the windows! It's nice outside!"
        if lastMessage['text']!=text:
            lastMessage['text'] = text
            client.chat_postMessage(channel='#slacknotifications',text=text)

get_weather()


schedule.every().hour.at(":00").do(get_weather)
schedule.every().hour.at(":15").do(get_weather)
schedule.every().hour.at(":30").do(get_weather)
schedule.every().hour.at(":45").do(get_weather)

while True:
    schedule.run_pending()
    time.sleep(1)