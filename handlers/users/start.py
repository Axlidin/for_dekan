from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram import types
from keyboards.default.menu import menu
from loader import dp

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    if message.from_user.id == 742648323:
        await message.answer("Xush kelibsiz, <b>Dadabayev Sardorbek Usmanovich</b>")
    else:
        await message.answer(f"Assalomu alaykum, {message.from_user.get_mention()}\n"
                         "<b>Men Andijon davlat universiteti Axborot texnologiyalari va kompyuter "
                             "injiniringi fakulteti dekani Dadabayev Sardorbek Usmanovich.</b> "
                             "Fakultetni har tomonlama rivojlantirish rasmiy botiga xush kelibsiz!\n"
                         "xabar yozish uchun 👇  tugamani bosing", reply_markup=menu)