import oracledb
import datetime
from dateutil.relativedelta import relativedelta

from . import constants as const


class Colin_crawler():
    def __init__(self, config_path=const.CONFIG_PATH):
        self.config_path = config_path
        oracledb.init_oracle_client(config_dir=self.config_path)
        self.init_start_date = datetime.datetime.strptime(const.INIT_START_DATE, '%Y/%m/%d')
        self.init_end_date = datetime.datetime.strptime(const.INIT_END_DATE, '%Y/%m/%d')
        self.final_end_date = datetime.datetime.strptime(const.FINAL_END_DATE, '%Y/%m/%d')
        self.cursor = self._connect_to_oracle_db()

    def _connect_to_oracle_db(self):
        connection = oracledb.connect(user=const.ORACLE_USERNAME, password=const.ORACLE_PASSWORD, dsn=const.ORACLE_DSN)
        print("connected to COLIN DB")
        cur = connection.cursor()
        return cur

    def fetch_events_in_range(self, start, end):
        # TODO: might be able to optimize this query
        query = """select distinct CORP_NUM from EVENT
                   where EVENT_TIMESTMP between :start_date and :end_date and EVENT_TYP_CD='FILE'
                   """
        print("querying")
        self.cursor.execute(query, start_date=start, end_date=end)
        print("querying complete")
        return self.cursor

    # TODO: should probably just remove the need for this and turn the starting date range
    # into something we input into the bot
    # could input it through console or maybe set an env var

    def get_initial_date_range(self):
        return(self.init_start_date, self.init_end_date)

    def get_final_end_date(self):
        return self.final_end_date

    def get_next_date(self, start, end):
        start = end
        end += relativedelta(years=1)
        return (start, end)