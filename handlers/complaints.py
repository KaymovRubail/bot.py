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

class Complaints(StatesGroup):
    who=State()
    reason=State()
async def get_complaints(call: types.CallbackQuery):
    await bot.send_message(
        chat_id=call.from_user.id,
        text='Who annoys u (write person`s first name)'
    )
    await Complaints.who.set()
async def load_name(m: types.Message, state: FSMContext):
    data=ddbb.Database()
    rows=data.select_user()
    names=[i[1] for i in rows]
    if m.text in names:
        async with state.proxy() as data:
            data['bad_user']=m.text
        await bot.send_message(
            chat_id=m.from_user.id,
            text='What is the reason?'
        )
        await Complaints.next()
    else:
        await bot.send_message(
            chat_id=m.from_user.id,
            text='There is no such kind of user'
        )
        await state.finish()
async def load_reason(m: types.Message, state: FSMContext):
    datab=ddbb.Database()
    rows=datab.select_user()
    ids = [i[0] for i in rows]
    names = [i[1] for i in rows]
    async with state.proxy() as data:
        data['reason']=m.text
        bad_man_id=ids[names.index(data['bad_user'])]
        try:
            datab.insert_complain_table(
                complainer_id=m.from_user.id,
                user_name=m.from_user.username,
                first_name=m.from_user.first_name,
                badman_id=bad_man_id,
                reason=data['reason']
            )
        except sqlite3.IntegrityError:
            datab.update_complain_table(
                reason=data['reason'],
                badman_id=bad_man_id
            )
        finally:
            count = datab.select_count_complain_table(
                bad_id=bad_man_id,
            )
            if count[0]==3:
                await bot.send_message(
                    chat_id=bad_man_id,
                    text=(f'user {data["bad_user"]}\n'
                          f'U have 3 comlaints💢\n'
                          f'Our Management will contact you\n'
                          f'to verify your account🚦')
                )
            else:
                await bot.send_message(
                    chat_id=bad_man_id,
                    text=(f'user {data["bad_user"]}\n'
                          f'You have a complaint from an unknown user🎭\n'
                          f'reason📖:\n'
                          f'{data["reason"]}\n\n'
                          f'If u press "chance", u will be able to guess who has coplainet about u by user_name or first_name👤'
                          f'If u guess , ur complaint count will decrease -1⏬ else nothing🚫'
                          f'If u press "confirm", nothing will happen'),
                    reply_markup=await buttons.chance_confirm(bad_man_id)
                )
    await bot.send_message(
        chat_id=m.chat.id,
        text='Thank u for informing!'
    )
    await state.finish()

class Guess(StatesGroup):
    guess = State()
async def chance(call: types.CallbackQuery):
    await call.message.delete()
    bad_man_id = call.data.split("_")[1]
    await bot.send_message(
        chat_id=bad_man_id,
        text='You have only one attempt\n'
             'write user_name or first_name'
    )
    await Guess.guess.set()

async def load_guess(m:types.Message, state:FSMContext):
    datab=ddbb.Database()
    names=datab.select_username_complain_table()
    user_name=[i[0] for i in names]
    first_name=[i[1] for i in names]
    if m.text in user_name or m.text in first_name:
        datab.update_count_complain_table(badman_id=m.from_user.id)
        await bot.send_message(
            chat_id=m.from_user.id,
            text='You have guessed, congratulations!🎉🎊\n'
                 'Ur count will decrease'
        )
        await state.finish()
    else:
        await bot.send_message(
            chat_id=m.from_user.id,
            text='You did not guess correctly\n'
                 'try to not get complaints any more'
        )
        await state.finish()

async def confirm(call:types.CallbackQuery):
    await call.message.delete()
    await bot.send_message(
        chat_id=call.from_user.id,
        text='Okay,try to be better😁'
    )
def register_complaints(dp: Dispatcher):
    dp.register_callback_query_handler(get_complaints,lambda call:call.data=='compl')
    dp.register_message_handler(load_name,state=Complaints.who,content_types=['text'])
    dp.register_message_handler(load_reason,state=Complaints.reason,content_types=['text'])
    dp.register_callback_query_handler(chance,lambda call:call.data.startswith('chance'))
    dp.register_callback_query_handler(confirm,lambda call:call.data.startswith('confirm'))
    dp.register_message_handler(load_guess,state=Guess.guess,content_types=['text'])