from src.scraper import Colin_scraper
import asyncio
import csv

async def main():
    with Colin_scraper() as bot:
        bot.open_log_in()
        bot.log_in()
        cookies = bot.get_cookies()
        bot.open_reg_search_from_log_in()

        csvfile = open(r'\\SFP.IDIR.BCGOV\U177\MCAI$\Profile\Desktop\COLIN org nums\TABLE_EXPORT_DATA.csv', newline='')
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        count = 0;
        for row in reader:
            if count != 0:
                org_num = row[0].strip('\"')
                bot.search_org(org_num)
                await bot.download_pdfs(cookies)
                bot.go_back()
            count += 1

asyncio.run(main())
