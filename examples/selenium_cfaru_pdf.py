from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common import NoSuchElementException, ElementNotInteractableException
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
#options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

def scrap_pdf_url(url):
	logger.info(f'Driver {url!r}')
	driver.get(url)
	#driver.implicitly_wait(2)
	errors = [NoSuchElementException, ElementNotInteractableException] 
	wait = WebDriverWait(
		driver,
		timeout=10,
		poll_frequency=.5,
		ignored_exceptions=errors,
	)
	logger.info('Waiting download button')
	wait.until(lambda _: driver.find_element(By.XPATH, '//*[@title="download"]'))
	download_button = driver.find_element(By.XPATH, '//*[@title="download"]')
	logger.info(f'Button {download_button}')
	download_button.click()
	#driver.implicitly_wait(5)

for target_url in examples_404:
	scrap_pdf_url(target_url)	

