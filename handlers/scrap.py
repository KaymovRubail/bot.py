from aiogram import types, Dispatcher
from config import bot,admin
from keyboardbuttons import buttons
from database import ddbb
from aiogram.utils.deep_linking import _create_link
import os
import binascii
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from scrapping.asyncscrap import AsyncEnglishScrapper
import asyncio
async def english_adv(call: types.CallbackQuery):
    datab=ddbb.Database()
    scrapper = AsyncEnglishScrapper()
    links=await scrapper.get_page()
    for link in links[0][:5]:
        datab.insert_eng_table(link=link)
        await bot.send_message(chat_id=call.from_user.id, text=link,reply_markup=await buttons.save(link))

async def english_b2(call: types.CallbackQuery):
    datab=ddbb.Database()
    scrapper = AsyncEnglishScrapper()
    links=await scrapper.get_page()
    for link in links[1][:5]:
        datab.insert_eng_table_b2(link=link)
        await bot.send_message(chat_id=call.from_user.id, text=link,reply_markup=await buttons.save(link))

async def english_b1(call: types.CallbackQuery):
    datab=ddbb.Database()
    scrapper = AsyncEnglishScrapper()
    links=await scrapper.get_page()
    for link in links[2][:5]:
        datab.insert_eng_table_b1(link=link)
        await bot.send_message(chat_id=call.from_user.id, text=link,reply_markup=await buttons.save(link))

async def english_a2(call: types.CallbackQuery):
    datab=ddbb.Database()
    scrapper = AsyncEnglishScrapper()
    links=await scrapper.get_page()
    for link in links[3][:5]:
        datab.insert_eng_table_a2(link=link)
        await bot.send_message(chat_id=call.from_user.id, text=link,reply_markup=await buttons.save(link))

async def english_a1(call: types.CallbackQuery):
    datab=ddbb.Database()
    scrapper = AsyncEnglishScrapper()
    links=await scrapper.get_page()
    for link in links[4][:5]:
        datab.insert_eng_table_a1(link=link)
        await bot.send_message(chat_id=call.from_user.id, text=link,reply_markup=await buttons.save(link))


async def eng_favourite_save(call: types.CallbackQuery):
    datab=ddbb.Database()
    check=datab.select_id_fav_table(tg_id=call.from_user.id,link=call.data[5:])
    if check is None:
        datab.insert_favo_eng_table(
            tg_id=call.from_user.id,
            link=call.data[5:]
        )

async def eng_favourites_show(call: types.CallbackQuery):
    datab=ddbb.Database()
    links=datab.select_link_fav_table(tg_id=call.from_user.id)
    for link in links:
        await bot.send_message(
            chat_id=call.from_user.id,
            text=link[0],
            reply_markup=await buttons.fav_delete(link[0])
        )

async def eng_favourites_delete(call: types.CallbackQuery):
    await call.message.delete()
    datab=ddbb.Database()
    datab.delete_fav_eng_table(link=call.data[4:])

async def find_users(call:types.CallbackQuery):
    datab=ddbb.Database()
    ids=datab.select_tg_user_id_fav_table(link=call.data[5:])
    users=[f'tg://user?id={id[0]}' for id in ids if id[0]!= call.from_user.id]
    if users:
        await bot.send_message(
            chat_id=call.from_user.id,
            text=f'Here are the list of users who also prefer that material😁:\n'
                 f'{users}'
        )
    else:
        await bot.send_message(
            chat_id=call.from_user.id,
            text='No users'
        )
def register_scrap(dp: Dispatcher):
    dp.register_callback_query_handler(english_adv, lambda call:call.data == 'advanced')
    dp.register_callback_query_handler(eng_favourite_save, lambda call:call.data.startswith('save'))
    dp.register_callback_query_handler(eng_favourites_show, lambda call:call.data == 'show')
    dp.register_callback_query_handler(eng_favourites_delete, lambda call : call.data.startswith('del'))
    dp.register_callback_query_handler(find_users, lambda call:call.data.startswith('find'))
    dp.register_callback_query_handler(english_b2,lambda call:call.data == 'upperInt')
    dp.register_callback_query_handler(english_b1,lambda call:call.data == 'inter')
    dp.register_callback_query_handler(english_a2,lambda call:call.data == 'ele')
    dp.register_callback_query_handler(english_a1,lambda call:call.data == 'begin')