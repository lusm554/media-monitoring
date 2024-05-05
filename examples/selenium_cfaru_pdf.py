from selenium import webdriver
from selenium.webdriver import ChromeOptions, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common import NoSuchElementException, ElementNotInteractableException
import time
import logging

logging.basicConfig(
  level=logging.INFO,
  format='[%(asctime)s] %(levelname)s [%(name)s] %(message)s',
  datefmt='%Y-%m-%d %H:%M:%S %Z',
)
logger = logging.getLogger(__name__)

examples_404 = [
	'https://цфа.рф/reshenie/Tokeon/Zalog',
]
examples_200 = [
	'https://цфа.рф/reshenie/Tokeon/TMobaile3',
]

options = ChromeOptions()
options.add_argument("--headless")
options.add_experimental_option("prefs", {
    "download.default_directory": '/Users/lusm/fromgit/monitor-cfa-rss/examples/',
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True
})
driver = webdriver.Chrome(options=options)

def check_preloader_removed(driver):
	try:
		preloader_text = driver.find_element(By.XPATH, '//*[@class="preloader-title"]')
		logger.info(f'Preloader found')
		return False
	except NoSuchElementException:
		logger.info(f'Preloader not found')
		return True

def scrap_pdf_url(url):
	logger.info(f'Driver {url!r}')
	driver.get(url)
	wait = WebDriverWait(
		driver,
		timeout=15,
		poll_frequency=.5,
	)
	logger.info('Waiting download menu button')
	wait.until(check_preloader_removed)
	try:
		download_menu_button = driver.find_element(By.XPATH, '//*[@title="Download"]')
		ActionChains(driver).click(download_menu_button).perform()
		logger.info('Clicked download menu button')
	except Exception as error:
		logger.error(error)
	time.sleep(.5)
	try:
		download_button = driver.find_element(By.XPATH, '//*[@href="linkFull"]')
		ActionChains(driver).click(download_button).perform()
		#download_button = driver.find_element(By.XPATH, '//*[@href="linkFull"]')
		#print(download_button.href)
		logger.info('Clicked download button')
		time.sleep(1)
	except Exception as error:
		logger.error(error)
	logger.info('Waiting for close')
	#time.sleep(10)

for target_url in examples_404:
	scrap_pdf_url(target_url)	

