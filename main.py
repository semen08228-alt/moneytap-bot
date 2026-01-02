from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os

TOKEN = os.getenv("BOT_TOKEN")

# Хранилище кликов (пока в памяти)
users = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in users:
        users[user_id] = 0

    keyboard = [
        [InlineKeyboardButton("💸 ТАП!", callback_data="tap")],
        [InlineKeyboardButton("📊 Баланс", callback_data="balance")]
    ]

    await update.message.reply_text(
        "Добро пожаловать в 💸 MoneyTap!\n\nЖми кнопку и зарабатывай монеты 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    if user_id not in users:
        users[user_id] = 0

    if query.data == "tap":
        users[user_id] += 1
        await query.edit_message_text(
            f"💰 Ты заработал +1 монету!\n\nБаланс: {users[user_id]}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💸 ТАП!", callback_data="tap")],
                [InlineKeyboardButton("📊 Баланс", callback_data="balance")]
            ])
        )

    elif query.data == "balance":
        await query.edit_message_text(
            f"📊 Твой баланс: {users[user_id]} монет",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💸 ТАП!", callback_data="tap")]
            ])
        )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()

if __name__ == "__main__":
    main()
