import logging
import telebot


API_TOKEN = '6446989431:AAFUgeJoHmL57QiknLMTVDfFDS6zicoERTY'

bot = telebot.TeleBot(API_TOKEN)

питання = [
    "Яке ваше хобі?",
    "Який тип діяльності вас цікавить?",
    "Який рівень досвіду у вас є?",
]

варіанти = [
    ["Спорт", "Малювання", "Музика"],
    ["Торгівля", "Технології", "Послуги"],
    ["Початківець", "Середній", "Досвідчений"],
]

відповіді = {}


@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    відповіді[chat_id] = []
    bot.send_message(
        chat_id, "Привіт! Давайте визначимо, який бізнес вам підходить. Відповідайте на декілька питань.")
    задати_питання(0, chat_id)


def задати_питання(номер_питання, chat_id):
    розмітка = telebot.types.ReplyKeyboardMarkup(
        resize_keyboard=True, selective=True)
    варіанти_список = варіанти[номер_питання]
    for варіант in варіанти_список:
        розмітка.add(варіант)
    bot.send_message(chat_id, питання[номер_питання], reply_markup=розмітка)


@bot.message_handler(func=lambda message: message.text in варіанти[0])
def відповісти_на_питання_1(message):
    chat_id = message.chat.id
    відповіді[chat_id].append(message.text)
    задати_питання(1, chat_id)


@bot.message_handler(func=lambda message: message.text in варіанти[1])
def відповісти_на_питання_2(message):
    chat_id = message.chat.id
    відповіді[chat_id].append(message.text)
    задати_питання(2, chat_id)


@bot.message_handler(func=lambda message: message.text in варіанти[2])
def відповісти_на_питання_3(message):
    chat_id = message.chat.id
    відповіді[chat_id].append(message.text)
    рекомендація = отримати_рекомендацію(відповіді[chat_id])
    bot.send_message(
        chat_id, f"На основі ваших відповідей рекомендуємо бізнес: {рекомендація}")
    del відповіді[chat_id]


def отримати_рекомендацію(відповіді):
    if відповіді[0] == "Спорт" and відповіді[1] == "Торгівля":
        return "Магазин спортивних товарів"
    elif відповіді[0] == "Малювання" and відповіді[1] == "Технології":
        return "Графічний дизайн та ілюстрації для технологічних компаній"
    # Додайте інші умови для інших рекомендацій
    return "Немає конкретної рекомендації"


if __name__ == '__main__':
    bot.polling()
