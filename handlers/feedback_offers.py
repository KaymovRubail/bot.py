from aiogram import types, Dispatcher
from aiogram.types import CallbackQuery

from database import ddbb
from config import bot,mediaa
from const import FirstCaption,Userinfo
from keyboardbuttons import buttons
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class feedb_and_offer(StatesGroup):
    idea=State()
    problem=State()

async def feed_offer(call:types.CallbackQuery):
    await bot.send_message(
        chat_id=call.from_user.id,
        text='What can u offer to make our bot to become better?'
    )
    await feedb_and_offer.idea.set()
async def load_idea(m:types.Message,state:FSMContext):
    async with state.proxy() as data:
        data['idea']=m.text
    await bot.send_message(
        chat_id=m.from_user.id,
        text='What problem did you notice'
    )
    await feedb_and_offer.next()
async def load_problem(m:types.Message,state):
    datab=ddbb.Database()
    async with state.proxy() as data:
        data['problem']=m.text
        datab.insert_feedback_problem_table(
            tg_id=m.from_user.id,
            idea=data['idea'],
            problem=data['problem']
        )
    await bot.send_message(
        chat_id=m.from_user.id, text='Thank u for ur interest'
    )
    await state.finish()

def register_fo(dp:Dispatcher):
    dp.register_callback_query_handler(feed_offer,lambda call:call.data=="fo")
    dp.register_message_handler(load_idea,state=feedb_and_offer.idea,content_types=["text"])
    dp.register_message_handler(load_problem,state=feedb_and_offer.problem,content_types=["text"])