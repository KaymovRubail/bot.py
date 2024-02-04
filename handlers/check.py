from aiogram import types, Dispatcher
from config import bot,admin
from keyboardbuttons import buttons
from database import ddbb
from aiogram.utils.deep_linking import _create_link
import os
import binascii
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

async def check_menu(call: types.CallbackQuery):
    await bot.send_message(
        chat_id=call.from_user.id,
        text='Welcome to the check menu',
        reply_markup= await buttons.check_generate()
    )
class CreatCheck(StatesGroup):
    reason=State()
    amount=State()

async def create_check(call: types.CallbackQuery):
    await bot.send_message(
        chat_id=call.from_user.id,
        text='Check creation is running...'
    )
    await bot.send_message(
        chat_id=call.from_user.id,
        text='What you are creating check for?'
    )
    await CreatCheck.reason.set()

async def load_reason(m: types.Message,state: FSMContext):
    async with state.proxy() as data:
        data['reason']=m.text
    await bot.send_message(
        chat_id=m.from_user.id,
        text='Okay, write how much do you want to give\n'
             'if u want to stop🫸 write "stop"'
    )
    await CreatCheck.next()

async def load_amount(m: types.Message,state:FSMContext):
    datab=ddbb.Database()
    balance=datab.select_balance(tg=m.from_user.id)[0]
    if m.text.isdigit():
        if balance!=0:
            if int(m.text) <= balance:
                async with state.proxy() as data:
                    data['amount'] = int(m.text)
                    token = binascii.hexlify(os.urandom(10)).decode()
                    link = await _create_link("start", payload=token)
                    datab.insert_check_table(
                        sender=m.from_user.id,
                        reason=data['reason'],
                        amount=data['amount'],
                        link=link
                    )
                    await bot.send_message(
                        chat_id=m.from_user.id,
                        text=f'U have successfully created your check\n'
                             f'check link: {link}\n'
                             f'Send this link to people who will receive check\n'
                             f'Be careful!'
                    )
                await state.finish()
            else:
                await bot.send_message(
                    chat_id=m.from_user.id,
                    text=f'U dont have so much money\n'
                         f'Ur balance: {balance}\n'
                         f'Write possible amount!'
                )
        else:
            await bot.send_message(
                chat_id=m.from_user.id,
                text=f'Sorry but ur balance is  0, you cant create check😭'
            )
            await state.finish()
    elif m.text.lower() == 'stop':
        await bot.send_message(
            chat_id=m.from_user.id,
            text=f'Check creation is stopped'
        )
        await state.finish()
    else:
        await bot.send_message(
            chat_id=m.from_user.id, text='Write only digits\n'
                                         'if u want to stop🫸\n'
                                         'Write "stop"'
        )

async def use_check(call: types.CallbackQuery):
    datab=ddbb.Database()
    link=call.data[9:]
    status = datab.select_check_table(link=link)[6]
    if status != 'used':
        sender_id = datab.select_check_table(link=link)[1]
        amount = datab.select_check_table(link=link)[4]
        datab.update_tl_user_balance_minus(amount=amount, tg_id=sender_id)
        datab.update_tl_user_balance_minus(amount=-amount, tg_id=call.from_user.id)
        datab.update_check_table(taker=call.from_user.id, status='used', link=link)
        await bot.send_message(
            chat_id=call.from_user.id,
            text=f'You have successfully received check🎉🤑'
        )
    else:
        await bot.send_message(
            chat_id=call.from_user.id,
            text=f'Sorry but this check was already used😭. U cant use it again✖️'
        )
def register_check_system(dp: Dispatcher):
    dp.register_callback_query_handler(check_menu,lambda call:call.data=='check')
    dp.register_callback_query_handler(create_check,lambda call:call.data=='create_check')
    dp.register_message_handler(load_reason,state=CreatCheck.reason,content_types=['text'])
    dp.register_message_handler(load_amount,state=CreatCheck.amount,content_types=['text'])
    dp.register_callback_query_handler(use_check,lambda call:call.data.startswith('usecheck'))