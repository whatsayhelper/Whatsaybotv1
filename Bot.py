import os
import openai
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Laad de omgevingsvariabelen
from dotenv import load_dotenv
load_dotenv()

# Haal je Telegram Bot Token en OpenAI API Key op
TELEGRAM_API_KEY = os.getenv('TELEGRAM_BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

openai.api_key = OPENAI_API_KEY

# Start de bot
def start(update, context):
    update.message.reply_text('Hallo! Hoe kan ik je helpen?')

def respond(update, context):
    user_message = update.message.text
    response = get_openai_response(user_message)
    update.message.reply_text(response)

def get_openai_response(user_message):
    response = openai.Completion.create(
        engine="text-davinci-003",  # of de nieuwste versie die je hebt
        prompt=user_message,
        max_tokens=150
    )
    return response.choices[0].text.strip()

def main():
    updater = Updater(TELEGRAM_API_KEY, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, respond))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
