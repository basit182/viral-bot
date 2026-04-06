import requests
import os
import threading
from flask import Flask
from datetime import date
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# ================= WEB SERVER =================
app_web = Flask(__name__)

@app_web.route("/")
def home():
    return "Bot is running!"

def run_web():
    app_web.run(host="0.0.0.0", port=10000)

threading.Thread(target=run_web).start()

# ================= TOKENS =================
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ================= LIMIT SYSTEM =================
user_usage = {}
FREE_LIMIT = 10

def check_limit(user_id):
    today = str(date.today())

    if user_id not in user_usage:
        user_usage[user_id] = {"date": today, "count": 0}

    if user_usage[user_id]["date"] != today:
        user_usage[user_id] = {"date": today, "count": 0}

    if user_usage[user_id]["count"] >= FREE_LIMIT:
        return False

    user_usage[user_id]["count"] += 1
    return True

# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 ViralForge AI\n\n"
        "Send anything:\n"
        "• Ask questions (like ChatGPT)\n"
        "• Get viral scripts\n"
        "• Generate images\n\n"
        "⚡ Free limit: 7/day"
    )

# ================= AI TEXT =================
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
                "content": f"""
You are an advanced AI assistant.

1. If user asks normal questions:
- Answer clearly
- Be helpful, smart, human-like

2. If user asks for scripts or content:
- Create HIGHLY engaging viral scripts
- Strong hook in first 2 seconds
- Short powerful lines
- Add curiosity and suspense
- End with twist

3. Shorts format:
(0:01 - 0:05) Hook  
(0:06 - 0:10) Build curiosity  
(0:11 - 0:20) Main reveal  
(0:21 - 0:30) Twist  

4. Long videos:
- Structured script (intro → climax → ending)

User: {prompt}
"""
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

# ================= IMAGE =================
def generate_image(prompt):
    return f"https://image.pollinations.ai/prompt/{prompt}"

# ================= MESSAGE HANDLER =================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_text = update.message.text

    # limit check
    if not check_limit(user_id):
        await update.message.reply_text(
            f"""🚫 Free limit reached ({FREE_LIMIT}/day)

But wait...

Your next viral idea could blow up 🚀

Unlock:
⚡ Unlimited scripts
🔥 Better viral hooks
🎯 High engagement ideas

💎 Premium: ₹99/month
"""
        )
        return

    msg = await update.message.reply_text("⏳ Processing...")

    # image detection
    if "image" in user_text.lower() or "generate image" in user_text.lower():
        img_url = generate_image(user_text)
        await update.message.reply_photo(photo=img_url)
        return

    # normal AI
    reply = generate_text(user_text)
    await msg.edit_text(f"✅ Done!\n\n{reply}")

# ================= MAIN =================
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot is running...")
    app.run_polling()

# ================= RUN =================
if __name__ == "__main__":
    main()
