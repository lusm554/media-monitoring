from selenium import webdriver
from selenium.webdriver import ChromeOptions, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.support import expected_conditions as EC
import time 

url = 'https://цфа.рф/reshenie/CFAHAB/bRaund3'
options = ChromeOptions()
#options.add_argument("--headless")
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
driver.get(url)

def check_element_disappear(driver):
  try:
    driver.find_element(By.XPATH, '//div[@id="preloader"]')
    return False
  except NoSuchElementException:
    return True

try:
  #time.sleep(60*5)
  print(1)
  WebDriverWait(driver, timeout=15).until(check_element_disappear)
  print(2)
  btn = WebDriverWait(driver, timeout=30).until(
    EC.element_to_be_clickable(
      (By.XPATH, '//button[(@aria-label="Download") and (@class="svg-button icon group2")]')
    )
  )
  driver.execute_script("arguments[0].click();", btn);
  print(3)
  #ActionChains(driver).click(btn).perform()
  #driver.implicitly_wait(60*5)
  btn = WebDriverWait(driver, timeout=10).until(
    EC.element_to_be_clickable((By.XPATH, '//a[@class="download-full-button"]'))
  )
  driver.execute_script("arguments[0].setAttribute('download',arguments[1])", btn, 'cfa_234.pdf')
  print(4)
  #ActionChains(driver).click(btn).perform()
  driver.execute_script("arguments[0].click();", btn);
  time.sleep(3)
  print(5)
finally:
  driver.quit()

