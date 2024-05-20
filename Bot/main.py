from src.bot import *
if __name__ == "__main__":
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
    asyncio.run(run_scheduler())