from src.scraper import Colin_scraper
import asyncio
import datetime

TEST_END_DATE = datetime.datetime(1901, 1, 1)
async def main():
    with Colin_scraper() as bot:
        # connect to oracle db
        # get starting date range
        # log in and go to reg search
        # get list of events to search through
        # for each event:
            # search org_num
            # download all pdfs in date range
            # go back to search

        cursor = bot.connect_to_oracle_db()
        date_tuple = bot.get_starting_date_range()
        bot.open_log_in()
        bot.log_in()
        cookies = bot.get_cookies()
        bot.open_reg_search_from_log_in()

        # replace TEST_END_DATE with present date or something
        while date_tuple[0] != TEST_END_DATE:
            events = bot.fetch_events_in_range(cursor, date_tuple[0], date_tuple[1])
            print(f'start: {date_tuple[0]}')
            print(f'end: {date_tuple[1]}')
            for event in events:
                org, = event
                print(org)
                bot.search_org(org)
                await bot.download_pdfs(cookies, date_tuple, org)
                bot.reset_search()

            date_tuple = bot.get_next_date(date_tuple[0], date_tuple[1])

asyncio.run(main())
