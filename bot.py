import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler

TOKEN = "7878360475:AAGRpyLWxPTwB8W65Gze6yiRRtfIonw0Q2s"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Этапы диалога
NAME, GENDER, AGE, HEIGHT, WEIGHT, ACTIVITY, GOAL = range(7)

# Ответы для кнопок
gender_keyboard = [['Мужчина', 'Женщина']]
activity_keyboard = [['Минимальная', 'Низкая'], ['Средняя', 'Высокая', 'Очень высокая']]
goal_keyboard = [['Похудение', 'Поддержание', 'Набор веса']]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я твой личный диетолог. Давай подберём тебе питание. Как тебя зовут?")
    return NAME

async def name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['name'] = update.message.text
    await update.message.reply_text("Укажи свой пол:", reply_markup=ReplyKeyboardMarkup(gender_keyboard, one_time_keyboard=True, resize_keyboard=True))
    return GENDER

async def gender(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['gender'] = update.message.text
    await update.message.reply_text("Сколько тебе лет?")
    return AGE

async def age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['age'] = int(update.message.text)
    await update.message.reply_text("Укажи свой рост в см:")
    return HEIGHT

async def height(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['height'] = int(update.message.text)
    await update.message.reply_text("Укажи свой вес в кг:")
    return WEIGHT

async def weight(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['weight'] = float(update.message.text)
    await update.message.reply_text("Какой у тебя уровень активности?", reply_markup=ReplyKeyboardMarkup(activity_keyboard, one_time_keyboard=True, resize_keyboard=True))
    return ACTIVITY

async def activity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['activity'] = update.message.text
    await update.message.reply_text("Какова твоя цель?", reply_markup=ReplyKeyboardMarkup(goal_keyboard, one_time_keyboard=True, resize_keyboard=True))
    return GOAL

async def goal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['goal'] = update.message.text
    user = context.user_data

    # Расчёт КБЖУ
    gender_coef = 5 if user['gender'] == 'Мужчина' else -161
    bmr = 10 * user['weight'] + 6.25 * user['height'] - 5 * user['age'] + gender_coef

    activity_levels = {
        'Минимальная': 1.2,
        'Низкая': 1.375,
        'Средняя': 1.55,
        'Высокая': 1.725,
        'Очень высокая': 1.9
    }

    total_calories = bmr * activity_levels[user['activity']]

    if user['goal'] == 'Похудение':
        total_calories -= 300
    elif user['goal'] == 'Набор веса':
        total_calories += 300

    # Белки, жиры, углеводы (стандартное соотношение)
    proteins = round((total_calories * 0.3) / 4)
    fats = round((total_calories * 0.25) / 9)
    carbs = round((total_calories * 0.45) / 4)

    await update.message.reply_text(
        f"{user['name']}, ты {user['gender'].lower()}, {user['age']} лет.\n"
        f"Твоя цель: {user['goal'].lower()}.\n"
        f"Рассчитанная суточная норма:\n"
        f"🔸 Калории: {int(total_calories)} ккал\n"
        f"🔸 Белки: {proteins} г\n"
        f"🔸 Жиры: {fats} г\n"
        f"🔸 Углеводы: {carbs} г\n\n"
        f"Скоро сможешь получить полноценное меню!"
    )
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, name)],
            GENDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, gender)],
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, age)],
            HEIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, height)],
            WEIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, weight)],
            ACTIVITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, activity)],
            GOAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, goal)],
        },
        fallbacks=[]
    )

    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == '__main__':
    main()
