import asyncio
import logging
import configparser
import sys
from aiogram import Bot, Dispatcher

from handlers import employee


if len(sys.argv) > 1:
    CONFIG_PATH = sys.argv[1]
else:
    raise "no config..."


def get_api_token(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)

    return config.get('options', 'telegram_api_token')


async def main(api_token):
    bot = Bot(token=api_token)
    dp = Dispatcher()
    dp.include_routers(employee.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    api_token = get_api_token(CONFIG_PATH)

    logging.basicConfig(level=logging.INFO)
    asyncio.run(main(api_token))
