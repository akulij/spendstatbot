from aiogram import Bot, Dispatcher, executor
from config import botkey

bot = Bot(token=botkey)
dp = Dispatcher(bot)

@dp.message_handler()
async def echo(message):
	await message.answer(message.text)

if __name__ == "__main__":
	executor.start_polling(dp)