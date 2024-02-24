from telegram_bot import TelegramBot

if __name__ == '__main__':
    TELEGRAM_TOKEN = "6554966811:AAGoI6Bey2dfrpSLmTOeBIPoFBhG7YA_-7s"
    bot = TelegramBot(TELEGRAM_TOKEN)
    bot.application.run_polling()
