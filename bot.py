import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio

TOKEN = os.getenv("TOKEN")

spam_tasks = {}  # user_id : asyncio task

async def spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id  # group ya private chat id

    if len(context.args) < 2:
        await context.bot.send_message(
            chat_id=chat_id,
            text="❌ Format galat hai\nUse:\n/spam 10 Hello bhai"
        )
        return

    try:
        count = int(context.args[0])   # first argument = number
        message = " ".join(context.args[1:])  # rest = message
    except:
        await context.bot.send_message(chat_id=chat_id, text="❌ Number galat hai")
        return

    async def send_messages():
        for i in range(count):
            await context.bot.send_message(chat_id=chat_id, text=message)
            await asyncio.sleep(0.2)

    task = asyncio.create_task(send_messages())
    spam_tasks[user_id] = task


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    if user_id in spam_tasks:
        spam_tasks[user_id].cancel()
        del spam_tasks[user_id]
        await context.bot.send_message(chat_id=chat_id, text="🛑 Spam stopped")
    else:
        await context.bot.send_message(chat_id=chat_id, text="Koi spam chal nahi raha 🙂")


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("spam", spam))
app.add_handler(CommandHandler("stop", stop))

print("🤖 Bot is running...")
app.run_polling()
