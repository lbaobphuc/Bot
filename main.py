from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import urllib.parse

BOT_TOKEN = '8055106598:AAEWKlquZsNGrA2mKiPZ7yjqSO_9smuSNsU'

# Danh sách nhóm cần kiểm tra
REQUIRED_GROUPS = ['@shenktol']

# Lưu dữ liệu ref tạm (nên dùng DB thực tế)
ref_data = {}

async def is_user_in_required_groups(user_id, bot):
    for group in REQUIRED_GROUPS:
        try:
            member = await bot.get_chat_member(group, user_id)
            if member.status in ['left', 'kicked']:
                return False
        except:
            return False
    return True

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    args = context.args

    # Ghi người giới thiệu
    if args:
        referrer_id = args[0]
        if referrer_id != str(user_id):
            ref_data[user_id] = referrer_id

    # Kiểm tra tham gia nhóm
    if await is_user_in_required_groups(user_id, context.bot):
        await update.message.reply_text("✅ Bạn đã tham gia đủ nhóm. Chào mừng!")
    else:
        await update.message.reply_text(
            "❌ Bạn chưa tham gia đủ nhóm yêu cầu.\n"
            + "\n".join([f"- {group}" for group in REQUIRED_GROUPS])
        )

async def ref(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    encoded_ref = urllib.parse.quote(str(user_id))
    bot_username = context.bot.username
    ref_link = f"https://t.me/{bot_username}?start={encoded_ref}"
    await update.message.reply_text(f"🔗 Link mời của bạn:\n{ref_link}")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("ref", ref))
app.run_polling()
