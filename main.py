import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    ContextTypes
)
from datetime import datetime, date
from panchang import fetch_panchang_data
from horoscope import fetch_horoscope
from config import BOT_TOKEN  # Or use os.environ.get("BOT_TOKEN") for Render

logging.basicConfig(level=logging.INFO)

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌟 Welcome to AstroBot!\n\n"
        "Use /tithi to get today’s Panchang\n"
        "Use /horoscope to view your Zodiac prediction\n"
        "Use /birthdata ddmmyyyy or /marriage ddmmyyyy to view Panchang on special dates"
    )

# /tithi command
async def tithi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    today = date.today().isoformat()
    result = fetch_panchang_data(today)
    await update.message.reply_text(f"📆 Today’s Panchang:\n{result}")

# /birthdata or /marriage
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
                f"⚠️ *Invalid date format!*\n"
                f"Use this format:\n\n"
                f"`{cmd} 14022024`\n"
                f"_That's DDMMYYYY (e.g., 14 Feb 2024)_",
                parse_mode="Markdown"
            )
    else:
        cmd = update.message.text.split()[0]
        await update.message.reply_text(
            f"⚠️ *Date missing!*\n"
            f"Use this format:\n\n"
            f"`{cmd} 14022024`\n"
            f"_That's DDMMYYYY (e.g., 14 Feb 2024)_",
            parse_mode="Markdown"
        )

# /horoscope buttons
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

# Zodiac sign handler
async def handle_zodiac_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    sign = query.data
    result = fetch_horoscope(sign)
    await query.edit_message_text(text=result, parse_mode="Markdown")

# Main bot execution
if __name__ == "__main__":
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("tithi", tithi))
    application.add_handler(CommandHandler("birthdata", custom_panchang))
    application.add_handler(CommandHandler("marriage", custom_panchang))
    application.add_handler(CommandHandler("horoscope", horoscope))
    application.add_handler(CallbackQueryHandler(handle_zodiac_click))

    print("🤖 Bot is running...")
    application.run_polling()
