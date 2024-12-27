import asyncio 
import logging


from config_data.config import Config, load_env_secret
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from handlers import other_handlers, user_handlers
from keyboards.main_menu import set_main_menu

logger = logging.getLogger(__name__)

async def main():
    logging.basicConfig(
        level= logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')
    logger.info('Starting bot')
    config: Config = load_env_secret()
    bot = Bot(token=config.tg_bot.token,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)
    await set_main_menu(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot,allowed_updates=dp.resolve_used_update_types())

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())