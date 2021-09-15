# -*- coding: utf8 -*-
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from functions import edit_message_text, current_time
from config import TOKEN, States
from payment import check_payment
import keyboards as kb
import aioschedule
import dbworker
import asyncio
import lang

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


async def on_startup(_):
    asyncio.create_task(current_time())
    print('Бот запущен..')


# START
@dp.message_handler(lambda message: dbworker.get_current_state(message.chat.id) == States.START.value)
@dp.message_handler(commands=['start'])
async def start_command(msg: types.Message):
    print(msg, types.Message)
    chat_id = msg.chat.id
    try:
        await bot.delete_message(chat_id, msg.message_id)
    except Exception as e:
        print(e)
    if dbworker.get_current_state(chat_id) == -1:
        dbworker.create_state(chat_id)
        message = await bot.send_message(chat_id, lang.privetstvie, reply_markup=kb.before_rules)
        dbworker.set_last_msg_id(chat_id, message.message_id)
    elif dbworker.get_name(chat_id) == '-':
        await edit_message_text(chat_id, lang.enter_name)
        dbworker.set_state(chat_id, States.NAME.value)
    elif dbworker.get_sex(chat_id) == '-':
        await edit_message_text(chat_id, lang.enter_sex, reply_markup=kb.choose_sex)
    elif not dbworker.get_paid(chat_id):
        last_msg_id = dbworker.get_last_msg_id(chat_id)
        try:
            await bot.delete_message(chat_id, last_msg_id)
        except Exception as e:
            print(e)
        message = await bot.send_message(chat_id, lang.payment_text, reply_markup=await kb.go_to_posts(chat_id))
        dbworker.set_last_msg_id(chat_id, message.message_id)


# NAME
@dp.message_handler(lambda message: dbworker.get_current_state(message.chat.id) == States.NAME.value)
async def name_command(msg: types.Message):
    chat_id = msg.chat.id
    print(msg)
    try:
        await bot.delete_message(chat_id, msg.message_id)
    except Exception as e:
        print(e)
    dbworker.set_name(chat_id, msg.text)
    await edit_message_text(chat_id, lang.time_zone)
    dbworker.set_state(chat_id, States.TIMEZOME.value)


# TIMEZONE
@dp.message_handler(lambda message: dbworker.get_current_state(message.chat.id) == States.TIMEZOME.value)
async def timezone_command(msg: types.Message):
    chat_id = msg.chat.id
    print(msg)
    try:
        await bot.delete_message(chat_id, msg.message_id)
    except Exception as e:
        print(e)

    if msg.text.isdigit():
        user_msg = int(msg.text)
    else:
        user_msg = msg.text

    dbworker.set_time_zone(chat_id, user_msg)
    await edit_message_text(chat_id, lang.enter_sex, reply_markup=kb.choose_sex)
    dbworker.set_state(chat_id, States.START.value)


# CALLBACKS
@dp.callback_query_handler(lambda call: True)
async def callback_inline(call):
    chat_id = call.message.chat.id
    msg_id = call.message.message_id
    if call.message:
        # print(call.message)
        # print(call.data)
        if call.data == 'before_rules':
            await edit_message_text(chat_id, lang.before_rules, reply_markup=kb.rules_kb)
        elif call.data == 'go_to_rules':
            await edit_message_text(chat_id, lang.rules, reply_markup=kb.go_to_name)
        elif call.data == 'go_to_name':
            await edit_message_text(chat_id, lang.enter_name)
            dbworker.set_state(chat_id, States.NAME.value)

        elif call.data == 'male':
            dbworker.set_sex(chat_id, 'm')
            await edit_message_text(chat_id, lang.payment_text, reply_markup=await kb.go_to_posts(chat_id))
        elif call.data == 'female':
            dbworker.set_sex(chat_id, 'w')
            await edit_message_text(chat_id, lang.payment_text, reply_markup=await kb.go_to_posts(chat_id))
        elif call.data == 'check_payment':
            result = await check_payment(chat_id)
            if result:
                s = dbworker.get_sex(chat_id)
                await edit_message_text(chat_id, eval(f'lang.after_pay_text_{s}'))
            else:
                await bot.answer_callback_query(call.id, lang.dont_paied, show_alert=True)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
