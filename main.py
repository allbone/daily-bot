import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import requests

loaded = load_dotenv()

if not loaded:
    print("警告：無法載入 .env 檔案！")

token = os.getenv("DISCORD_TOKEN")
print(f"Token 的值是: {token}")
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
test_value = os.getenv("TEST_VARIABLE")
print(f"測試變數的值是: {test_value}")

# 設定機器人前綴 
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"目前登入身份 --> {bot.user.name}")

@bot.event
async def on_member_join(member):
    await member.send("歡迎來到伺服器！")
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "shit" in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author.mention} - 請注意用詞！")

    await bot.process_commands(message)

    if message.author == bot.user:
        return

    if "!weather" in message.content.lower():
        # 使用 OpenWeatherMap API 獲取天氣資訊
        api_key = os.getenv("OPENWEATHER_API_KEY")
        await message.channel.send("請輸入想查詢天氣的城市名稱：")

        def check(m):
            return m.author == message.author and m.channel == message.channel

        try:
            reply = await bot.wait_for("message", check=check, timeout=30.0)
            city = reply.content.strip()
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=zh_tw"
            response = requests.get(url)
            data = response.json()

            if response.status_code == 200:
                weather = data["weather"][0]["description"]
                temp = data["main"]["temp"]
                await message.channel.send(f"今天 {city} 的天氣是 {weather}，氣溫約 {temp}°C。")
            else:
                await message.channel.send("無法取得天氣資訊，請確認城市名稱是否正確！")
        except Exception as e:
            await message.channel.send("發生錯誤，無法取得天氣資訊！")
            print(f"Error: {e}")
    await bot.process_commands(message)

    if "!route" in message.content.lower():
        await message.channel.send("請輸入格式正確的內容：出發地,目的地,出發時間（例如：台北,高雄,08:00）")

        def check(m):
            return m.author == message.author and m.channel == message.channel

        try:
            reply = await bot.wait_for("message", check=check, timeout=60.0)
            inputs = reply.content.split(",")
            if len(inputs) != 3:
                await message.channel.send("格式錯誤，請重新輸入！")
                return

            origin, destination, departure_time = inputs
            # 使用 Google Maps API 或其他交通工具 API 計算路線
            api_key = os.getenv("GOOGLE_MAPS_API_KEY")
            url = (
                f"https://maps.googleapis.com/maps/api/directions/json?"
                f"origin={origin}&destination={destination}&departure_time=now&key={api_key}"
            )
            response = requests.get(url)
            data = response.json()

            if response.status_code == 200 and data["status"] == "OK":
                route = data["routes"][0]["legs"][0]
                duration = route["duration"]["text"]
                distance = route["distance"]["text"]
                await message.channel.send(
                    f"從 {origin} 到 {destination} 的距離是 {distance}，預計需要 {duration}。"
                )
            else:
                await message.channel.send("無法取得路線資訊，請確認輸入的地點是否正確！")
        except Exception as e:
            await message.channel.send("發生錯誤，無法計算路線！")
            print(f"Error: {e}")

    if "!簡介" in message.content.lower():
        await message.channel.send
        (
            "👥 第十組 WakeMeUp 🛏️\n"
            "個人化智慧通勤規劃 Line Bot\n\n"
            "💻 開發環境：Python 3 \n\n"
            "📌 成員：\n"
            "藥學二　王瑋仁\n"
            "化工二　呂子毅\n"
            "藥學二　唐翊安\n"
            "工海一　張博彥"
        )

    if "!指令" in message.content.lower():
        await message.channel.send(            
            "目前支援的功能有：\n\n"
            "🌀 天氣查詢 ➤ 請輸入：\n"
            "　　天氣 【地點】\n"
            "　　例如：天氣 台北\n\n"
            "🗺️ 路線查詢 ➤ 請輸入：\n"
            "　　路線 【出發地】,【目的地】,【時間】\n"
            "　　例如：路線 台北,高雄,08:00\n\n"
            "📚 功能查詢 ➤ 輸入：\n"
            "　　功能\n\n"
            "🧑🏻‍💻 開發者查詢 ➤ 輸入：\n"
            "　　簡介\n\n"
            "🔁 其他訊息 ➤ 原樣回覆")
    
bot.run(token, log_handler=handler, log_level=logging.DEBUG)
