
import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from openai import AsyncOpenAI

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.environ["BOT_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
Ты ИИ-участник Telegram-группы «Стрелка 🍂🎃».
Общайся по-русски, как живой участник: естественно, коротко,
с юмором, иронией и дружескими подколами.
Не будь официальным, не повторяйся и не спамь.
Если не знаешь ответа, не выдумывай факты.
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Йо 😎 Я Стрелка AI 🍂🎃! Напиши мне сообщение."
    )

async def reply_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    if update.effective_chat.type != "private":
        if not update.message.reply_to_message:
            return
        if update.message.reply_to_message.from_user.id != context.bot.id:
            return

    try:
        response = await client.responses.create(
            model="gpt-4.1-mini",
            instructions=SYSTEM_PROMPT,
            input=update.message.text,
            max_output_tokens=180,
        )
        answer = response.output_text.strip()
        if answer:
            await update.message.reply_text(answer)
    except Exception:
        logging.exception("AI reply failed")
        await update.message.reply_text("Чёт я завис 😅 Попробуй ещё раз.")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_ai))
    app.run_polling()

if __name__ == "__main__":
    main()
      
