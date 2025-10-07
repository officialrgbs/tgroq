import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

load_dotenv()

# Load environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! I'm your Groq-powered Telegram bot.")

def query_groq(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",  # or "llama3-70b-8192"
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    }
    r = requests.post(url, headers=headers, json=payload)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await update.message.reply_text("💭 Thinking...")
    try:
        response = query_groq(user_message)
        await update.message.reply_text(response)
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

def main():
    if not TELEGRAM_TOKEN or not GROQ_API_KEY:
        print("❌ Missing environment variables!")
        return

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🚀 Bot is running on Render...")
    app.run_polling()

if __name__ == "__main__":
    main()
