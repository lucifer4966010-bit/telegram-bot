import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio

TOKEN = os.getenv("TOKEN")

spam_tasks = {}  # user_id : asyncio task

async def spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if len(context.args) < 2:
        await update.message.reply_text(
            "❌ Format galat hai\nUse:\n/spam 10 Hello bhai"
        )
        return

    try:
        count = int(context.args[0])   # first argument = number
        message = " ".join(context.args[1:])  # rest = message
    except:
        await update.message.reply_text("❌ Number galat hai")
        return

    async def send_messages():
        for i in range(count):
            await update.message.reply_text(message)
            await asyncio.sleep(0.2)

    task = asyncio.create_task(send_messages())
    spam_tasks[user_id] = task


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id in spam_tasks:
        spam_tasks[user_id].cancel()
        del spam_tasks[user_id]
        await update.message.reply_text("🛑 Spam stopped")
    else:
        await update.message.reply_text("Koi spam chal nahi raha 🙂")


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("spam", spam))
app.add_handler(CommandHandler("stop", stop))

print("🤖 Bot is running...")
app.run_polling()
