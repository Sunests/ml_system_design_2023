from tg_bot.bot import TGBot
import asyncio

if __name__ == '__main__':
    tgBot = TGBot()
    asyncio.run(main=tgBot.run_bot())
