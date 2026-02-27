import os
import asyncio
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ================== CONFIG ==================
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("TOKEN not found! Add it in Render Environment Variables.")

ADMIN_ID = 7488582600

FINAL_LINK = "https://t.me/+B0UIZVSPyrdmMDM1"
VIP_LINK = "https://t.me/+Up_UvxioMutiNDA1"

VIDEO_FILE_ID_1 = "BAACAgUAAxkBAAIDWmmgsckJdGr_PPWk5r_qySVaSU5OAAIwGgACzCoIVYf4fspEue9JOgQ"
VIDEO_FILE_ID_2 = "BAACAgUAAxkBAAIDW2mgscmJZMg5AqPnN9glqZGw0uLuAAIxGgACzCoIVfb_lYtaWUmMOgQ"
# ============================================


# ================== START ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        msg1 = await update.message.reply_video(video=VIDEO_FILE_ID_1)
        msg2 = await update.message.reply_video(video=VIDEO_FILE_ID_2)

        # Auto delete after 30 seconds
        async def delete_videos():
            await asyncio.sleep(30)
            try:
                await msg1.delete()
                await msg2.delete()
            except:
                pass

        asyncio.create_task(delete_videos())

        keyboard = [
            ["🚀 Get More Videos💦"],
            ["💎 Become A VIP (No Ads)"],
            ["📜 Terms and Conditions"]
        ]

        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

        await update.message.reply_text(
            "👋 Welcome to our Official Viral Videos Bot!💦\n\nChoose an option below:",
            reply_markup=reply_markup
        )

    except Exception as e:
        print("Start Error:", e)


# ================== TEXT ==================
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🚀 Get More Videos💦":
        keyboard = [[InlineKeyboardButton("Get Viral Video💦", callback_data="get_access")]]
        await update.message.reply_text(
            "Click below to Claim More Than 500+ Videos💦:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif text == "💎 Become A VIP (No Ads)":
        await update.message.reply_text(
            "💎 VIP ACCESS REQUIREMENT\n\n"
            "Complete the task and send screenshot for approval."
        )

    elif text == "📜 Terms and Conditions":
        await update.message.reply_text(
            "📜 Terms & Conditions\n\n"
            "1️⃣ Complete verification honestly.\n"
            "2️⃣ No cheating allowed.\n"
            "3️⃣ Admin decision is final."
        )


# ================== INLINE ==================
async def inline_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "get_access":
        await query.message.reply_text(
            "📌 Instructions:\n\n"
            "1️⃣ Download app\n"
            "2️⃣ Login\n"
            "3️⃣ Send screenshot for approval."
        )


# ================== SCREENSHOT ==================
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user

    keyboard = [
        [
            InlineKeyboardButton("Approve", callback_data=f"approve_{user.id}"),
            InlineKeyboardButton("Reject", callback_data=f"reject_{user.id}")
        ]
    ]

    await context.bot.forward_message(
        chat_id=ADMIN_ID,
        from_chat_id=update.message.chat_id,
        message_id=update.message.message_id
    )

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"New screenshot from {user.id}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    await update.message.reply_text("⏳ Waiting for admin approval.")


# ================== ADMIN ==================
async def admin_decision(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = int(query.data.split("_")[1])

    if query.data.startswith("approve"):
        keyboard = [
            [InlineKeyboardButton("Open Normal Access", url=FINAL_LINK)],
            [InlineKeyboardButton("Open VIP Access", url=VIP_LINK)]
        ]

        await context.bot.send_message(
            chat_id=user_id,
            text="✅ Approved! You now have access.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data.startswith("reject"):
        await context.bot.send_message(
            chat_id=user_id,
            text="❌ Verification Failed. Try again."
        )


# ================== MAIN ==================
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    app.add_handler(CallbackQueryHandler(inline_handler, pattern="get_access"))
    app.add_handler(CallbackQueryHandler(admin_decision, pattern="^(approve|reject)_"))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
