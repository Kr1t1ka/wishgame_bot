# -*- coding: utf8 -*-
from yoomoney import Client, Quickpay
from config import YM_TOKEN, price
from datetime import datetime
import dbworker
import requests

client = Client(YM_TOKEN)
user = client.account_info()


async def create_payment(user_id):
    form_created = dbworker.get_form_created(user_id)
    if not form_created:
        quickpay = Quickpay(
            receiver=user.account,
            quickpay_form="shop",
            targets="Sponsor this project",
            paymentType="SB",
            sum=price,
            label=user_id
        )
        url = quickpay.base_url
        dbworker.set_pay_url(user_id, url)
        dbworker.set_form_created(user_id, True)
        url = quickpay.redirected_url
    else:
        url = await get_temp_url(user_id)
    dbworker.set_from_date(user_id)
    return url


# create_payment(435375091)

async def check_payment(user_id):
    from_date = dbworker.get_from_date(user_id)
    from_date = datetime.strptime(from_date, "%Y-%m-%d %H:%M:%S.%f")
    history = client.operation_history(label=user_id, from_date=from_date)
    print(history.operations)
    if len(history.operations) > -1:
        # operation = history.operations[0]
        # status = operation.status
        # if status == 'success':
        dbworker.set_paid(user_id, True)
        #     return True
        # else:
        #     return False
    # else:
    #     return False
        return True


# check_payment(435375091)

async def get_temp_url(user_id):
    url = dbworker.get_pay_url(user_id)
    r = requests.get(url, allow_redirects=False, headers={'User-Agent': 'Mozilla/5.0'})
    return r.headers['Location']
