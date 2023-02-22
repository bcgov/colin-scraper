import asyncio

from src.scraper import Colin_scraper
from src.crawler import Colin_crawler

# TODO: fix query
# TODO: find way around 10:45 - 6:00 COLIN lockout

async def main():
    crawler = Colin_crawler()
    with Colin_scraper() as bot:
        date_tuple = crawler.get_initial_date_range()
        end_date = crawler.get_final_end_date()
        bot.open_log_in()
        bot.log_in()
        bot.open_reg_search_from_log_in()
        cookies = bot.get_cookies()

        while date_tuple[1] <= end_date:
            events = crawler.fetch_events_in_range(date_tuple[0], date_tuple[1])
            print(f'start: {date_tuple[0]}')
            print(f'end: {date_tuple[1]}')
            
            for event in events:
                org_num, = event
                print(org_num)
                bot.search_org(org_num)
                await bot.download_pdfs(cookies, date_tuple, org_num)
                bot.reset_search()

            date_tuple = crawler.get_next_date(date_tuple[0], date_tuple[1])

asyncio.run(main())
