import sys; sys.path.insert(0, '.')
import scraper_lib as scraper
from scraper_lib import Release
import datetime
import uuid

#releases = scraper.CfaReleasesScraper().fetch_and_parse(scraper.Periods.LAST_WEEK)
#releases = scraper.CfaReleasesScraper().fetch_and_parse(scraper.Periods.ALL_AVAILABLE_TIME)
#print(releases)
releases = [Release(
platform_name='На платформе А-Токен',
url='https://цфа.рф/reshenie/A-Token/AlfaBank7',
release_time=datetime.datetime(2024, 9, 3, 0, 0),
title='АО "Альфа-Банк"',
db_id=None
), Release(
platform_name='На платформе Токеон',
url='https://цфа.рф/reshenie/Tokeon/PS',
release_time=datetime.datetime(2024, 9, 3, 0, 0),
title='ИП Подсухин Станислав Олегович',
db_id=None
), Release(
platform_name='На платформе Мастерчейн',
url='https://цфа.рф/reshenie/Masterchain/VTB4',
release_time=datetime.datetime(2024, 9, 2, 0, 0),
title='ПАО "Банк ВТБ"',
db_id=None
), Release(
platform_name='На платформе Мастерчейн',
url='https://цфа.рф/reshenie/Masterchain/VTB6',
release_time=datetime.datetime(2024, 9, 2, 0, 0),
title='ПАО "Банк ВТБ"',
db_id=None
), Release(
platform_name='Платформа ЦФА ХАБ',
url='https://цфа.рф/reshenie/CFAHAB/bRaund3',
release_time=datetime.datetime(2024, 9, 2, 0, 0),
title='ООО "банк Раунд"',
db_id=None
)]

from selenium import webdriver
from selenium.webdriver import ChromeOptions, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.support import expected_conditions as EC
import time 
import uuid
import os

class CfaReleasePDF2TextScraper:
  def __init__(self):
    options = ChromeOptions()
    options.add_argument("--headless")
    options.page_load_strategy = 'eager' # normal
    options.add_experimental_option("prefs", {
      "download.default_directory": '/Users/lusm/fromgit/media_monitoring_bot/pdfs',
      "download.directory_upgrade": True,
      "download.prompt_for_download": False,
      "download.directory_upgrade": True,
      "plugins.always_open_pdf_externally": True,
      "safebrowsing.disable_download_protection": True,
    })
    driver = webdriver.Chrome(options=options)
    self.driver = driver

  def __check_element_disappear__(self, driver):
    try:
      driver.find_element(By.XPATH, '//div[@id="preloader"]')
      return False
    except NoSuchElementException:
      return True

  def __check_file_downloaded__(self, filepath):
    filepath = '/Users/lusm/fromgit/media_monitoring_bot/pdfs/' + filepath
    return lambda _: os.path.isfile(filepath)

  def parse_pdf_to_text(self, pdf_filepath):
    from pdfminer.high_level import extract_text
    import re
    pdf_filepath = '/Users/lusm/fromgit/media_monitoring_bot/pdfs/' + pdf_filepath
    text = extract_text(pdf_filepath)
    text = re.sub(r'\s+', ' ', text) 
    text = re.sub(r'[^\w\s.,!?-]', '', text)
    print(len(text))
    return text

  def fetch_and_parse(self, cfa_url):
    try:
      driver = self.driver
      driver.get(cfa_url)
      WebDriverWait(driver, timeout=15).until(self.__check_element_disappear__)
      btn = WebDriverWait(driver, timeout=30).until(
        EC.element_to_be_clickable(
          (By.XPATH, '//button[(@aria-label="Download") and (@class="svg-button icon group2")]')
        )
      )
      driver.execute_script("arguments[0].click();", btn);
      btn = WebDriverWait(driver, timeout=10).until(
        EC.element_to_be_clickable((By.XPATH, '//a[@class="download-full-button"]'))
      )
      filepath = '_'.join([str(uuid.uuid4()), *cfa_url.split('/')[-2:]]).lower() + '.pdf'
      driver.execute_script("arguments[0].setAttribute('download',arguments[1])", btn, filepath)
      driver.execute_script("arguments[0].click();", btn);
      WebDriverWait(driver, timeout=15, ).until(self.__check_file_downloaded__(filepath))
      pdf_text = self.parse_pdf_to_text(filepath)
      return pdf_text
    except:
      raise ValueError('Cannot get pdfs from url.')

  def driver_quite(self):
    self.driver.quit()

cfapdf2text = CfaReleasePDF2TextScraper()
print(len(releases))
for r in releases:
  print(r.url)
  pdf_text = cfapdf2text.fetch_and_parse(r.url)
  print(len(pdf_text))
  #print(pdf_text)


