import os
from dotenv import load_dotenv

load_dotenv()

STAFF_USERNAME = os.getenv('STAFF_USERNAME')
STAFF_PASSWORD = os.getenv('STAFF_PASSWORD')
ORACLE_USERNAME =  os.getenv('ORACLE_DB_USERNAME')
ORACLE_PASSWORD =  os.getenv('ORACLE_DB_PASSWORD')
ORACLE_DSN =  os.getenv('ORACLE_DB_DSN')
TEST_ORG = os.getenv('TEST_ORG_NUM')
INIT_START_DATE = os.getenv('INIT_START_DATE')
INIT_END_DATE = os.getenv('INIT_END_DATE')
FINAL_END_DATE = os.getenv('FINAL_END_DATE')

REGISTRY_SEARCH_URL = 'http://gaucho.bcgov:7777/corporateonline/colin/search/searchAction.do?action=setup&org.apache.struts.taglib.html.TOKEN=c2cbbb166a6e92f91d38f0dcf48bb866'
LOG_IN_URL = 'http://gaucho.bcgov:7777/corporateonline/colin/signon/start.do?action=login'

# TODO: paths need to be changed to relative paths
CONFIG_PATH = 'config'
DRIVER_PATH = r'\\SFP.IDIR.BCGOV\U177\MCAI$\Profile\Desktop\Documents\Chrome WebDriver'
TEMP_BASE_PATH = r"C:\Users\MCAI\Desktop\Test PDFs"
UNWANTED_TAGS = ['MAIL', 'EMAIL']
