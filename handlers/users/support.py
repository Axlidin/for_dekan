import logging
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from keyboards.inline.support import support_keyboard, support_callback
from loader import dp, bot

@dp.message_handler(state='*', commands='Bekor_qilish')
@dp.message_handler(Text(equals='Bekor_qilish', ignore_case=True), state='*')
async def cancel_handler2(message: types.Message, state: FSMContext):
    """
    Foydalanuvchiga har qanday harakatni bekor qilishga ruxsat bering
    """
    current_state = await state.get_state()
    if current_state is None:
        return
    logging.info('Cancelling state %r', current_state)
    await state.finish()
    await message.reply('Bekor qilndi.')

@dp.message_handler(text="Xabar yozish")
async def ask_support(message: types.Message):
    text = "<b>Xabar yubormoqchimisiz? Quyidagi tugmani bosing!</b>"
    keyboard = await support_keyboard(messages="one")
    await message.answer(text, reply_markup=keyboard)

@dp.callback_query_handler(support_callback.filter(messages="one"))
async def send_to_support(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await call.answer()
    user_id = int(callback_data.get("user_id"))
    await call.message.answer("Xabar kiriting va yuboring"
                              "<b>\nAks xolda bo'lsa /Bekor_qilish bosing</b>")
    await state.set_state("wait_for_support_message")
    await state.update_data(second_id=user_id, )
    await state.update_data(mention=call.from_user.get_mention(as_html=True))

@dp.message_handler(state="wait_for_support_message", content_types=types.ContentTypes.ANY)
async def get_support_message(message: types.Message, state: FSMContext):
    data = await state.get_data()
    mention = data.get("mention")
    second_id = data.get("second_id")
    if message.from_user.id == 742648323:
        await bot.send_message(second_id,
                               f"<b>Dadabayev Sardorbek Usmanovich</b> sizga xabar yubordi! Quyidagi tugmani bosish orqali xabarga javob berishingiz mumkin.")
    else:
        await bot.send_message(second_id,
                               f"{mention} sizga xabar yubordi! Quyidagi tugmani bosish orqali xabarga javob berishingiz mumkin.")
    keyboard = await support_keyboard(messages="one", user_id=message.from_user.id)
    await message.copy_to(second_id, reply_markup=keyboard)
    await message.answer("Sizning xabaringiz yuborildi!")
    await state.reset_state()
