# -*- coding: utf8 -*-
from aiogram import Bot
from config import TOKEN, am_time, pm_time, total_days
from datetime import datetime
from lang import post_today, days_between
import aioschedule
import asyncio
import dbworker

bot = Bot(token=TOKEN)


async def edit_message_text(chat_id, text, parse_mode='HTML', disable_web_page_preview=False, reply_markup=None):
    last_msg_id = dbworker.get_last_msg_id(chat_id)
    try:
        await bot.edit_message_text(chat_id=chat_id, message_id=last_msg_id, text=text, parse_mode=parse_mode,
                                    reply_markup=reply_markup)
    except Exception as e:
        print(e)
        try:
            await bot.delete_message(chat_id, last_msg_id)
        except Exception as e:
            print(e)
        message = await bot.send_message(chat_id, text, parse_mode=parse_mode, reply_markup=reply_markup,
                                         disable_web_page_preview=disable_web_page_preview)
        dbworker.set_last_msg_id(chat_id, message.message_id)


async def current_time():
    aioschedule.every().day.at(am_time).do(everyday_post, part_of_day='am')
    aioschedule.every().day.at(pm_time).do(everyday_post, part_of_day='pm')
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def everyday_post(part_of_day):
    user_ids = dbworker.get_user_ids_for_post()
    for user_id in user_ids:
        day = await days_between(user_id[0])
        print(f'user: {user_id} day: {day}')
        if day > 0:
            if day == 1:
                last_msg_id = dbworker.get_last_msg_id(user_id[0])
                try:
                    await bot.delete_message(user_id[0], last_msg_id)
                except Exception as e:
                    print(e)
            await post_today(user_id[0], part_of_day)
        if day == total_days and part_of_day == 'pm':
            dbworker.set_done(user_id[0])
