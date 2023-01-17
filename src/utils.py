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
"""This module contains utility functions for scraper"""
import datetime

def avg_dates(dates):
    """Used for testing

    Return the average datetime from an array of datetimes
    """
    sum = datetime.timedelta()
    for date in dates:
        sum += date
    return sum / len(dates)

def get_pdf_count(pdf_dict, text):
    """Return the number of a PDF in pdf_dict"""
    if text in pdf_dict:
        pdf_dict[text] += 1
        count = pdf_dict[text]
    else:
        pdf_dict[text] = 0
        count = pdf_dict[text]
    return count
