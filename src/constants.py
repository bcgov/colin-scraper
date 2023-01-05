import os
from dotenv import load_dotenv

load_dotenv()

STAFF_USERNAME = os.getenv('STAFF_USERNAME')
STAFF_PASSWORD = os.getenv('STAFF_PASSWORD')
ORACLE_USERNAME =  os.getenv('ORACLE_DB_USERNAME')
ORACLE_PASSWORD =  os.getenv('ORACLE_DB_PASSWORD')
ORACLE_DSN =  os.getenv('ORACLE_DB_DSN')
TEST_ORG = os.getenv('TEST_ORG_NUM')

REGISTRY_SEARCH_URL = 'https://www.corporateonline.gov.bc.ca/corporateonline/colin/search/searchAction.do?action=setup&org.apache.struts.taglib.html.TOKEN=d648a1357a80be3449d85f89499d3b25'
LOG_IN_URL = 'https://www.corporateonline.gov.bc.ca/corporateonline/colin/signon/start.do?action=login'
DRIVER_PATH = r'\\SFP.IDIR.BCGOV\U177\MCAI$\Profile\Desktop\Documents\Chrome WebDriver'
TEMP_BASE_PATH = r"C:\Users\MCAI\Desktop\Test PDFs"
UNWANTED_TAGS = ['MAIL', 'EMAIL']
