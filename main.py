from telegram_bot import TelegramBot

if __name__ == '__main__':
    TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
    bot = TelegramBot(TELEGRAM_TOKEN)
    print("Bot instance created.")
    bot.run()



