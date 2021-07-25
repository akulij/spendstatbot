from hashlib import sha256
from time import time_ns
from datetime import datetime
import matplotlib.pyplot as plt
from random import randbytes

import db
from config import SALT


def parse_message(text):
    raw = text.split(maxsplit=2)
    if len(raw) == 3 and raw[0].isdigit():
        return_data = ("add_cost", {
            "cost": int(raw[0]),
            "buy_type": raw[1],
            "description": raw[2]
        })
    else:
        return_data = ("button_action", text)
    return return_data


def parse_command(text):
    splited = text.split(maxsplit=1)
    if len(splited) == 1:
        return None
    else:
        return splited[1]


def generate_link(user_id):
    family_name = db.get_family_name(user_id)
    if family_name is None:
        return None
    data = family_name + SALT + str(time_ns())
    hash_result = sha256(data.encode("utf-8") + randbytes(10)).hexdigest()
    db.append_family_link(db.get_user_family(user_id), hash_result)
    return hash_result


def getcosts_message_builder(user_id, keyword, start_date, weeks=0, months=0, years=0):
    costs_list = db.get_interval_costs(user_id, start_date, weeks, months, years)
    week_sum = db.get_interval_sum(user_id, start_date, weeks, months, years)
    costs, labels = db.get_costs_statistic(user_id, start_date, weeks, months, years)
    picture_name = None

    message = f"Ваши траты за {keyword}:\n" \
              if len(costs_list) else f"У вас нет трат за {keyword}"

    for num, cost in enumerate(costs_list):
        message += f"  {cost['cost']}руб. - {cost['description']} ({cost['type']})\n"
        if num == 19:
            break
    if len(costs_list) > 20:
        message += "    ...\n"
    if len(costs_list):
        message += "Всего потрачено за {}: {}руб.".format(keyword, week_sum)
        fig, ax = plt.subplots()
        ax.pie(costs, labels=labels, autopct="%i%%")
        picture_name = "images/pieresult{}{}.png".format(datetime.now(), user_id)
        fig.savefig(picture_name)

    return message, picture_name


def family_users_getstatistic(family_id):
    users, totals = db.get_users_infamily_sums(family_id)
    picture_name = None
    family_total = db.get_family_total_in_month(family_id)
    if family_total is None:
        message = "За месяц ничего не потрачено"
    else:
        message = "Потратили за месяц:\n"
        for user, total in zip(users, totals):
            message += f"  {user} - {total}руб.\n"
        message += f"Всего потрачено: {family_total}руб."
        fig, ax = plt.subplots()
        costs, labels = db.get_family_costs_statistic(family_id)
        ax.pie(costs, labels=labels, autopct="%i%%")
        picture_name = "images/pieresult{}{}.png".format(datetime.now(), family_id)
        fig.savefig(picture_name)
    return message, picture_name


def username(message):
    if message is None:
        return "Username"
    else:
        return message.from_user.first_name + \
               (" "+message.from_user.last_name
                if message.from_user.last_name else "")
