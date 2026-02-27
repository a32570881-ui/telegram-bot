import os
import asyncio
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# ================== CONFIG ==================
TOKEN = os.getenv("TOKEN")

ADMIN_ID = 7488582600
SECOND_ID = 1930422156

FINAL_LINK = "https://t.me/+B0UIZVSPyrdmMDM1"
VIP_LINK = "https://t.me/+Up_UvxioMutiNDA1"

VIDEO_FILE_ID_1 = "BAACAgUAAxkBAAIDWmmgsckJdGr_PPWk5r_qySVaSU5OAAIwGgACzCoIVYf4fspEue9JOgQ"
VIDEO_FILE_ID_2 = "BAACAgUAAxkBAAIDW2mgscmJZMg5AqPnN9glqZGw0uLuAAIxGgACzCoIVfb_lYtaWUmMOgQ"
# ============================================


# ================== START ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # ⚡ Instant send using file_id
    msg1 = await update.message.reply_video(video=VIDEO_FILE_ID_1)
    msg2 = await update.message.reply_video(video=VIDEO_FILE_ID_2)

    # ⏳ Auto delete after 2 minutes
    async def delete_videos():
        await asyncio.sleep(30)
        try:
            await msg1.delete()
            await msg2.delete()
        except:
            pass

    context.application.create_task(delete_videos())

    await asyncio.sleep(1)

    keyboard = [
        ["🚀 Get More Videos💦"],
        ["💎 Become A VIP (No Ads)"],
        ["📜 Terms and Conditions"]
    ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )

    await update.message.reply_text(
        "👋 Welcome to our Official Viral Videos Bot!💦\n\nChoose an option below:",
        reply_markup=reply_markup
    )


# ================== TEXT HANDLER ==================
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🚀 Get More Videos💦":
        keyboard = [[InlineKeyboardButton("Get Viral Video💦", callback_data="get_access")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "Click below to Claim More Than 500+ Videos💦:",
            reply_markup=reply_markup
        )

    elif text == "💎 Become A VIP (No Ads)":
        await update.message.reply_text(
            "💎 VIP ACCESS REQUIREMENT\n\n"
            "To unlock VIP membership, you must first complete a Task To Help The Admin.\n\n"
            "1️⃣ Click 'Start'\n"
            "2️⃣ Follow instructions\n"
            "3️⃣ Send screenshot for approval\n\n"
            "After approval, you will receive both Normal and VIP access links."
        )

    elif text == "📜 Terms and Conditions":
        await update.message.reply_text(
            "📜 Terms & Conditions\n\n"
            "1️⃣ Complete verification honestly.\n"
            "2️⃣ Any cheating attempt will be rejected.\n"
            "3️⃣ Access links are personal.\n"
            "4️⃣ Admin decision is final."
        )


# ================== INLINE ==================
async def inline_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "get_access":
        await query.message.reply_text(
            "📌 Instructions:\n\n"
            "1️⃣ Download FlixFox app:\n"
            "https://filmm.me/SyfNVrge\n\n"
            "2️⃣ Login into the app.\n"
            "3️⃣ Take screenshot with login timing visible.\n"
            "4️⃣ Send screenshot here for verification.\n"
            "PLEASE DO THE PROCESS (SUPPORT THE ADMIN....)"
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
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.forward_message(
        chat_id=ADMIN_ID,
        from_chat_id=update.message.chat_id,
        message_id=update.message.message_id
    )

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"New screenshot from @{user.username} (ID: {user.id})",
        reply_markup=reply_markup
    )

    await update.message.reply_text(
        "⏳ Waiting for admin approval.\n\nPlease wait patiently."
    )


# ================== ADMIN ==================
async def admin_decision(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    user_id = int(data.split("_")[1])

    if "approve" in data:
        keyboard = [
            [InlineKeyboardButton("Open Normal Access", url=FINAL_LINK)],
            [InlineKeyboardButton("Open VIP Access", url=VIP_LINK)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await context.bot.send_message(
            chat_id=user_id,
            text="✅ Verification Approved!\n\nYou now have access to both channels.",
            reply_markup=reply_markup
        )

    elif "reject" in data:
        await context.bot.send_message(
            chat_id=user_id,
            text="❌ Verification Failed.\n\n"
                 "You are trying to cheat or you are a pre-existing user.\n"
                 "Please try again using another device."
        )


# ================== MAIN ==================
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    app.add_handler(CallbackQueryHandler(inline_handler, pattern="get_access"))
    app.add_handler(CallbackQueryHandler(admin_decision, pattern="^(approve|reject)_"))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    print("Bot is running...")

    import asyncio
    asyncio.run(app.run_polling())


if __name__ == "__main__":
    main()
