from aiogram import types, Dispatcher
from aiogram.types import Update
from config import bot,chat1_id,admin
from keyboardbuttons import buttons
from database import ddbb
from profanity_check import predict_prob
from time import sleep

async def group_filter_message(m: types.Message):
        datab=ddbb.Database()
        bad_word=predict_prob([m.text])
        if bad_word>0.7:
            datab.inseert_ban(tg_id=m.from_user.id,first_name=m.from_user.first_name)
            datab.update_count_bun_table(tg_id=m.from_user.id)
            countt=datab.select_count_bun_table(tg_id=m.from_user.id)
            count=countt[0]
            sleep(0.5)
            await m.delete()
            if count<3:
                await bot.send_message(
                    chat_id=m.chat.id,
                    text=f'user: {m.from_user.first_name}\n'
                         f'U have written bad word\n'
                         f'It was {count}th time\n'
                         f'If u do it 3rd time\n'
                         f'U will be banned❌!!'

                )
            else:
                datab.delete_user(tg_id=m.from_user.id)
                await bot.send_message(
                    chat_id=m.chat.id,
                    text= f'user: {m.from_user.first_name}\n'
                          f'U wrote bad word 3rd time '
                          f'I must ban u!👿'

                )
                sleep(2)
                await bot.ban_chat_member(
                    chat_id=m.chat.id,
                    user_id=m.from_user.id
                )


async def cout_all_users(m:types.Message):
        data = ddbb.Database()
        if m.text == "See all users📃":
            user = data.select_user()
            if user is not None:
                user_id = [i[0] for i in user if i[0]!=int(admin)]
                user_name = [i[1] for i in user if i[0]!=int(admin)]
                l = user_id.copy()
                await bot.send_message(
                    chat_id=m.from_user.id,
                    text=f'{user_name}'
                )
                for i in range(len(user_id)):
                    try:
                        await bot.send_message(
                            chat_id=user_id[i]
                            , text=f'Hi👋,i am ur bot🤖 \n'
                                   f'How are u doing?'
                        )

                    except Exception as e:
                        l.remove(user_id[i])
                chance_to_write = []
                for i in l:
                    for j in user:
                        if i == j[0]:
                            chance_to_write.append(j[1])
                await bot.send_message(
                    chat_id=m.from_user.id
                    , text=f'This is the list of people\n'
                           f'who i can write: \n'
                           f'{chance_to_write}'
                )
        elif m.text == "See all bad users👿":
            userban = data.seletc_from_ban()
            if userban != None:
                user_ban_id = [i[0] for i in userban if i[0]!=int(admin)]
                user_ban_name= [i[1:] for i in userban if i[0]!=int(admin)]
                ll = user_ban_id.copy()
                await bot.send_message(
                    chat_id=m.from_user.id
                    , text=f'{user_ban_name}'
                )
                for i in range(len(user_ban_id)):
                    try:
                        await bot.send_message(
                            chat_id=user_ban_id[i]
                            , text=f'Hi👋,i am ur bot🤖 \n'
                                   f'How are u doing?'
                        )
                    except Exception as e:
                        ll.remove(user_ban_id[i])
                chance_to_write = []
                for i in ll:
                    for j in userban:
                        if i == j[0]:
                            chance_to_write.append(j[1])
                if len(chance_to_write) > 0:
                    await bot.send_message(
                        chat_id=m.from_user.id
                        , text=f'This is the list of people\n'
                               f'who i can write: \n'
                               f'{chance_to_write}'
                        ,reply_markup= await buttons.write_all_userd_button()
                    )
                else:
                    await bot.send_message(
                        chat_id=m.from_user.id
                        , text=f'I have no chance to write anybody'
                    )
        elif m.text=="See all users answer🙈":
            users=data.select_all_user_answer()
            ids=data.select_all_id_answer()
            if users is not None:
                await bot.send_message(
                    chat_id=m.from_user.id
                    , text=f'Here are the user answers🅰️'
                )
                for i in range(len(ids)):
                    ii=list(users[i])
                    idd=ids[i][0]
                    link=f'tg://user?id={idd}'
                    await bot.send_message(
                        chat_id=m.from_user.id
                        , text=f"{ii}\n"
                               f"link: {link}"
                    )
            else:
                await bot.send_message(
                    chat_id=m.from_user.id,
                    text=f'There are no users🥲'
                )
def register_group_filter( dp: Dispatcher):
    dp.register_message_handler(group_filter_message,lambda m:m.chat.id==int(chat1_id))
    dp.register_message_handler(cout_all_users,lambda m:m.chat.id==int(admin))