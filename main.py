from aiogram import Bot, Dispatcher, executor
from aiogram.types import InputFile
import matplotlib.pyplot as plt
from datetime import datetime

from config import botkey
import db
import kbds
import usefull

bot = Bot(token=botkey)
dp = Dispatcher(bot)


def dbuserexists(fn):
    async def wrapper(message):
        if not db.user_in_db(message.from_user.id):
            # print(message)
            db.add_new_user(message.from_user.id, message.from_user.username)
        await fn(message)
    return wrapper


def removed(fn):
    async def removed_func(message):
        print("Function {} was removed, use another instead". format(fn.__name__))
    return removed_func


@dp.message_handler(commands=["start"])
@dbuserexists
async def start(message):
    ref_part = usefull.parse_command(message.text)
    if ref_part is None:
        await message.answer("Hello!", reply_markup=kbds.base_keyboard)
    else:
        status = db.link_to_family(message.from_user.id, ref_part)
        if status == "ADDED":
            await message.answer("Your account linked to family successfully")
        elif status == "CHANGED":
            await message.answer("you have changed family successfully")
        else:
            await message.answer("Can't link account to this family")


@dp.message_handler(commands=["familylink"])
async def familylink(message):
    """Prints family's link to connect account to family"""
    link = usefull.generate_link(message.from_user.id)
    if link is None:
        await message.answer("You is not in family")
    else:
        await message.answer("Your link: {}".format(link))


@dp.message_handler(commands=["family"])
async def family(message):
    "Prints family's statistic"
    args = message.text[1:]
    await message.answer(args)


@dp.message_handler(commands=["familyadd"])
@removed
async def familyadd(message):
    """adds account to the family"""
    status = db.add_user_to_family(username, db.get_user_family(message.from_user.id))
    if status == "OK":
        await message.answer("account added successfully")
    elif status == "EXISTS":
        await message.answer("account was added previously")
    else:
        await message.answer("Can't add account to this family")


@dp.message_handler(commands=["familyremove"])
async def familyremove(message):
    """Removes account from family"""
    status = db.remove_user_from_family(username, db.get_user_family(message.from_user.id))
    if status == "OK":
        await message.answer("account added successfully")
    elif status == "NOTINFAMILY":
        await message.answer("You are not admin in user's family")
    else:
        await message.answer("Can't add account to this family")


@dp.message_handler(commands=["familycreate"])
async def familycreate(message):
    """Creates family"""
    familyname = usefull.parse_command(message.text)
    if familyname is None:
        await message.answer("You need to specify family name like this:\n/family FamilyName")
    else:
        status = db.create_family(message.from_user.id, familyname)
        if status == "OK":
            await message.answer("Family created succesfully")
        if status == "EXISTS":
            await message.answer("You have already created family")
        else:
            await message.answer("Error while creating user")


@dp.message_handler(lambda message: message.text == "Траты за неделю")
async def week_costs(message):
    msg, costs, labels = usefull.getcosts_message_builder(message.from_user.id,
                                                          start_date=message.date,
                                                          weeks=1, keyword="неделю")
    await message.answer(msg)


@dp.message_handler(lambda message: message.text == "Траты за месяц")
async def week_costs(message):
    fig, ax = plt.subplots()
    msg, costs, labels = usefull.getcosts_message_builder(message.from_user.id,
                                                          start_date=message.date,
                                                          months=1, keyword="месяц")
    ax.pie(costs, labels=labels, autopct="%iруб.")
    picture_name = "pieresult{}{}.png".format(datetime.now(), message.from_user.id)
    fig.savefig(picture_name)

    # await message.answer(msg)
    await message.answer_photo(photo=InputFile(picture_name), caption=msg)


@dp.message_handler(lambda message: message.text == "Траты за год")
async def week_costs(message):
    fig, ax = plt.subplots()
    msg, costs, labels = usefull.getcosts_message_builder(message.from_user.id,
                                                          start_date=message.date,
                                                          months=1, keyword="год")
    ax.pie(costs, labels=labels, autopct="%iруб.")
    picture_name = "pieresult{}{}.png".format(datetime.now(), message.from_user.id)
    fig.savefig(picture_name)

    await message.answer_photo(photo=InputFile(picture_name), caption=msg)


@dp.message_handler()
@dbuserexists
async def parser(message):
    """Parses message for adding costs, etc"""
    message_type, parsed_msg = usefull.parse_message(message.text)
    if message_type == "add_cost":
        error = db.add_cost(message.from_user.id, parsed_msg["cost"],
                            parsed_msg["buy_type"], parsed_msg["description"],
                            str(message.date))
        if error == "OK":
            await message.answer("Чек успешно добавлен")
        else:
            await message.answer("Невозможно добавить чек")


if __name__ == "__main__":
    executor.start_polling(dp)
