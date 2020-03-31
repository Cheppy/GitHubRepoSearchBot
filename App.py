from aiogram import Bot, Dispatcher, executor, types

from gitSearch import github_search
import misc
from aiogram import Bot, Dispatcher, executor, types

bot = Bot(token=misc.API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends /start or /help command
    """
    await message.reply("Hello user. This bot will help you search github repos")


@dp.message_handler(commands=['search'])
async def echo(message: types.Message):
    """

    :param message:
    This handler will be called when user sends /search command with one or two parameters

    """
    search_args = message.get_args().split()
    print(search_args)

    message_txt = github_search(*search_args)
    if message_txt == "":
        message_txt = f"{misc.error_message} {search_args}'"
    await bot.send_message(message.chat.id, misc.search_results_message + str(message_txt),
                           parse_mode="HTML",
                           disable_web_page_preview=True)

if __name__ == 'main':
    executor.start_polling(dp, skip_updates=True)