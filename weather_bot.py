import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes


TELEGRAM_TOKEN = '7409978697:AAFXd3o0wRqhoNVUKidBY7Svd0pbPJaUwtU'   # Example: '123456:ABCDEF...' (after reset)
WEATHER_API_KEY = 'e9ba5512c3f392fbe27f67b2bf35e460'  # Example: 'e9ba5512c3f392fbe27f67b2bf35e460'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hello! I'm your Weather Wizard Bot!\n"
        "Send /weather <city> to get the current weather + 3-day forecast.\n"
        "Example: /weather Kochi"
    )

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Please provide a city name.\nExample: /weather Kochi")
        return

    city = ' '.join(context.args)
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={WEATHER_API_KEY}&units=metric"

    response = requests.get(url)
    if response.status_code != 200:
        await update.message.reply_text("❌ Could not retrieve weather. Please check the city name!")
        return

    data = response.json()

    # Current weather
    current = data['list'][0]
    desc = current['weather'][0]['description'].title()
    temp = current['main']['temp']

    # 3-day forecast (grab forecast at 12:00 PM)
    forecast = []
    for item in data['list']:
        if '12:00:00' in item['dt_txt']:
            date = item['dt_txt'].split()[0]
            d = item['weather'][0]['description'].title()
            t = item['main']['temp']
            forecast.append(f"{date}: {d}, {t}°C")
            if len(forecast) == 3:
                break

    msg = f"🌤️ *Current weather in {city.title()}*\n{desc}, {temp}°C\n\n🌦️ *3-day forecast:*\n"
    msg += "\n".join(forecast)

    await update.message.reply_text(msg, parse_mode="Markdown")

# Main bot setup
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("weather", weather))

    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()