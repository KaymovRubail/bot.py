from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Update, CallbackQuery


async def menu_buttons_for_admin(var1,var2):
    markup = ReplyKeyboardMarkup()
    first=KeyboardButton(var1,callback_data=var1)
    second=KeyboardButton(var2,callback_data=var2)
    markup.add(first,second)
    return markup
async def menu_buttons_for_admin2(var1):
    markup = ReplyKeyboardMarkup()
    first=KeyboardButton(var1,callback_data=var1)
    markup.add(first)
    return markup