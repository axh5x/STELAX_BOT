https://api.telegram.org/bot%3C8091248340:AAHsjE9yFtUY8NwmaQ0i7vYUXak_DLoUDts%3E/setWebhook?url=https://stelax-bot-n2rp.onrender.com%2Fwebhook%2F%3C8091248340:AAHsjE9yFtUY8NwmaQ0i7vYUXak_DLoUDts%3E
import logging, random, datetime
from hijri_converter import convert
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters
)
import os

# إعدادات
TOKEN = "8091248340:AAHsjE9yFtUY8NwmaQ0i7vYUXak_DLoUDts"
ADMIN_ID = 5014554262  # ضع معرفك
bot_active = True
blocked_users = set()  # قائمة الحظر
users_data = {}  # هنا نخزن بيانات المستخدمين

# تفعيل اللوج
logging.basicConfig(level=logging.INFO)

# الاستفتاحيات
OPENINGS = [
    "📩 رسالة جديدة قد وصلت للتو… ✨",
    "✭ من بين ضجيج العالم وهدوء الكون ، وصلت إليك رسالة الآن 📨…",
    "✭ رسالة أخرى قادمة ، لنرى محتواها 💬.."
]

# النهايات
CLOSINGS = [
    "⊛ كل رسالة قد تكون بداية فكرة… أو نهاية حكاية 🎬 .",
    "⊛ ربما الرسائل تحمل بين كلماتها معانٍ ، لايمكن التعبير عنها✨.",
    "⊛ في كل نص، سرّ صغير ينتظر أن يُكتشف🕯️."
]

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "مرحباً بك في 📨 𝐒𝐓𝐄𝐋𝐀𝐗 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 ، يمكنك التواصل معنا ورؤية 𝐒𝐓𝐄𝐋𝐀𝐗 أقرب من أي وقتٍ مضى، ماذا تنتظر؟ أرسل رسالتك أو مصارحتك نحن بانتظارك 📩 ."
    )

# استقبال الرسائل
async def receive_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global bot_active, blocked_users, users_data
    user = update.message.from_user
    text = update.message.text

    # نخزن بيانات المرسل
    users_data[user.id] = user.username

    if not bot_active:
        return await update.message.reply_text("عذراً البوت متوقف حالياً أو تحت التطوير، حاول لاحقاً ⏸️. ")

    if user.id in blocked_users:
        return await update.message.reply_text("🚫 لا يمكنك إرسال رسائل لهذا البوت.")

    now = datetime.datetime.now()
    date_greg = now.strftime("%Y-%m-%d")
    hijri = convert.Gregorian(now.year, now.month, now.day).to_hijri()
    date_hijri = f"{hijri.year}-{hijri.month:02d}-{hijri.day:02d}"
    time_str = now.strftime("%I:%M")
    am_pm = "صباحاً" if now.strftime("%p") == "AM" else "مساءً"

    opening = random.choice(OPENINGS)
    closing = random.choice(CLOSINGS)

    formatted_msg = f"""
𝐅𝐑𝐎𝐌: <a href="https://t.me/stelax_cntc_bot?start=chat">𝐒𝐓𝐄𝐋𝐀𝐗 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 📨 •</a>
━━━━━━━━━━━━━━━
{opening}
━━━━━━━━━━━━━━━
🗓️ التاريخ: {date_greg}م
🌙: {date_hijri}هـ
⏰ الوقت: {time_str} {am_pm}

✉️ المحتوى:
❜{text}❛
━━━━━━━━━━━━━━━
{closing}
"""

    keyboard = [
        [
            InlineKeyboardButton("👤 المرسل", callback_data=f"user_{user.id}"),
            InlineKeyboardButton("🚫 حظر", callback_data=f"block_{user.id}")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=formatted_msg,
        reply_markup=reply_markup,
        parse_mode="HTML"
    )

    await update.message.reply_text(
        "تم استلام رسالتك بنجاح، شكراً لمراسلتك! سنقوم بالرد عليك فور قراءتها 🔖"
    )

# لوحة التحكم /panel
async def panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return await update.message.reply_text("🚫 غير مسموح لك بالدخول هنا.")

    keyboard = [
        [InlineKeyboardButton("▶️ تشغيل", callback_data="start"),
         InlineKeyboardButton("⏸️ إيقاف", callback_data="stop")],
        [InlineKeyboardButton("ℹ️ الحالة", callback_data="status")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("⚙️ لوحة التحكم:", reply_markup=reply_markup)

# التعامل مع الأزرار
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global bot_active, blocked_users, users_data
    query = update.callback_query
    await query.answer()

    if query.data == "start":
        bot_active = True
        await query.edit_message_text("✅ تم تشغيل البوت.")
    elif query.data == "stop":
        bot_active = False
        await query.edit_message_text("⏸️ تم إيقاف البوت.")
    elif query.data == "status":
        status = "🟢 يعمل" if bot_active else "🔴 متوقف"
        await query.edit_message_text(f"ℹ️ حالة البوت: {status}")

    elif query.data.startswith("user_"):
        user_id = int(query.data.split("_")[1])
        username = users_data.get(user_id, "لا يوجد")
        if username:
            await query.message.reply_text(f"👤 معرف المرسل: {user_id}\n📛 اسم المستخدم: @{username}")
        else:
            await query.message.reply_text(f"👤 معرف المرسل: {user_id}\n📛 اسم المستخدم: لا يوجد")

    elif query.data.startswith("block_"):
        user_id = int(query.data.split("_")[1])
        blocked_users.add(user_id)
        await query.message.reply_text(f"🚫 تم حظر المرسل (ID: {user_id}).")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("panel", panel))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_message))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🤖 البوت يعمل...")
    app.run_polling()

if __name__ == "__main__":
    main()
