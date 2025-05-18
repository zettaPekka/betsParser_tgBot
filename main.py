import asyncio

from core.init_bot import bot, dp


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except:
        pass