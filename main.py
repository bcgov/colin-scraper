from src.scraper import Colin_scraper
import asyncio
import datetime

TEST_END_DATE = datetime.datetime(2016, 2, 9)
async def main():
    with Colin_scraper() as bot:
        cursor = bot.connect_to_oracle_db()
        date_tuple = bot.select_starting_date_range(cursor)
        orgs = bot.get_corp_nums(cursor)
        bot.open_log_in()
        bot.log_in()
        cookies = bot.get_cookies()
        bot.open_reg_search_from_log_in()
        
        while (date_tuple[1] != TEST_END_DATE):
            for org, in orgs:
                bot.search_org(org)
                await bot.download_pdfs(cookies, date_tuple, org)
                bot.go_back()
            date_tuple = bot.get_next_date(date_tuple[0], date_tuple[1])

asyncio.run(main())
