# -*- coding: utf8 -*-
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from payment import create_payment
import lang

before_rules = InlineKeyboardMarkup()
next_btn = InlineKeyboardButton(text=lang.next_btn, callback_data="before_rules")
before_rules.add(next_btn)

rules_kb = InlineKeyboardMarkup()
next_btn = InlineKeyboardButton(text=lang.rules_btn, callback_data="go_to_rules")
rules_kb.add(next_btn)

go_to_name = InlineKeyboardMarkup()
next_btn = InlineKeyboardButton(text=lang.ok_rules, callback_data="go_to_name")
go_to_name.add(next_btn)

choose_sex = InlineKeyboardMarkup()
men_btn = InlineKeyboardButton(text=lang.male_btn, callback_data="male")
women_btn = InlineKeyboardButton(text=lang.female_btn, callback_data="female")
choose_sex.add(men_btn, women_btn)


async def go_to_posts(user_id):
    url = await create_payment(user_id)
    go_to_posts = InlineKeyboardMarkup()
    pay_btn = InlineKeyboardButton(text=lang.pay_btn, url=url)
    check_btn = InlineKeyboardButton(text=lang.check_btn, callback_data="check_payment")
    go_to_posts.add(pay_btn).add(check_btn)
    return go_to_posts
