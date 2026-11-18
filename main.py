import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")
LOGO_URL = "https://files.catbox.moe/n24jew.jpg"

TOTAL_SUPPLY = 50000
AIRDROP_TOTAL = 15000
CLAIM_AMOUNT = 10
MAX_USERS = 1500

claimed_users = {}
total_claimed = 0

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎁 Claim 10 VLM", callback_data="claim")],
        [InlineKeyboardButton("💰 My Balance", callback_data="balance")],
        [InlineKeyboardButton("📊 Airdrop Status", callback_data="status")],
    ]
    text = (
        "💜 *Welcome to VELMI!* 💜\n\n"
        "Official Community Token on TON\n\n"
        f"Total Supply: {TOTAL_SUPPLY} VLM\n"
        f"Airdrop: {AIRDROP_TOTAL} VLM for the first {MAX_USERS} members\n"
        f"Reward per user: *{CLAIM_AMOUNT} VLM*\n\n"
        "Tap Claim below to start 👇"
    )
    await update.message.reply_photo(photo=LOGO_URL, caption=text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    username = query.from_user.username or query.from_user.first_name
    global total_claimed

    if query.data == "claim":
        if user_id in claimed_users:
            await query.message.reply_text("❌ You have already claimed your 10 VLM!")
            return
        if total_claimed >= AIRDROP_TOTAL:
            await query.message.reply_text("😢 Airdrop is over!")
            return
        claimed_users[user_id] = CLAIM_AMOUNT
        total_claimed += CLAIM_AMOUNT
        await query.message.reply_text(f"✅ *Congratulations!* 🎉\n\nYou received *{CLAIM_AMOUNT} VLM*\nUsername: @{username}\n\nPlease send your Tonkeeper Wallet Address here to receive it.", parse_mode="Markdown")
    elif query.data == "balance":
        bal = claimed_users.get(user_id, 0)
        await query.message.reply_text(f"💰 Your Balance: *{bal} VLM*", parse_mode="Markdown")
    elif query.data == "status":
        remaining = AIRDROP_TOTAL - total_claimed
        await query.message.reply_text(f"📊 *Airdrop Status*\n\nDistributed: {total_claimed} VLM\nRemaining: {remaining} VLM\nClaimed Users: {len(claimed_users)} / {MAX_USERS}", parse_mode="Markdown")

async def wallet_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"✅ Wallet Address Received: `{update.message.text}`\n\nYour 10 VLM will be sent soon! Thank you for joining VELMI 💜", parse_mode="Markdown")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("claim", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, wallet_handler))
    print("VELMI Bot is running...")
    app.run_polling()
