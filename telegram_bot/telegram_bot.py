import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from decouple import config

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привет! Как тебя зовут?')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_name = update.message.text
    await update.message.reply_text(f'Приятно познакомиться, {user_name}! Перейдите на наш сайт: http://127.0.0.1:8001/dreamtaste')

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.warning(f'Update {update} caused error {context.error}')

async def main():
    application = ApplicationBuilder().token(config('TELEGRAM_TOKEN')).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error)
    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())