import os
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from telegram import Update
from langdetect import detect
from deep_translator import GoogleTranslator

# =================== Налаштування ===================

BOT_TOKEN = "8513190655:AAFgc4xkUeCDlIohMk-2W8mNmDZgo2iHb1A"
HISTORY_FILE = "history.txt"
MAX_LENGTH = 1000

# =================== Простий AI ===================

RESPONSES = {
    "hello": "Hello! How can I help you?",
    "hi": "Hi 🙂 How can I help?",
    "how are you": "I'm fine and ready to help you!",
    "bye": "Goodbye! Have a nice day!",
    "weather": "Tell me your city and I will try to help.",
    "time": "I don't know the exact time, but I can help with other things 🙂",
}

DEFAULT_RESPONSE = "🙂 I understand you. Tell me more."

# =================== Команди ===================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привіт 👋 Я легкий Telegram-бот.\nПиши українською, англійською або німецькою 🙂"
    )

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.strip()

    # 1️⃣ Визначаємо мову
    try:
        user_lang = detect(user_text)
    except:
        user_lang = "uk"

    # 2️⃣ Переклад у EN для логіки
    try:
        prompt_en = GoogleTranslator(source="auto", target="en").translate(user_text)
    except:
        prompt_en = user_text

    prompt_en = prompt_en.lower()

    # 3️⃣ Логіка відповіді
    answer_en = DEFAULT_RESPONSE
    for key, val in RESPONSES.items():
        if key in prompt_en:
            answer_en = val
            break

    # 4️⃣ Переклад назад
    try:
        final_answer = GoogleTranslator(source="en", target=user_lang).translate(answer_en)
    except:
        final_answer = answer_en

    final_answer = final_answer[:MAX_LENGTH]

    # 5️⃣ Відправка
    await update.message.reply_text(final_answer)

    # 6️⃣ Історія
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(f"User ({user_lang}): {user_text}\nBot: {final_answer}\n{'-'*40}\n")


# =================== Main ===================

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("✅ Бот запущено")
    app.run_polling()


if __name__ == "__main__":
    main()
