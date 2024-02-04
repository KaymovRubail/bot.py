from aiogram import types, Dispatcher
from config import bot,admin
from keyboardbuttons import buttons
from database import ddbb
from aiogram.utils.deep_linking import _create_link
import os
import binascii
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

async def reference_menu(call: types.CallbackQuery):
    datab=ddbb.Database()
    info=datab.select_balance_totalreferral_table(tg_id=call.from_user.id)
    await bot.send_message(
        chat_id=call.from_user.id,
        text=f'Welcome to referral menu\n'
             f'Share me and invite others\n'
             f'to earn money🤑!!\n'
             f'Balance: {info[0]}\n'
             f'Referrals: {info[1]}\n'
             f'Press button below to generate link',
        reply_markup= await buttons.generate_link()
    )


async def generate_link(call: types.CallbackQuery):
    datab=ddbb.Database()
    link_user=datab.select_all_from_tl_users(tg_id=call.from_user.id)[5]
    if link_user:
        await bot.send_message(
            chat_id=call.from_user.id,
            text=f'Your old link: {link_user}'
        )
    else:
        token = binascii.hexlify(os.urandom(8)).decode()
        link = await _create_link("start", payload=token)
        datab.update_tg_user_link(link=link,tg_id=call.from_user.id)
        await bot.send_message(
            chat_id=call.from_user.id,
            text=f'Your new link: {link}'
        )
async def see_referrals(call: types.CallbackQuery):
    datab=ddbb.Database()
    referrals=datab.select_referrals_referral_table(tg_id=call.from_user.id)
    ids=[i[0] for i in referrals]
    await bot.send_message(
        chat_id=call.from_user.id,
        text=f'Your referrals: {ids}'
    )
async def balance(call: types.CallbackQuery):
    datab=ddbb.Database()
    balance=datab.select_balance(tg=call.from_user.id)[0]
    await bot.send_message(
        chat_id=call.from_user.id,
        text=f'Your balance: {balance}'
    )
class Send_money(StatesGroup):
    first_name=State()
    amount=State()
async def send_money(call: types.CallbackQuery):
    await bot.send_message(
        chat_id=call.from_user.id,
        text="Who do u want send money for?\n"
             "Write user's first_name🥸"
    )
    await Send_money.first_name.set()

async def load_first_name(m: types.Message,state: FSMContext ):
    datab=ddbb.Database()
    all=datab.select_user()
    names=[i[1] for i in all]
    if m.text in names:
        async with state.proxy() as data:
            data['first_name']=m.text
        await bot.send_message(
            chat_id=m.from_user.id,
            text='Okay, How much would u like to give?'
        )
        await Send_money.next()
    else:
        await bot.send_message(
            chat_id=m.from_user.id,
            text='Sorry,there is no user with that name'
        )
        await state.finish()

async def load_amount(m: types.Message,state:FSMContext ):
    datab=ddbb.Database()
    all = datab.select_user()
    balance=datab.select_balance(tg=m.from_user.id)[0]
    names = [i[1] for i in all]
    ids = [i[0] for i in all]
    if m.text.isdigit():
        if int(m.text) <= balance:
            async with state.proxy() as data:
                data['amount']=int(m.text)
                datab.insert_transactions(
                    sender=m.from_user.id,
                    taker=ids[names.index(data['first_name'])],
                    amount=int(m.text)
                )
                datab.update_tl_user_balance_minus(amount=data['amount'],tg_id=m.from_user.id)
                datab.update_tl_user_balance_minus(amount=-data['amount'],tg_id=ids[names.index(data['first_name'])])
            await bot.send_message(
                chat_id=m.from_user.id,
                text='U have successfully sent your money🎉🤑'
            )
            await state.finish()
        else:
            await bot.send_message(
                chat_id=m.from_user.id,
                text='Sorry, u dont have enough money to sending🥸\n'
                     'Start again to resend.'
            )
            await state.finish()
    else:
        await bot.send_message(
            chat_id=m.from_user.id,
            text='Write only digits!!😡\n'
                 'Start again to resend.'

        )
        await state.finish()



def register_referrence(dp:Dispatcher):
    dp.register_callback_query_handler(reference_menu,lambda call:call.data=='ferral')
    dp.register_callback_query_handler(generate_link,lambda call:call.data=='generate_link')
    dp.register_callback_query_handler(see_referrals,lambda call:call.data=='jjj')
    dp.register_callback_query_handler(balance,lambda call:call.data=='balance')
    dp.register_callback_query_handler(send_money,lambda call:call.data=='send')
    dp.register_message_handler(load_first_name,state=Send_money.first_name,content_types=['text'])
    dp.register_message_handler(load_amount,state=Send_money.amount,content_types=['text'])