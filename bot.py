import requests
import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# ================== WEB SERVER (Render/Railway keep alive) ==================
app_web = Flask(__name__)

@app_web.route("/")
def home():
    return "Bot is running!"

def run_web():
    app_web.run(host="0.0.0.0", port=10000)

threading.Thread(target=run_web).start()

# ================== TOKENS ==================
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ================== START ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎬 Viral Script + AI Bot\n\n"
        "Send anything:\n"
        "- Ask questions (like ChatGPT)\n"
        "- Ask for scripts (shorts/reels/long videos)\n\n"
        "🔥 Example:\n"
        "👉 'What is AI?'\n"
        "👉 'Make viral script on black hole'"
    )

# ================== HELP ==================
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("बस topic bhejo, main sab handle karunga 😎")

# ================== AI FUNCTION ==================
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
You are an advanced AI assistant like ChatGPT.

1. If user asks normal questions:
- Answer clearly
- Be helpful, smart, human-like
- Give practical answers

2. If user asks for scripts/content:
- Create HIGHLY engaging viral scripts
- Strong hook in first 2 seconds
- Short, powerful sentences
- Build curiosity & suspense
- Add pattern interrupts
- End with twist or strong impact

3. Shorts format:
(0:01 - 0:05) Hook  
(0:06 - 0:10) Build curiosity  
(0:11 - 0:20) Main reveal  
(0:21 - 0:30) Twist  

4. Long videos:
- Full structured script
- Intro → Build-up → Explanation → Climax → Ending
- High retention style

Always:
- Be engaging
- Avoid boring tone
- Sound like real human

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

# ================== MESSAGE HANDLER ==================
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
