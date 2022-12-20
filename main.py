from src.scraper import Colin_scraper
import asyncio
import datetime

async def main():
    with Colin_scraper() as bot:
        bot.open_log_in()
        bot.log_in()
        cookies = bot.get_cookies()
        bot.open_reg_search_from_log_in()
        bot.search_org('BC0990639')
        await bot.download_pdfs(cookies)

asyncio.run(main())
