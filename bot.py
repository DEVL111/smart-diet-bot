from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Храним временные данные пользователя
user_data = {}

# === КНОПКИ ГЛАВНОГО МЕНЮ ===
main_menu_keyboard = [
    ['🧮 Рассчитать КБЖУ и меню'],
    ['📷 Проверить продукт по фото'],
    ['⚙️ Настройки', 'ℹ️ О боте']
]
main_menu_markup = ReplyKeyboardMarkup(main_menu_keyboard, resize_keyboard=True)

# === СТАРТ ===
def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_text(
        f"👋 Привет, {user.first_name}! Я — твой личный диетолог.\n\n"
        "Выбери, что хочешь сделать:",
        reply_markup=main_menu_markup
    )

# === МЕНЮ ===
def handle_menu(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    chat_id = update.message.chat_id

    if text == '🧮 Рассчитать КБЖУ и меню':
        user_data[chat_id] = {}
        update.message.reply_text("Как тебя зовут?", reply_markup=ReplyKeyboardRemove())

        # Устанавливаем следующий шаг — имя
        context.user_data['step'] = 'name'

    elif text == '📷 Проверить продукт по фото':
        update.message.reply_text("Отправь фото продукта или его состава.")

    elif text == '⚙️ Настройки':
        update.message.reply_text("Раздел в разработке. Скоро будет доступен.")

    elif text == 'ℹ️ О боте':
        update.message.reply_text(
            "🤖 Я — умный диетолог. Рассчитываю КБЖУ, составляю меню, анализирую продукты. "
            "Работаю на научной основе. В разработке 💪"
        )

# === ОБРАБОТКА СООБЩЕНИЙ ПОШАГОВО ===
def handle_text(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    text = update.message.text
    step = context.user_data.get('step')

    if step == 'name':
        user_data[chat_id]['name'] = text
        update.message.reply_text("Укажи свой пол:", reply_markup=ReplyKeyboardMarkup([['Мужчина', 'Женщина']], resize_keyboard=True))
        context.user_data['step'] = 'gender'

    elif step == 'gender':
        user_data[chat_id]['gender'] = text
        update.message.reply_text("Сколько тебе лет?")
        context.user_data['step'] = 'age'

    elif step == 'age':
        if not text.isdigit():
            update.message.reply_text("Пожалуйста, введи число.")
            return
        user_data[chat_id]['age'] = int(text)
        name = user_data[chat_id]['name']
        gender = user_data[chat_id]['gender']
        age = user_data[chat_id]['age']

        gender_word = "мужчина" if gender == "Мужчина" else "женщина"
        age_word = f"{age} лет" if 11 <= age % 100 <= 19 else (
            f"{age} год" if age % 10 == 1 else (
                f"{age} года" if 2 <= age % 10 <= 4 else f"{age} лет"
            )
        )

        update.message.reply_text(
            f"Отлично, {name}! Ты — {gender_word}, {age_word}.\nСкоро продолжим расчёт.",
            reply_markup=main_menu_markup
        )
        context.user_data.clear()

# === ЗАПУСК БОТА ===
def main():
    updater = Updater("7878360475:AAGRpyLWxPTwB8W65Gze6yiRRtfIonw0Q2s", use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_menu))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
