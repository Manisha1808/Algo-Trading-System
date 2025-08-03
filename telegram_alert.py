from telegram import Bot
import logging


BOT_TOKEN = "Bot_token"

CHAT_ID = "chat_id"  

bot = Bot(token=BOT_TOKEN)

def send_telegram_message(message: str):
    try:
        bot.send_message(chat_id=CHAT_ID, text=message)
        logging.info("Telegram message sent successfully.")
    except Exception as e:
        logging.error(f"Failed to send Telegram message: {e}")
