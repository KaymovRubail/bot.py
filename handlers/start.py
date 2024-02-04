from aiogram import types, Dispatcher
from database import ddbb
from config import bot,mediaa
from const import FirstCaption
from keyboardbuttons import buttons
from aiogram.utils.deep_linking import _create_link
import sqlite3
async def start_button(message:types.Message):
    data=ddbb.Database()
    command=message.get_full_command()[1]
    if command!='':
        if len(command)==16:
            link = await _create_link('start', payload=command)
            owner = data.select_all_from_tl_users_by_link(link=link)[1]
            ids = data.select_tg_id_user_table(tg_id=message.from_user.id)
            if owner != message.from_user.id:
                if ids is None:
                    try:
                        data.insert_referral_table(owner=owner, referral=message.from_user.id)
                        data.update_tg_user_balance(tg_id=owner)
                    except sqlite3.IntegrityError:
                        pass
            else:
                await bot.send_message(
                    chat_id=message.from_user.id,
                    text='U can not use ur own link🚫'
                )
                return
            data.insert_user(
                telegram_id=message.from_user.id,
                username=message.from_user.username,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name
            )
            with open(mediaa + "ani.gif", 'rb') as gif:
                await bot.send_animation(
                    chat_id=message.from_user.id,
                    animation=gif,
                    caption=FirstCaption.format(name=message.from_user.first_name),
                    reply_markup=await buttons.quest_button(),
                )
        elif len(command)==20:
            data.insert_user(
                telegram_id=message.from_user.id,
                username=message.from_user.username,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name
            )
            link = await _create_link('start', payload=command)

            sender_id= data.select_check_table(link=link)[1]
            amount=data.select_check_table(link=link)[4]
            if sender_id != message.from_user.id:
                await bot.send_message(
                    chat_id=message.from_user.id,
                    text=f'CHECK🎫\n'
                         f'Amount: {amount}',
                    reply_markup=await buttons.use_check(link)
                )
            else:
                await bot.send_message(
                    chat_id=message.from_user.id,
                    text='U cant use ur own check😡'
                )
    else:
        with open(mediaa + "ani.gif", 'rb') as gif:
            await bot.send_animation(
                chat_id=message.from_user.id,
                animation=gif,
                caption=FirstCaption.format(name=message.from_user.first_name),
                reply_markup=await buttons.quest_button(),
            )



def register_start_handler(dp:Dispatcher):
    dp.register_message_handler(start_button, commands="start")