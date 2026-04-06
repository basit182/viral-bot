import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import threading
from flask import Flask

app_web = Flask(__name__)

@app_web.route("/")
def home():
    return "Bot is running!"

def run_web():
    app_web.run(host="0.0.0.0", port=10000)

threading.Thread(target=run_web).start()
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
            "content": f"""You are an advanced AI assistant like ChatGPT.

Your behavior:

1. If the user asks normal questions:
- Answer clearly
- Be helpful, smart, and human-like
- Explain simply but effectively
- Give practical and useful answers

2. If the user asks about video ideas, scripts, reels, shorts, or content:
- Create HIGHLY engaging and viral content
- Use strong hooks in the first 2 seconds
- Keep sentences short and powerful
- Build curiosity and suspense
- Add pattern interrupts
- End with a twist, question, or strong impact

3. For YouTube Shorts / Reels scripts:
Format like this:
(0:01 - 0:05) Hook  
(0:06 - 0:10) Build curiosity  
(0:11 - 0:20) Main reveal  
(0:21 - 0:30) Twist / ending  

4. For long videos:
- Give structured script
- Include intro, build-up, explanation, climax, ending
- Keep audience retention high

5. Always:
- Be confident
- Be engaging
- Avoid boring answers
- Sound like a real intelligent human

User: {prompt}
"""
"""
"messages": [
    {
        "role": "user",
        "content": f"""
You are a powerful AI assistant.

If the user asks for a viral script, create a HIGHLY viral YouTube Shorts script.

Otherwise, behave like ChatGPT:
- Answer clearly
- Be helpful
- Give smart and human-like responses

User: {prompt}
"""
    }
    ]
"""
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
