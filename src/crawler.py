# Copyright © 2019 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""This module manages the craler service 

Fetches data from Oracle DB and passes it to the COLIN scraper
"""
import oracledb
import datetime
from dateutil.relativedelta import relativedelta

from . import constants as const


class Colin_crawler():
    """Manages all the aspects of COLIN crawler"""

    def __init__(self, config_path=const.CONFIG_PATH):
        """Initialize and return the crawler service"""
        self.config_path = config_path
        oracledb.init_oracle_client(config_dir=self.config_path)
        self.init_start_date = datetime.datetime.strptime(const.INIT_START_DATE, '%Y/%m/%d')
        self.init_end_date = datetime.datetime.strptime(const.INIT_END_DATE, '%Y/%m/%d')
        self.final_end_date = datetime.datetime.strptime(const.FINAL_END_DATE, '%Y/%m/%d')
        self.cursor = self._connect_to_oracle_db()

    def _connect_to_oracle_db(self):
        """Connect to COLIN Oracle DB."""
        print("connecting to COLIN DB", flush=True)
        connection = oracledb.connect(user=const.ORACLE_USERNAME, password=const.ORACLE_PASSWORD, dsn=const.ORACLE_DSN)
        print("connected to COLIN DB", flush=True)
        cur = connection.cursor()
        return cur

    def fetch_events_in_range(self, start, end):
        """Fetch events from Oracle DB within a datetime range."""
        query = """select distinct CORP_NUM from EVENT
                   where EVENT_TIMESTMP between :start_date and :end_date and EVENT_TYP_CD='FILE'
                   """
        print("querying")
        self.cursor.execute(query, start_date=start, end_date=end)
        print("querying complete")
        return self.cursor

    def get_initial_date_range(self):
        """Return the initial date range from init_start to init_end"""
        return(self.init_start_date, self.init_end_date)

    def get_final_end_date(self):
        """Return the final ending date for the bot"""
        return self.final_end_date

    def get_next_date(self, start, end):
        """Return the next date range as a tuple from an initial date range"""
        start = end
        end += relativedelta(years=1)
        return (start, end)
