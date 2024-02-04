from aiogram import types, Dispatcher
from config import bot,admin
from keyboardbuttons import buttons
from database import ddbb
async def ask(call: types.CallbackQuery):
    data=ddbb.Database()
    check=data.select_user_answer(tg_id=call.from_user.id)
    if not check:
        await bot.send_message(
            chat_id=call.from_user.id,
            text="Type of transport u prefer:",
            reply_markup=await buttons.question_for_transpot_type('Air✈️', 'Car🚗', 'Train🚂', 'Bus🚌')
        )
    else:
        await bot.send_message(
            chat_id=call.from_user.id,
            text="U have already answered\n"
                 "If u want rewrite press 'rewrite' button",
            reply_markup= await buttons.rewrite()
        )

async def answer_airmodel(call: types.CallbackQuery):
    await bot.send_message(
        chat_id=call.from_user.id,
        text="Wich plane do like most:",
        reply_markup= await buttons.model_airplane('Boeing','Airbus',call.data.replace('aa',''))
    )


async def answer_carmodel(call: types.CallbackQuery):
    await bot.send_message(
        chat_id=call.from_user.id,
        text="Wich car do like most:",
        reply_markup= await buttons.model_car('BMW','Mercedes',call.data.replace('cc',''))
    )


async def answer_Busmodel(call: types.CallbackQuery):
    await bot.send_message(
        chat_id=call.from_user.id,
        text="Wich bus do like most:",
        reply_markup= await buttons.model_bus('London Routemaster (London Bus)','Mercedes-Benz Citaro (Various Cities Worldwide)',call.data.replace('bb',''))
    )


async def answer_trainmodel(call: types.CallbackQuery):
    await bot.send_message(
        chat_id=call.from_user.id,
        text="Wich train do like most:",
        reply_markup= await buttons.model_train('Shinkansen (Bullet Train) - Japan','TGV (Train à Grande Vitesse) - France',call.data.replace('tt',''))
    )


async def yesno_answer(call: types.CallbackQuery):
    await bot.send_message(
        chat_id=call.from_user.id,
        text="Have u ever been on it:",
        reply_markup=await buttons.yes_no("yes✅","no❌",call.data[2:])
    )


async def thanks(call: types.CallbackQuery):
    gg=call.data.split(',')
    print(gg)
    database=ddbb.Database()
    await bot.send_message(
        chat_id=call.from_user.id,
        text="Thank you for answering 🙏🫂"
    )
    try:
        database.insert_answer(
            telegram_id=call.from_user.id,
            name=call.from_user.first_name,
            type=gg[2],
            model=gg[1],
            exp=gg[0]
        )
    except Exception as e:
        database.update_user_answer(
            transport_type=gg[2]
            ,model=gg[1]
            ,experience=gg[0]
            ,telegram_user_id=call.from_user.id
        )

async def answer_for_ban(call: types.CallbackQuery):
    datab=ddbb.Database()
    count=datab.select_count_bun_table(tg_id=call.from_user.id)
    if count:
        await bot.send_message(
            chat_id=call.from_user.id,
            text="U r in the bad users list\n"
                 f"Amount of bad word: {count[0]}"
        )
    else:
        await bot.send_message(
            chat_id=call.from_user.id,
            text="Good for u\n"
                 "There is no ur name\n"
                 "Good boy"
        )

async def warn_user(call: types.CallbackQuery):
    data=ddbb.Database()
    userban = data.seletc_from_ban()
    user_ban_id = [i[0] for i in userban if i[0] != int(admin)]
    user_ban_name = [i[1:] for i in userban if i[0] != int(admin)]
    user_ban_count=[i[2] for i in userban if i[0]!=int(admin)]
    for i in range(len(user_ban_id)):
        try:
            await bot.send_message(
                chat_id=user_ban_id[i]
                , text=f"Hi {user_ban_name[i][0]}\n"
                       f"U have written {user_ban_count[i]} bad word\n"
                       "If u do it 3rd time\n"
                       "U will be bunned📛"
            )
        except Exception as e:
            pass
    await bot.send_message(
        chat_id=call.from_user.id,
        text='Done✅'
    )

async def rewrite_ask(call: types.CallbackQuery):
    await bot.send_message(
        chat_id=call.from_user.id,
        text="Type of transport u prefer:",
        reply_markup=await buttons.question_for_transpot_type('Air✈️', 'Car🚗', 'Train🚂', 'Bus🚌')
    )

t=['я','ю','&','^','$','{','@','%']
h=set(t)
def register_ask(dp: Dispatcher):
    dp.register_callback_query_handler(ask, lambda call: call.data == "question_base")
    dp.register_callback_query_handler(answer_airmodel, lambda call:call.data.startswith("aa"))
    dp.register_callback_query_handler(answer_carmodel, lambda call:call.data.startswith("cc"))
    dp.register_callback_query_handler(answer_trainmodel, lambda call:call.data.startswith("tt"))
    dp.register_callback_query_handler(answer_Busmodel, lambda call:call.data.startswith("bb"))
    dp.register_callback_query_handler(yesno_answer, lambda call:bool(len(set(call.data).intersection(h))))
    dp.register_callback_query_handler(thanks, lambda call:call.data.startswith("yes"))
    dp.register_callback_query_handler(thanks, lambda call:call.data.startswith("no"))
    dp.register_callback_query_handler(answer_for_ban, lambda call:call.data=="bad")
    dp.register_callback_query_handler(warn_user, lambda call:call.data=="warn")
    dp.register_callback_query_handler(rewrite_ask, lambda call:call.data=="re")