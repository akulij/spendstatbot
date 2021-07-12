import db
from hashlib import sha256
from config import salt
from time import time_ns


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
    data = db.get_family_data(user_id)
    data.append(salt)
    data.append()
    hash_data = ''.join(data)


def getcosts_message_builder(user_id, keyword, start_date, weeks=0, months=0, years=0):
    costs_list = db.get_interval_costs(user_id, start_date, weeks, months, years)
    week_sum = db.get_interval_sum(user_id, start_date, weeks, months, years)
    costs, labels = db.get_costs_statistic(user_id, start_date, weeks, months, years)

    message = "Ваши траты за {}:\n".format(keyword) \
              if len(costs_list) else "У вас нет трат за {}".format(keyword)

    for num, cost in enumerate(costs_list):
        message += "    {cost}руб. - {description} ({type})\n" \
                   .format(cost=cost["cost"], type=cost["type"],
                           description=cost["description"])
        if num == 19:
            break
    if len(costs_list) > 20:
        message += "    ...\n"
    if len(costs_list):
        message += "Всего потрачено за неделю: {}руб.".format(week_sum)

    return message, costs, labels
