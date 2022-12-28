from src.scraper import Colin_scraper
import asyncio
import csv
import datetime

async def main():
    with Colin_scraper() as bot:
        cursor = bot.connect_to_oracle_db()
        date_tuple = bot.select_starting_date_range(cursor)
        orgs = bot.get_corp_nums(cursor)
        bot.open_log_in()
        bot.log_in()
        cookies = bot.get_cookies()
        bot.open_reg_search_from_log_in()

        for org, in orgs:
            bot.search_org(org)
            await bot.download_pdfs(cookies, date_tuple, org)
            bot.go_back()

asyncio.run(main())
