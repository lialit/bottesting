import os
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from telegram import Update
from langdetect import detect
from deep_translator import GoogleTranslator

# =================== Налаштування ===================
BOT_TOKEN = "8513190655:AAFgc4xkUeCDlIohMk-2W8mNmDZgo2iHb1A"  # Замініть на свій токен
HISTORY_FILE = "history.txt"
MAX_LENGTH = 1000  # обмеження символів для Telegram

# =================== Простий словниковий AI ===================
# Ви можете додати сюди більше шаблонів
RESPONSES = {
    "hello": "Hello! How can I help you?",
    "hi": "Hi there! How can I help you?",
    "how are you": "I'm an AI bot, I am always okay!",
    "bye": "Goodbye! Have a nice day!",
}

DEFAULT_RESPONSE = "I am not sure how to respond to that, but I will try to help you!"

# =================== Команди ===================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привіт 👋 Я супер-легкий локальний бот.\nПиши будь-якою мовою EN/DE/UA!"
    )

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.strip()

    # 1️⃣ Визначаємо мову користувача
    try:
        user_lang = detect(user_text)
    except:
        user_lang = "uk"

    # 2️⃣ Перекладаємо в англійську для логіки
    try:
        prompt_en = GoogleTranslator(source="auto", target="en").translate(user_text)
    except:
        prompt_en = user_text.lower()

    prompt_en_lower = prompt_en.lower()

    # 3️⃣ Вибір відповіді
    answer_en = DEFAULT_RESPONSE
    for key, val in RESPONSES.items():
        if key in prompt_en_lower:
            answer_en = val
            break

    # 4️⃣ Переклад назад у мову користувача
    try:
        final_answer = GoogleTranslator(source="en", target=user_lang).translate(answer_en)
    except:
        final_answer = answer_en

    # 5️⃣ Обрізаємо до MAX_LENGTH
    final_answer = final_answer[:MAX_LENGTH]

    # 6️⃣ Відправляємо відповідь
    await update.message.reply_text(final_answer)

    # 7️⃣ Зберігаємо історію
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(f"User ({user_lang}): {user_text}\nBot: {final_answer}\n{'-'*50}\n")

# =================== Основна функція ===================

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("Супер-легкий бот запущено ✅")
    app.run_polling()

# =================== Точка входу ===================

if __name__ == "__main__":
    main()



