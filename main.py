import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    ContextTypes
)
from datetime import datetime, date
from panchang import fetch_panchang_data
from horoscope import fetch_horoscope
from config import BOT_TOKEN

logging.basicConfig(level=logging.INFO)

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌟 Welcome to AstroBot!\n\n"
        "Use /tithi to get today’s Panchang\n"
        "Use /horoscope to view your Zodiac prediction\n"
        "Use /birthdata ddmmyyyy or /marriage ddmmyyyy to view Panchang on special dates"
    )

# /tithi
async def tithi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    today = date.today().isoformat()
    result = fetch_panchang_data(today)
    await update.message.reply_text(f"📆 Today’s Panchang:\n{result}")

# /birthdata and /marriage
async def custom_panchang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        dob = context.args[0]
        try:
            dt = datetime.strptime(dob, "%d%m%Y").date()
            result = fetch_panchang_data(dt.isoformat())
            await update.message.reply_text(f"📆 Panchang for {dob}:\n{result}")
        except:
            cmd = update.message.text.split()[0]
            await update.message.reply_text(
                f"⚠️ *Invalid date format!*\nUse:\n`{cmd} 14022024`", parse_mode="Markdown"
            )
    else:
        cmd = update.message.text.split()[0]
        await update.message.reply_text(
            f"⚠️ *Date missing!*\nUse:\n`{cmd} 14022024`", parse_mode="Markdown"
        )

# /horoscope
async def horoscope(update: Update, context: ContextTypes.DEFAULT_TYPE):
    zodiac_buttons = [
        ["♈ Aries", "♉ Taurus", "♊ Gemini"],
        ["♋ Cancer", "♌ Leo", "♍ Virgo"],
        ["♎ Libra", "♏ Scorpio", "♐ Sagittarius"],
        ["♑ Capricorn", "♒ Aquarius", "♓ Pisces"]
    ]
    keyboard = [
        [InlineKeyboardButton(text, callback_data=text.split(" ")[1].lower()) for text in row]
        for row in zodiac_buttons
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🌟 Select your Zodiac Sign:", reply_markup=markup)

# button click
async def handle_zodiac_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    sign = query.data
    result = fetch_horoscope(sign)
    await query.edit_message_text(text=result, parse_mode="Markdown")

# Main
if __name__ == "__main__":
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("tithi", tithi))
    app.add_handler(CommandHandler("birthdata", custom_panchang))
    app.add_handler(CommandHandler("marriage", custom_panchang))
    app.add_handler(CommandHandler("horoscope", horoscope))
    app.add_handler(CallbackQueryHandler(handle_zodiac_click))

    print("🤖 Bot is running...")
    app.run_polling()
