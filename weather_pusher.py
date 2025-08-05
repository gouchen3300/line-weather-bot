import os
import requests
from dotenv import load_dotenv
from linebot import LineBotApi
from linebot.models import TextSendMessage

load_dotenv()

LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
CWB_API_KEY = os.getenv("CWB_API_KEY")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)

USER_IDS = [
    "Uba1b04df5a26f27776591bcd75891712"
]

WEEKLY_WEATHER_API = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-091"

def get_weekly_weather(location_name):
    params = {
        "Authorization": CWB_API_KEY,
        "locationName": location_name,
        "format": "JSON"
    }

    try:
        res = requests.get(WEEKLY_WEATHER_API, params=params)
        data = res.json()
        records = data["records"]["locations"][0]["location"][0]
        name = records["locationName"]
        weather_elements = {el["elementName"]: el["time"] for el in records["weatherElement"]}

        result = f"【{name} 一週天氣預報】\n"

        for i in range(0, 7):
            start_time = weather_elements["Wx"][i]["startTime"][:10]
            wx = weather_elements["Wx"][i]["elementValue"][0]["value"]
            pop = weather_elements["PoP12h"][i]["elementValue"][0]["value"]
            min_temp = weather_elements["MinT"][i]["elementValue"][0]["value"]
            max_temp = weather_elements["MaxT"][i]["elementValue"][0]["value"]

            result += f"\n📅 {start_time}\n天氣：{wx}\n降雨機率：{pop}%\n氣溫：{min_temp}°C ~ {max_temp}°C\n"

        return result

    except Exception as e:
        return f"⚠️ 無法取得天氣資料：{str(e)}"

def push_weather():
    message = get_weekly_weather("高雄市")
    for user_id in USER_IDS:
        try:
            line_bot_api.push_message(user_id, TextSendMessage(text=message))
        except Exception as e:
            print(f"❌ 發送給 {user_id} 失敗：{str(e)}")

if __name__ == "__main__":
    push_weather()
