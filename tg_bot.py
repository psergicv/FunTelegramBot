import random
import json
from config import token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.utils import executor

bot = Bot(token=token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_bot(message: types.Message):
    buttons = ["more"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)

    await message.answer("Fun Collection", reply_markup=keyboard)


@dp.message_handler(Text(equals="more"))
async def get_anekdot(message: types.Message):
    with open("anekdot_db.json", encoding='utf-8') as file:
        anekdot_text = json.load(file)

    total_anekdots_number = len(anekdot_text)
    anekdot_number = random.randrange(1, total_anekdots_number + 1)
    anek_id = random.randrange(1, 21)
    for k in anekdot_text.keys():
        if int(k) == anekdot_number:
            for v in anekdot_text[k].keys():
                if int(v) == anek_id:
                    for v1 in anekdot_text[k][v].values():
                        await message.answer(v1)


if __name__ == '__main__':
    executor.start_polling(dp)
