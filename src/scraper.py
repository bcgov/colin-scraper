import os
import aiohttp
import asyncio
import oracledb
import datetime
from dateutil.relativedelta import relativedelta


from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from . import constants as const
from .utils import get_pdf_count

class Colin_scraper(webdriver.Chrome):
    def __init__(self, driver_path=const.DRIVER_PATH):
        self.driver_path = driver_path
        os.environ['PATH'] += self.driver_path
        super(Colin_scraper, self).__init__()
        self.implicitly_wait(1)
        self.maximize_window()

    def open_reg_search_from_log_in(self):
        registry_search = self.find_element(By.XPATH, '//*[@id="servicesLeft"]/div/p[1]/a')
        registry_search.click()

    def reset_search(self):
        try:
            back_btn = self.find_element(By.XPATH, '//*[@id="formContent"]/div[3]/div[1]/a')
            back_btn.click()
        except:
            self.find_element(By.NAME, 'corpNum').clear()


    def open_log_in(self):
        self.get(const.LOG_IN_URL)

    def log_in(self):
        # find all log in elements 
        username = self.find_element(By.NAME, 'user')
        password = self.find_element(By.NAME, 'password')
        submit = self.find_element(By.NAME, 'nextButton')
        type_dropdown = Select(self.find_element(By.NAME, 'realmId'))

        # log in
        username.send_keys('mcai')
        password.send_keys('N0>{m8=6|2@o*2')
        type_dropdown.select_by_value('staff')
        submit.click()

    def search_org(self, org_num):
        # input corpNum
        corp_num = self.find_element(By.NAME, 'corpNum')
        corp_num.send_keys(org_num)
        submit = self.find_element(By.NAME, 'nextButton')
        submit.click()

    async def download_pdfs(self, cookies, date_tuple, org_num):
        start_date, end_date = date_tuple

        # setup cookies and BS
        cookies_payload = self._setup_cookies(cookies)
        soup = self._setup_bs()

        # get all a_tags for pdfs between start_date and end_date
        all_pdf_a_tags = self._find_valid_tags(soup, start_date, end_date)

        # download all PDFs
        pdf_dict = {}
        connector = aiohttp.TCPConnector(force_close=True)
        async with aiohttp.ClientSession(cookies=cookies_payload, connector=connector) as session:
            tasks = []
            # for each href setup callback to grab pdf
            for a_tag in all_pdf_a_tags:
                text = a_tag.text
                count = get_pdf_count(pdf_dict, text)
                href = a_tag.get('href')
                href = 'https://www.corporateonline.gov.bc.ca' + href
                tasks.append(asyncio.ensure_future(self._get_pdf(session, href, text, count)))

            # send requests to get all pdfs in parallel
            pdfs = await asyncio.gather(*tasks)
            # for now write all pdf data from mem into pdf files on disk
            for temp_pdf in pdfs:
                with open(f'{const.BASE_PATH}/' + f'{org_num}_' + temp_pdf['text'] + f'_{temp_pdf["count"]}' '.pdf', 'wb') as pdf:
                    pdf.write(temp_pdf['response'])

    def connect_to_oracle_db(self):
        oracledb.init_oracle_client(config_dir=r'\\SFP.IDIR.BCGOV\U177\MCAI$\Profile\Desktop\scripts\config')
        connection = oracledb.connect(user='readonly', password='t3mpt3mp', dsn='cprd.world')
        print("connected to COLIN DB")
        cur = connection.cursor()
        return cur

    def fetch_events_in_range(self, cursor, start, end):
        query = f"""select CORP_NUM, EVENT_TYP_CD from EVENT
                   where EVENT_TIMESTMP between :start_date and :end_date and EVENT_TYP_CD='FILE'
                   """
        print("querying")
        cursor.execute(query, start_date=start, end_date=end)
        res = cursor.fetchall()
        print("querying complete")
        return res

    def get_starting_date_range(self):
        start = datetime.datetime(2002,1,1)
        end = datetime.datetime(2003,1,1)
        return(start, end)

    def get_next_date(self, start, end):
        start = end
        end += relativedelta(years=1)
        return (start, end)

    def _setup_bs(self):
        # setup bs
        page_source = self.page_source
        soup = bs(page_source, 'lxml')
        return soup

    def _setup_cookies(self, cookies):
        # create cookies dict for session
        cookies_payload = {}
        for cookie in cookies:
                name = cookie['name']
                value = cookie['value']
                cookies_payload[name] = value
        return cookies_payload

    def _find_valid_tags(self, soup, start_date, end_date):
        # get all table rows
        table_rows = soup.find_all('tr', {"class": "displayTableDataOdd"})
        table_rows += soup.find_all('tr', {"class": "displayTableDataEven"})

        # check if each row has date in range, if yes grab it's a_tags
        valid_tags = []

        for row in table_rows:
            date_str = row.select('tr > td')[1].get_text(strip=True)

            try:
                date = datetime.datetime.strptime(date_str, '%B %d, %Y %I:%M %p')
            except ValueError:
                date = datetime.datetime.strptime(date_str, '%B %d, %Y')
                
            if date >= start_date and date <= end_date:
                td_4 = row.select('tr > td')[3]
                a_tags = td_4.find_all('a')
                valid_tags += a_tags
        return valid_tags

    async def _get_pdf(self, session, href, text, count):
        async with session.get(href) as response:
            return {"response": await response.read(), "text": text, "count": count}
