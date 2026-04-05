import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# ================== TOKENS ==================
import os
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# ================== START ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎬 Viral Script Bot\n\n"
        "Send any topic (e.g. 'Bermuda Triangle')\n\n"
        "⚡ Free: 2 scripts/day\n"
        "💰 Premium: Unlimited"
    )

# ================== HELP ==================
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("बस topic bhejo, main script bana dunga 😏")

# ================== AI ==================
def generate_text(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "user",
                "content": f"Write a viral YouTube Shorts narration on: {prompt}. Start with a shocking hook. Use very short sentences. No characters, no scenes, no dialogues. Only fast-paced narration. Build curiosity. Keep it under 80 words. End with a strong twist or question."
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)

        if response.status_code != 200:
            return f"❌ API Error: {response.text}"

        result = response.json()
        return result["choices"][0]["message"]["content"]

    except Exception as e:
        return f"❌ Error: {str(e)}"

# ================== MESSAGE ==================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    msg = await update.message.reply_text("⏳ Generating...")

    reply = generate_text(user_text)

    await msg.edit_text(f"✅ Done!\n\n{reply}")

# ================== MAIN ==================
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot is running...")
    app.run_polling()

# ================== RUN ==================
if __name__ == "__main__":
    main()
