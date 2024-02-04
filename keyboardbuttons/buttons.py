from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def quest_button():
    markup = InlineKeyboardMarkup(row_width=1)
    qb = InlineKeyboardButton('Quastions❔', callback_data='question_base')
    qb1 = InlineKeyboardButton('Check for bad user📛', callback_data='bad')
    qb3 = InlineKeyboardButton('Registration🐧', callback_data='reg')
    qb4 = InlineKeyboardButton('Feedback💬 and Offer🫴', callback_data='fo')
    qb5 = InlineKeyboardButton('My profile🦾', callback_data='mypo')
    qb6 = InlineKeyboardButton('Update profile🪺', callback_data='update')
    qb7 = InlineKeyboardButton('Delete my profile☠️', callback_data='delete')
    qb8 = InlineKeyboardButton('View profiles🫨', callback_data='view')
    qb9 = InlineKeyboardButton('Complain💢', callback_data='compl')
    qb10 = InlineKeyboardButton('Referral menu🪼', callback_data='ferral')
    qb11 = InlineKeyboardButton('Check menu🧾', callback_data='check')
    qb12 = InlineKeyboardButton('Advanced level(English)🦥', callback_data='advanced')
    qb13 = InlineKeyboardButton('Upper Int level', callback_data='upperInt')
    qb14 = InlineKeyboardButton('Intermediate level(English)',callback_data='inter')
    qb15 = InlineKeyboardButton('Elementary level(English)',callback_data='ele')
    qb16 = InlineKeyboardButton('Beginners level(English)',callback_data='begin')
    qb17 = InlineKeyboardButton('Show saved material🌱', callback_data='show')
    markup.add(qb, qb1, qb3, qb4, qb5, qb6, qb7, qb8, qb9, qb10, qb11, qb12, qb13,qb14, qb15, qb16,qb17)
    return markup


async def question_for_transpot_type(var1, var2, var3, var4):
    markup = InlineKeyboardMarkup(row_width=1)
    air = InlineKeyboardButton(var1, callback_data='aa' + var1)
    car = InlineKeyboardButton(var2, callback_data='cc' + var2)
    bus = InlineKeyboardButton(var3, callback_data='bb' + var3)
    train = InlineKeyboardButton(var4, callback_data='tt' + var4)
    markup.add(air, car, bus, train)
    return markup


async def model_airplane(var1, var2, ex):
    markup = InlineKeyboardMarkup()
    air1 = InlineKeyboardButton(var1, callback_data='@' + ',' + var1 + ',' + ex)
    air2 = InlineKeyboardButton(var2, callback_data='ю' + ',' + var2 + ',' + ex)
    markup.add(air1, air2)
    return markup


async def model_car(var1, var2, ex):
    markup = InlineKeyboardMarkup()
    car1 = InlineKeyboardButton(var1, callback_data='$' + ',' + var1 + ',' + ex)
    car2 = InlineKeyboardButton(var2, callback_data='%' + ',' + var2 + ',' + ex)
    markup.add(car1, car2)
    return markup


async def model_train(var1, var2, ex):
    markup = InlineKeyboardMarkup()
    train1 = InlineKeyboardButton(var1, callback_data='{' + ',' + var1 + ',' + ex)
    train2 = InlineKeyboardButton(var2, callback_data='^' + ',' + var2 + ',' + ex)
    markup.add(train1, train2)
    return markup


async def model_bus(var1, var2, ex):
    markup = InlineKeyboardMarkup()
    bus1 = InlineKeyboardButton(var1, callback_data='я' + ',' + var1 + ',' + ex)
    bus2 = InlineKeyboardButton(var2, callback_data='&' + ',' + var2 + ',' + ex)
    markup.add(bus1, bus2)
    return markup


async def yes_no(var1, var2, ex):
    markup = InlineKeyboardMarkup()
    yesbutton = InlineKeyboardButton(var1, callback_data='yes' + ',' + ex)
    nobutton = InlineKeyboardButton(var2, callback_data='no' + ',' + ex)
    markup.add(yesbutton, nobutton)
    return markup


async def write_all_userd_button():
    markup = InlineKeyboardMarkup()
    a = InlineKeyboardButton("warn all users⚠️", callback_data='warn')
    markup.add(a)
    return markup


async def rewrite():
    markup = InlineKeyboardMarkup()
    a = InlineKeyboardButton("Rewrite✏️", callback_data='re')
    markup.add(a)
    return markup


async def like_dislike(user):
    markup = InlineKeyboardMarkup(row_width=1)
    qb1 = InlineKeyboardButton("Like👍", callback_data=f'Like_{user}')
    qb2 = InlineKeyboardButton("Dislike👎", callback_data=f'Dislike_{user}')
    markup.add(qb1, qb2)
    return markup


async def chance_confirm(id):
    markup = InlineKeyboardMarkup(row_width=1)
    a = InlineKeyboardButton("Chance🍀", callback_data=f'chance_{id}')
    b = InlineKeyboardButton("Confirm😐", callback_data=f'confirm_{id}')
    markup.add(a, b)
    return markup


async def generate_link():
    markup = InlineKeyboardMarkup(row_width=1)
    a = InlineKeyboardButton("Generate Link🧬", callback_data='generate_link')
    b = InlineKeyboardButton("See referrals🫣", callback_data='jjj')
    c = InlineKeyboardButton("Balance💴", callback_data='balance')
    d = InlineKeyboardButton("Send money💸", callback_data='send')
    markup.add(a, b, c, d)
    return markup


async def check_generate():
    markup = InlineKeyboardMarkup()
    a = InlineKeyboardButton("Create check©️", callback_data='create_check')
    markup.add(a)
    return markup


async def use_check(link):
    markup = InlineKeyboardMarkup()
    a = InlineKeyboardButton("Use check🎟️", callback_data=f'usecheck_{link}')
    markup.add(a)
    return markup


async def save(link):
    markup = InlineKeyboardMarkup()
    a = InlineKeyboardButton("Save😋", callback_data=f'save,{link}')
    markup.add(a)
    return markup

async def clear():
    markup = InlineKeyboardMarkup()
    a = InlineKeyboardButton("Clear", callback_data='clear')
    markup.add(a)
    return markup

async def fav_delete(links):
    markup = InlineKeyboardMarkup(row_width=1)
    a = InlineKeyboardButton("Delete🍁", callback_data=f'del,{links}')
    b = InlineKeyboardButton("Find others who saved", callback_data=f'find,{links}')
    markup.add(a,b)
    return markup

async def answer_go_back(id):
    markup = InlineKeyboardMarkup(row_width=1)
    a = InlineKeyboardButton("Answer", callback_data=f'ans,{id}')
    b = InlineKeyboardButton("Go back", callback_data='go')
    markup.add(a,b)
    return markup

async def skip():
    markup = InlineKeyboardMarkup(row_width=1)
    a = InlineKeyboardButton("Skip", callback_data='skip')
    markup.add(a)
    return markup