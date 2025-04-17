from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

TOKEN = "7878360475:AAGRpyLWxPTwB8W65Gze6yiRRtfIonw0Q2s"

GENDER, AGE = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [['Мужской', 'Женский']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Привет! Я твой личный диетолог. Укажи свой пол:", reply_markup=reply_markup)
    return GENDER

async def gender(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['gender'] = update.message.text
    await update.message.reply_text("Укажи, пожалуйста, свой возраст:")
    return AGE

async def age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['age'] = update.message.text

    gender_raw = context.user_data.get('gender')
    age_text = context.user_data.get('age')

    # Преобразуем пол
    gender = "мужчина" if gender_raw == "Мужской" else "женщина"

    # Склонение "год"
    def age_suffix(age):
        age = int(age)
        if 11 <= age % 100 <= 14:
            return "лет"
        elif age % 10 == 1:
            return "год"
        elif 2 <= age % 10 <= 4:
            return "года"
        else:
            return "лет"

    suffix = age_suffix(int(age_text))

    await update.message.reply_text(
        f"Ты {gender}, {age_text} {suffix}.\nСкоро продолжим!"
    )
    return ConversationHandler.END

app = ApplicationBuilder().token(TOKEN).build()

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        GENDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, gender)],
        AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, age)],
    },
    fallbacks=[]
)

app.add_handler(conv_handler)
print("Бот запущен")
app.run_polling()
