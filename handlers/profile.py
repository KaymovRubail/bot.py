from tkinter import Image
import sqlite3
from aiogram import types, Dispatcher
from aiogram.types import Update
from random import choice
from database import ddbb
from config import bot,mediaa
from const import FirstCaption,Userinfo
from keyboardbuttons import buttons
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

async def my_profile(call: types.CallbackQuery):
    data=ddbb.Database()
    prof=data.select_info_registr_table(tg_id=call.from_user.id)
    if prof:
        with open(prof[-1],'rb') as photo:
            await bot.send_photo(
                chat_id=call.from_user.id,
                photo=photo,
                caption=Userinfo.format(
                    name=prof[1],
                    bio=prof[2],
                    age=prof[3],
                    z=prof[4],
                    gender=prof[5],
                    bestcolor=prof[6]
                )
            )
    else:
        await bot.send_message(
            chat_id=call.from_user.id,
            text='U havnt registered yet'
        )

async def view_random_profile(call: types.CallbackQuery):
    data=ddbb.Database()
    prof=data.select_all_registr(tg_id=call.from_user.id)
    if prof:
        rand=choice(prof)[:9]
        with open(rand[-1],'rb') as photo:
            await bot.send_photo(
                chat_id=call.from_user.id,
                photo=photo,
                caption=Userinfo.format(
                    name=rand[2],
                    bio=rand[3],
                    age=rand[4],
                    z=rand[5],
                    gender=rand[6],
                    bestcolor=rand[7]
                ),
                reply_markup= await buttons.like_dislike(rand[1])
            )
    else:
        await bot.send_message(
            chat_id=call.from_user.id, text='U have already liked all profiles'
        )
async def like_dislike_management(call: types.CallbackQuery):
    data=ddbb.Database()
    calldata=call.data.split("_")
    try:
        data.insert_like_dislike_table(
            user=calldata[1],
            liker=call.from_user.id,
            what=calldata[0]
        )
    except sqlite3.IntegrityError:
        await bot.send_message(
            chat_id=call.from_user.id,
            text="U have already valued this profile"
        )
    finally:
        await call.message.delete()
        await view_random_profile(call=call)
async def del_profile(call: types.CallbackQuery):
    data=ddbb.Database()
    ids=data.select_id_info(
        tg=call.from_user.id
    )
    if ids:
        data.delete_info_registr_table(
            tg_id=call.from_user.id
        )
        await bot.send_message(
            chat_id=call.from_user.id,
            text='U have deleted ur profile'
        )
    else:
        await bot.send_message(
            chat_id=call.from_user.id,
            text='U dont have profile'
        )
def registr_edit_profile(dp: Dispatcher):
    dp.register_callback_query_handler(my_profile, lambda call:call.data=='mypo')
    dp.register_callback_query_handler(del_profile, lambda call:call.data=='delete')
    dp.register_callback_query_handler(view_random_profile, lambda call:call.data=='view')
    dp.register_callback_query_handler(like_dislike_management, lambda call: 'Like' in call.data)
    dp.register_callback_query_handler(like_dislike_management, lambda call: 'Dis' in call.data)