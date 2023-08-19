import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode

API_TOKEN = '6446989431:AAFUgeJoHmL57QiknLMTVDfFDS6zicoERTY'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


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


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    global відповіді
    відповіді[message.chat.id] = []
    await message.reply("Привіт! Давайте з'ясуємо, який бізнес вам підходить. Відповідайте на кілька запитань.")
    await ask_question(0, message.chat.id)


async def ask_question(номер_питання, chat_id):
    розмітка = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    варіанти_список = варіанти[номер_питання]
    for варіант in варіанти_список:
        розмітка.add(варіант)
    await bot.send_message(chat_id, питання[номер_питання], reply_markup=розмітка)


@dp.message_handler(lambda message: message.text in варіанти[0], state=None)
async def answer_question_1(message: types.Message):
    відповіді[message.chat.id].append(message.text)
    await ask_question(1, message.chat.id)


@dp.message_handler(lambda message: message.text in варіанти[1], state=None)
async def answer_question_2(message: types.Message):
    відповіді[message.chat.id].append(message.text)
    await ask_question(2, message.chat.id)


@dp.message_handler(lambda message: message.text in варіанти[2], state=None)
async def answer_question_3(message: types.Message):
    відповіді[message.chat.id].append(message.text)
    # Реалізуйте вашу логіку рекомендацій тут
    рекомендація = отримати_рекомендацію(відповіді[message.chat.id])
    await bot.send_message(message.chat.id, f"На основі ваших відповідей, рекомендуємо бізнес: {рекомендація}")
    del відповіді[message.chat.id]


def отримати_рекомендацію(відповіді):
    if відповіді[0] == "Спорт" and відповіді[1] == "Торгівля":
        return "Магазин спортивних товарів"
    elif відповіді[0] == "Малювання" and відповіді[1] == "Технології":
        return "Графічний дизайн та ілюстрації для технологічних компаній"
    # Додайте інші умови для інших варіантів відповідей
    return "Немає конкретної рекомендації"


if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
