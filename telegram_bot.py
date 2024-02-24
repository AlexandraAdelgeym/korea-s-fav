from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from spotify_client import SpotifyClient
from korean_learning_client import KoreanLearningClient
from news_client import NewsClient
from drama_client import DramaClient

TELEGRAM_TOKEN = "6554966811:AAGoI6Bey2dfrpSLmTOeBIPoFBhG7YA_-7s"


class TelegramBot:
    def __init__(self, token):
        self.application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
        self.spotify_client = SpotifyClient("167f663ad2ec4bdbb0b4b0383a181301", "ffec7936571a4fc6934be6128e5cb56f", "http://example.com", "Alexandra")
        self.korean_learning_client = KoreanLearningClient('data/korean_words.csv')
        self.news_client = NewsClient()
        self.drama_client = DramaClient()

        async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
            start_message = "Hi! \nWhat would you like?"

            keyboard = ReplyKeyboardMarkup([
                [KeyboardButton("🆕 What's new today?")],
                [KeyboardButton("💬 Learn Korean")]
            ], resize_keyboard=True, one_time_keyboard=False)

            reply_markup = keyboard.to_dict()

            await context.bot.send_message(chat_id=update.effective_chat.id, text=start_message,
                                           reply_markup=reply_markup)

        async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
            query = update.callback_query
            callback_data = query.data

            if callback_data == 'top_things':
                await top_things(update, context)
            elif callback_data == 'learn_korean':
                await learn_korean(update, context)
            elif callback_data.startswith('option_'):
                await handle_option_selection(update, context)

        async def top_things(update: Update, context: ContextTypes.DEFAULT_TYPE):
            top5_songs = self.spotify_client.get_top5()
            top_dramas = self.drama_client.get_top_dramas()
            top_news = self.news_client.get_top_news()

            combined_message_songs = "\n".join(top5_songs)

            combined_message_dramas = "\n".join(top_dramas)
            combined_message_news = "\n".join(top_news)

            all_messages = (f"Top songs: \n \n{combined_message_songs} \n\nTop dramas: "
                            f"\n \n{combined_message_dramas}\n\nTop news: \n\n{combined_message_news}")

            await context.bot.send_message(chat_id=update.effective_chat.id, text=all_messages,
                                           parse_mode='HTML')

        current_words_pair = None
        correct_translation = None

        options = None

        async def learn_korean(update: Update, context: ContextTypes.DEFAULT_TYPE):
            current_words_pair = self.korean_learning_client.get_random_pair()
            correct_translation = current_words_pair[1]

            options = self.korean_learning_client.generate_options(correct_translation)

            message = f"Translate the Korean word:\n\n{current_words_pair[0]}"
            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton(options[0], callback_data='option_0')],
                [InlineKeyboardButton(options[1], callback_data='option_1')],
                [InlineKeyboardButton(options[2], callback_data='option_2')],
                [InlineKeyboardButton(options[3], callback_data='option_3')]
            ])
            await context.bot.send_message(chat_id=update.effective_chat.id, text=message, reply_markup=reply_markup)

        async def handle_option_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
            query = update.callback_query
            selected_option_index = int(query.data.split('_')[1])

            if options[selected_option_index] == correct_translation:
                message = "✅ Correct! Next word:"
            else:
                message = f"❌ Wrong! The right answer is: {correct_translation}\nNext word:"

            await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
            await learn_korean(update, context)

        async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
            text = update.message.text

            if text == "🆕 What's new today?":
                await top_things(update, context)
            elif text == "💬 Learn Korean":
                await learn_korean(update, context)

        if __name__ == '__main__':
            application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

            start_handler = CommandHandler('start', start)
            application.add_handler(start_handler)

            application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
            application.add_handler(CallbackQueryHandler(button_click, pattern='top_things'))
            application.add_handler(CallbackQueryHandler(button_click, pattern='^learn_korean$|^option_'))

            application.run_polling()


