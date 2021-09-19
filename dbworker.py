# -*- coding: utf8 -*-
import sqlite3 as sl
import datetime
from config import main_db


def get_current_state(user_id):
    with sl.connect(main_db) as con:
        try:
            data = con.execute('SELECT state FROM USERS WHERE user_id={}'.format(user_id)).fetchone()
            return data[0]
        except:
            return -1


def set_state(user_id, value):
    with sl.connect(main_db) as con:
        con.execute('UPDATE USERS SET state="{}" WHERE user_id={}'.format(value, user_id))


def create_state(user_id):
    with sl.connect(main_db) as con:
        sql = 'INSERT INTO USERS (user_id, state, name, sex, paid, form_created, pay_url, done, last_msg_id) values(?, ?, ?, ?, ?, ?, ?, ?, ?)'
        data = [
            (user_id, '0', '-', '-', False, False, '-', False, 0)
        ]
        con.executemany(sql, data)


def get_user_ids_for_post():
    with sl.connect(main_db) as con:
        data = con.execute('SELECT user_id FROM USERS WHERE paid=True and done=False').fetchall()
        res = [user_id[0] for user_id in data if user_id]
        return res


def set_name(user_id, name):
    with sl.connect(main_db) as con:
        con.execute('UPDATE USERS SET name="{}" WHERE user_id={}'.format(name, user_id))


def get_name(user_id):
    with sl.connect(main_db) as con:
        data = con.execute('SELECT name FROM USERS WHERE user_id={}'.format(user_id)).fetchone()
        return data[0]


def set_sex(user_id, sex):
    with sl.connect(main_db) as con:
        con.execute('UPDATE USERS SET sex="{}" WHERE user_id={}'.format(sex, user_id))


def get_sex(user_id):
    with sl.connect(main_db) as con:
        data = con.execute('SELECT sex FROM USERS WHERE user_id={}'.format(user_id)).fetchone()
        return data[0]


def set_time_zone(user_id, time_zone):
    if not isinstance(time_zone, int):
        time_zone = 0
    with sl.connect(main_db) as con:
        con.execute('UPDATE USERS SET time_zone="{}" WHERE user_id={}'.format(time_zone, user_id))


def get_time_zone(user_id):
    with sl.connect(main_db) as con:
        data = con.execute(f'SELECT time_zone FROM USERS WHERE user_id="{user_id}"').fetchone()
        return data[0]


def get_paid(user_id):
    with sl.connect(main_db) as con:
        data = con.execute('SELECT paid FROM USERS WHERE user_id={}'.format(user_id)).fetchone()
        return data[0]


def set_paid(user_id, state):
    with sl.connect(main_db) as con:
        con.execute('UPDATE USERS SET paid={} WHERE user_id={}'.format(state, user_id))


def get_form_created(user_id):
    with sl.connect(main_db) as con:
        data = con.execute('SELECT form_created FROM USERS WHERE user_id={}'.format(user_id)).fetchone()
        return data[0]


def set_form_created(user_id, state):
    with sl.connect(main_db) as con:
        con.execute('UPDATE USERS SET form_created={} WHERE user_id={}'.format(state, user_id))


def get_from_date(user_id):
    with sl.connect(main_db) as con:
        data = con.execute('SELECT from_date FROM USERS WHERE user_id={}'.format(user_id)).fetchone()
        return data[0]


def set_from_date(user_id):
    date = datetime.datetime.now()
    with sl.connect(main_db) as con:
        con.execute('UPDATE USERS SET from_date="{}" WHERE user_id={}'.format(date, user_id))


def set_pay_url(user_id, url):
    with sl.connect(main_db) as con:
        con.execute('UPDATE USERS SET pay_url="{}" WHERE user_id={}'.format(url, user_id))


def get_pay_url(user_id):
    with sl.connect(main_db) as con:
        data = con.execute('SELECT pay_url FROM USERS WHERE user_id={}'.format(user_id)).fetchone()
        return data[0]


def set_done(user_id):
    with sl.connect(main_db) as con:
        con.execute('UPDATE USERS SET done=True WHERE user_id={}'.format(user_id))


def get_last_msg_id(user_id):
    with sl.connect(main_db) as con:
        data = con.execute('SELECT last_msg_id FROM USERS WHERE user_id={}'.format(user_id)).fetchone()
        return data[0]


def set_last_msg_id(user_id, msg_id):
    with sl.connect(main_db) as con:
        con.execute('UPDATE USERS SET last_msg_id={} WHERE user_id={}'.format(msg_id, user_id))


# print(get_user_ids_for_post())
# for i in get_user_ids_for_post():
#     print(get_time_zone(i))
# print(get_time_zone(274347505))