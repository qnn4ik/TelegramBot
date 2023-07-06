from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
from dotenv import load_dotenv, find_dotenv
from typing import Final

from money import Currency

load_dotenv(find_dotenv())
TOKEN: Final = os.getenv('TOKEN')

BOT_USERNAME: Final = '@redberrypie_bot'


# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Thanks for chatting with me. I am Redberry Bot!")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I am Redberry Bot! Please type something so I can respond!")


async def get_currency_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from datetime import datetime as dt

    currency = Currency()
    currency.set_currency()
    now = dt.now()
    bot_reply = f"Currencies at {now.day:02}.{now.month:02}, {now.hour}:{now.minute}\n"
    for curr, price in currency.get_currency().items():
        bot_reply += f'{curr}: {price}\n'

    await update.message.reply_text(bot_reply)


# Responses
def handle_response(text: str) -> str:
    processed: str = text.lower()

    if 'hello' in processed:
        return 'Hey there!'

    if 'how are you' in processed:
        return 'I am okay'

    if 'i love python' in processed:
        return 'so do I'

    return 'I do not know what to say'


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    user_id: int = update.message.from_user.id
    text: str = update.message.text

    print(f'User ({user_id}) from ({update.message.chat.id}) in {message_type} says: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, "").strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    print(f'Bot says: "{response}"')

    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Updates {update} caused error: {context.error}")


if __name__ == '__main__':
    print('Starting...')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('get_currency', get_currency_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    # Polls the bot
    print('Polling...')
    app.run_polling(poll_interval=3)
