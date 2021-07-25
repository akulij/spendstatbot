from aiogram import Bot, Dispatcher, executor
from aiogram.types import InputFile, InlineKeyboardMarkup, InlineKeyboardButton
import matplotlib.pyplot as plt
from datetime import datetime

from config import BOT_TOKEN, BOTNAME
import db
import kbds
import usefull

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
hello_msg = """
Это бот для слежения за своими тратами.
После любой своей покупки всегда добавляй её так:
(сумма) (категория) (описание)
Пример: 100 такси до дома
Команды:
/familycreate (familyname) - Создание семьи
/familylink - Получение ссылки на семью
/familyremove (username) - Удаление аккаунта из семьи
"""


def dbuserexists(fn):
    """Decorator for check existing user in database before function execution"""
    async def wrapper(message):
        if not db.user_in_db(message.from_user.id):
            db.add_new_user(message.from_user.id, message.from_user.username)
        await fn(message)
    return wrapper


@dp.message_handler(commands=["start"])
@dbuserexists
async def start(message):
    ref_part = usefull.parse_command(message.text)
    if ref_part is None:
        await message.answer(hello_msg, reply_markup=kbds.base_keyboard)
    else:
        db.link_user_to_family(message.from_user.id, ref_part)
        await message.answer(hello_msg, reply_markup=kbds.base_keyboard)
        await message.answer("Your account linked to family successfully")


@dp.message_handler(commands=["familylink"])
@dbuserexists
async def familylink(message):
    """Prints family's link to connect account to family"""
    link = usefull.generate_link(message.from_user.id)
    if link is None:
        await message.answer("You is not in family")
    else:
        await message.answer(f"Your link: t.me/{BOTNAME}?start={link}")


@dp.message_handler(commands=["familyremove"])
@dbuserexists
async def familyremove(message):
    """Removes account from family"""
    username = usefull.parse_command(message.text)
    if username is None:
        await message.answer("You need to specify nickname")
    else:
        user_id = db.get_userid_by_nickname(username)
        if user_id is None:
            await message.answer("Incorrect nickname")
            return
        status = db.remove_user_from_family(user_id,
                                            db.get_family_by_admin_id(message.from_user.id))
        if status == "OK":
            await message.answer("account removed successfully")
        elif status == "NOTINFAMILY":
            await message.answer("You are not admin in user's family")
        elif status == "USERISADMIN":
            await message.answer("Can't remove account if it is admin")
        else:
            await message.answer("Can't remove account from this family")


@dp.message_handler(commands=["familycreate"])
@dbuserexists
async def familycreate(message):
    """Creates family"""
    familyname = usefull.parse_command(message.text)
    if familyname is None:
        await message.answer("You need to specify family name like this:\n/familycreate FamilyName")
    elif len(familyname) > 100:
        await message.answer("Family name can't be longer than 100 chars")
        return
    else:
        status = db.create_family(message.from_user.id, familyname)
        if status == "OK":
            await message.answer("Family created succesfully")
        elif status == "EXISTS":
            await message.answer("You have already created family")
        else:
            await message.answer("Error while creating family")


@dp.message_handler(lambda message: message.text == "Траты за неделю")
@dbuserexists
async def week_costs(message):
    msg, picture_name = usefull.getcosts_message_builder(message.from_user.id,
                                                         start_date=message.date,
                                                         weeks=1, keyword="неделю")
    await message.answer(msg)


@dp.message_handler(lambda message: message.text == "Траты за месяц")
@dbuserexists
async def week_costs(message):
    msg, picture_name = usefull.getcosts_message_builder(message.from_user.id,
                                                         start_date=message.date,
                                                         months=1, keyword="месяц")

    if picture_name:
        await message.answer_photo(photo=InputFile(picture_name), caption=msg)
    else:
        await message.answer(msg)


@dp.message_handler(lambda message: message.text == "Траты за год")
@dbuserexists
async def week_costs(message):
    msg, picture_name = usefull.getcosts_message_builder(message.from_user.id,
                                                         start_date=message.date,
                                                         months=1, keyword="год")

    if picture_name:
        await message.answer_photo(photo=InputFile(picture_name), caption=msg)
    else:
        await message.answer(msg)


@dp.message_handler(lambda message: message.text == "Траты семьи")
@dbuserexists
async def family_costs(message):
    family_id = db.get_user_family(message.from_user.id)

    if family_id is None:
        await message.answer("У вас нет семьи. Создайте её с помощью комманды /familycreate или привяжитесь к другой с помощью линк-ссылки.")
    else:
        msg, picture_name = usefull.family_users_getstatistic(family_id)

        if picture_name:
            await message.answer_photo(photo=InputFile(picture_name), caption=msg)
        else:
            await message.answer(msg)


@dp.message_handler()
@dbuserexists
async def parser(message):
    """Parses message for adding costs"""
    message_type, parsed_msg = usefull.parse_message(message.text)
    if message_type == "add_cost":
        if len(parsed_msg["buy_type"]) > 30:
            await message.answer("Type of cost can't be longer than 30 chars")
            return
        if len(parsed_msg["description"]) > 255:
            await message.answer("Description of cost can't be longer than 255 chars")
            return
        error = db.add_cost(message.from_user.id, parsed_msg["cost"],
                            parsed_msg["buy_type"], parsed_msg["description"],
                            str(message.date))
        if error == "OK":
            await message.answer("Чек успешно добавлен")
        else:
            await message.answer("Невозможно добавить чек")
    else:
        await message.answer("Неизвестная команда. \nПожалуйста, нажмите на одну из кнопок или введите покупку в формате (сумма) (категория) (описание)")


if __name__ == "__main__":
    executor.start_polling(dp)
