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


def check_preloader_removed(driver):
  try:
    preloader_text = driver.find_element(By.XPATH, '//*[@class="preloader-title"]')
    logger.info(f'Preloader found')
    return False
  except NoSuchElementException:
    logger.info(f'Preloader not found')
    return True

def scrap_pdf_url(url):
  options = ChromeOptions()
  options.add_argument("--headless")
  options.add_experimental_option("prefs", {
      "download.default_directory": './pdfs',
      "download.prompt_for_download": False,
      "download.directory_upgrade": True,
      "plugins.always_open_pdf_externally": True
  })
  driver = webdriver.Chrome(options=options)

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
  logger.debug('Waiting for close')
  #time.sleep(10)

urls = ['https://цфа.рф/reshenie/Sberbank/Mollinomenedjment', 'https://цфа.рф/reshenie/Sberbank/Treidberry', 'https://цфа.рф/reshenie/Sberbank/pigm', 'https://цфа.рф/reshenie/Sberbank/AOSTP', 'https://цфа.рф/reshenie/Sberbank/ROSH', 'https://цфа.рф/reshenie/Sberbank/TP', 'https://цфа.рф/reshenie/Sberbank/FTS', 'https://цфа.рф/reshenie/Sberbank/PG', 'https://цфа.рф/reshenie/Sberbank/STPPZMC', 'https://цфа.рф/reshenie/Sberbank/Gloringfarm', 'https://цфа.рф/reshenie/Sberbank/Resyrs', 'https://цфа.рф/reshenie/Sberbank/Pigment',
 'https://цфа.рф/reshenie/Sberbank/Sberbank', 'https://цфа.рф/reshenie/Sberbank/SBKParitet', 'https://цфа.рф/reshenie/Sberbank/YurPesok', 'https://цфа.рф/reshenie/Sberbank/AlfaBank', 'https://цфа.рф/reshenie/Sberbank/BiznesInvesticii', 'https://цфа.рф/reshenie/Sberbank/BiznesInvest', 'https://цфа.рф/reshenie/Sberbank/77', 'https://цфа.рф/reshenie/Sberbank/omega', 'https://цфа.рф/reshenie/Sberbank/Biznes/Investicii', 'https://цфа.рф/reshenie/Sberbank/BIZNESINVESTICII', 'https://цфа.рф/reshenie/Sberbank/BizInv', 'https://цфа.рф/reshenie/Sberbank/BI', 'https://цфа.рф/reshenie/Sberbank/Avtomatrashet', 'https://цфа.рф/reshenie/Sberbank/BIZ/INVEST', 'https://цфа.рф/reshenie/Sberbank/Sber',
 'https://цфа.рф/reshenie/Sberbank/TDGRASS', 'https://цфа.рф/reshenie/Sberbank/BP', 'https://цфа.рф/reshenie/Sberbank/ERA', 'https://цфа.рф/reshenie/Sberbank/RUSLEO', 'https://цфа.рф/reshenie/Sberbank/RS', 'https://цфа.рф/reshenie/Sberbank/RadCiti', 'https://цфа.рф/reshenie/Sberbank/RADIOST', 'https://цфа.рф/reshenie/Sberbank/RADIOSITI', 'https://цфа.рф/reshenie/Sberbank/RSITI', 'https://цфа.рф/reshenie/Lighthouse/MIA', 'https://цфа.рф/reshenie/Lighthouse/VTBF', 'https://цфа.рф/reshenie/Lighthouse/Reiltm', 'https://цфа.рф/reshenie/Lighthouse/VTBFactoring',
 'https://цфа.рф/reshenie/Lighthouse/Rimeraservise', 'https://цфа.рф/reshenie/Lighthouse/Metrovagonmash', 'https://цфа.рф/reshenie/Lighthouse/souzlizing', 'https://цфа.рф/reshenie/Lighthouse/Gradient', 'https://цфа.рф/reshenie/Lighthouse/Mvm', 'https://цфа.рф/reshenie/A-Token/Rstlc', 'https://цфа.рф/reshenie/A-Token/DG', 'https://цфа.рф/reshenie/A-Token/TDAvtop', 'https://цфа.рф/reshenie/A-Token/GruppakompEKS', 'https://цфа.рф/reshenie/A-Token/NovieFermy', 'https://цфа.рф/reshenie/A-Token/pioner', 'https://цфа.рф/reshenie/A-Token/X5FINANS', 'https://цфа.рф/reshenie/A-Token/Finans',
 'https://цфа.рф/reshenie/A-Token/alrosa', 'https://цфа.рф/reshenie/A-Token/TDA', 'https://цфа.рф/reshenie/A-Token/avtopartner', 'https://цфа.рф/reshenie/A-Token/ZapSibNeftehim', 'https://цфа.рф/reshenie/A-Token/ZSN', 'https://цфа.рф/reshenie/A-Token/NF', 'https://цфа.рф/reshenie/A-Token/Nyufeshen', 'https://цфа.рф/reshenie/A-Token/ROSTEL', 'https://цфа.рф/reshenie/A-Token/SS', 'https://цфа.рф/reshenie/A-Token/ROSATOM', 'https://цфа.рф/reshenie/A-Token/KLSTreide', 'https://цфа.рф/reshenie/A-Token/LKMBPT', 'https://цфа.рф/reshenie/A-Token/ALFABANK', 'https://цфа.рф/reshenie/A-Token/FSK', 'https://цфа.рф/reshenie/A-Token/AlfaBank',
 'https://цфа.рф/reshenie/A-Token/EiPiTreid', 'https://цфа.рф/reshenie/A-Token/Vis', 'https://цфа.рф/reshenie/A-Token/Rostelecomcfa', 'https://цфа.рф/reshenie/A-Token/GlobalFactoringNetvorcRus', 'https://цфа.рф/reshenie/A-Token/Rostelecom', 'https://цфа.рф/reshenie/A-Token/Forte Xoum', 'https://цфа.рф/reshenie/A-Token/Segeja', 'https://цфа.рф/reshenie/A-Token/AB', 'https://цфа.рф/reshenie/A-Token/ALFBNK', 'https://цфа.рф/reshenie/A-Token/GazTransSnab', 'https://цфа.рф/reshenie/A-Token/LotZoloto', 'https://цфа.рф/reshenie/A-Token/ForteHg', 'https://цфа.рф/reshenie/A-Token/bro', 'https://цфа.рф/reshenie/A-Token/VanAiTiTreid', 'https://цфа.рф/reshenie/A-Token/MGKL',
 'https://цфа.рф/reshenie/A-Token/UBL', 'https://цфа.рф/reshenie/A-Token/Pion', 'https://цфа.рф/reshenie/A-Token/GKSEGEJA', 'https://цфа.рф/reshenie/A-Token/ls', 'https://цфа.рф/reshenie/A-Token/Fort', 'https://цфа.рф/files/reshenie_GCP-1-DT-012024-00001-12102023-pioner.pdf', 'https://цфа.рф/files/reshenie3.pdf', 'https://цфа.рф/files/reshenie2.pdf', 'https://цфа.рф/files/reshenie-ALFB-1-DTD-122023-00019-28092023.pdf', 'https://цфа.рф/files/a1.pdf', 'https://цфа.рф/files/-2.pdf', 'https://цфа.рф/files/a3.pdf', 'https://цфа.рф/files/a4.pdf', 'https://цфа.рф/files/a5.pdf', 'https://цфа.рф/files/a6.pdf', 'https://цфа.рф/files/a7.pdf', 'https://цфа.рф/files/a8.pdf',
 'https://цфа.рф/files/a9.pdf', 'https://цфа.рф/files/a10.pdf', 'https://цфа.рф/reshenie/Atomyze/TB', 'https://цфа.рф/reshenie/Atomyze/Sistema', 'https://цфа.рф/reshenie/Atomyze/GFNR', 'https://цфа.рф/reshenie/Atomyze/SibirskoeSteklo', 'https://цфа.рф/reshenie/Atomyze/Sibsteklo', 'https://цфа.рф/reshenie/Atomyze/ROSBANK', 'https://цфа.рф/reshenie/Atomyze/GPF', 'https://цфа.рф/reshenie/Atomyze/TKF', 'https://цфа.рф/reshenie/Atomyze/Rosbank', 'https://цфа.рф/reshenie/Atomyze/ROVIFaktoringplus', 'https://цфа.рф/reshenie/Atomyze/Fortehoum', 'https://цфа.рф/files/Reshenie-o-vypuske-5-ot-25-12-23-palladiy1.pdf', 'https://цфа.рф/files/Reshenie-o-vypuske-6-ot-25-12-23-platina2.pdf', 'https://цфа.рф/files/Reshenie-o-vypuske-Rosbank.pdf', 'https://цфа.рф/files/Reshenie-o-vypuske-22.12-1-6.pdf',
 'https://цфа.рф/files/Reshenie-o-vypuske-22.12.2023-2-5.pdf', 'https://цфа.рф/files/Reshenie-o-vypuske-22.12.23-1-3-4.pdf', 'https://цфа.рф/files/Reshenie-o-vypuske-22.12.23-4-3.pdf', 'https://цфа.рф/files/Reshenie-o-vypuske-Azur-22.12.2023.pdf', 'https://цфа.рф/files/Resheniya-o-vypuske-CFA-kvarta.pdf', 'https://цфа.рф/files/Reshenie-o-vypuske-NDM-22.pdf', 'https://цфа.рф/files/Reshenie-o-vypuske-GFN-03-11-2023-1--.pdf', 'https://цфа.рф/files/Reshenie-o-vypuske-GFN-15-11-2023-2---.pdf', 'https://цфа.рф/files/Reshenie-o-vypuske-CFA-GRADIENT-16-10-2023.pdf', 'https://цфа.рф/files/Reshenie-o-vypuske-cifrovyh-finansovyh-aktivov-1.pdf', 'https://цфа.рф/files/Reshenie-o-vypuske-CFA-GRADIENT.pdf', 'https://цфа.рф/files/Reshenie-o-vypuske-18.pdf', 'https://цфа.рф/files/at1.pdf', 'https://цфа.рф/files/at2.pdf', 'https://цфа.рф/files/at3.pdf', 'https://цфа.рф/files/at4.pdf', 'https://цфа.рф/files/at5.pdf', 'https://цфа.рф/files/at6.pdf', 'https://цфа.рф/files/at7.pdf', 'https://цфа.рф/files/at8.pdf', 'https://цфа.рф/files/at9.pdf', 'https://цфа.рф/files/at10.pdf',
 'https://цфа.рф/reshenie/Masterchain/pt', 'https://цфа.рф/reshenie/Masterchain/sistema', 'https://цфа.рф/reshenie/Masterchain/FINTEH', 'https://цфа.рф/reshenie/Masterchain/Evolyuciya', 'https://цфа.рф/files/5dwco1td1z2s8eagg39c2a1iyl67fxgm.pdf', 'https://цфа.рф/files/2h1cc0vcgoyvojm1k31wir4ol2n5168o1.pdf', 'https://цфа.рф/files/xzn7ka44eb1vziv5br2ca6h789vkzax02.pdf', 'https://цфа.рф/files/d3o1pgaks8r9ms5mv3e09pjg6ys16zeq.pdf', 'https://цфа.рф/files/12kiknut6va8twbfdpr57hw7edf3p6m6-28.11..pdf', 'https://цфа.рф/files/0nadee0s7339vb2gffnj0udql9jg13dh-30.10.2023.pdf', 'https://цфа.рф/files/5cadojmdubomfmp6le8oecgs4fxte1ur-06.10.2023.pdf', 'https://цфа.рф/files/ii773fu43bj4daac2aeb2c7dbb8cnqtr.pdf', 'https://цфа.рф/files/3d3q72s6mimblnt57qnzpx2uhlak2yx9.pdf', 'https://цфа.рф/reshenie/CFAHAB/OZON', 'https://цфа.рф/reshenie/CFAHAB/Devaises', 'https://цфа.рф/files/system_on_the_release_of_CFA.pdf', 'https://цфа.рф/files/Reshenie-MTS.pdf', 'https://цфа.рф/reshenie/Tokeon/FLIP', 'https://цфа.рф/reshenie/Tokeon/Reallizing', 'https://цфа.рф/reshenie/Tokeon/Zalog', 'https://цфа.рф/reshenie/Tokeon/PSB', 'https://цфа.рф/reshenie/Tokeon/Giberno',
 'https://цфа.рф/reshenie/Tokeon/TMobaile2', 'https://цфа.рф/reshenie/Tokeon/TMobaile3', 'https://цфа.рф/files/reshenie_o_vypuske_carmoney4.pdf', 'https://цфа.рф/files/reshenie_o_vypuske_real3.pdf', 'https://цфа.рф/files/reshenie_o_vypuske_psb2.pdf', 'https://цфа.рф/reshenie/Tokeon/Goldex/', 'https://цфа.рф/reshenie/Spb_Birzha/Karbon_Ziro', 'https://цфа.рф/reshenie/EvrofinansMosnarbank/EM', 'https://цфа.рф/reshenie/EvrofinansMosnarbank/SibAvtoTrans', 'https://цфа.рф/reshenie/EvrofinansMosnarbank/SAT', 'https://цфа.рф/reshenie/EvrofinansMosnarbank/SAT3', 'https://цфа.рф/reshenie/EvrofinansMosnarbank/SAT4', 'https://цфа.рф/reshenie/EvrofinansMosnarbank/EL6', 'https://цфа.рф/reshenie/EvrofinansMosnarbank/Uralzavod', 'https://цфа.рф/reshenie/Mosbirzha/Rostelec', 'https://цфа.рф/reshenie/Mosbirzha/Rostel', 'https://цфа.рф/reshenie/Mosbirzha/VBRR',
 'https://цфа.рф/reshenie/Mosbirzha/Invest', 'https://цфа.рф/reshenie/Mosbirzha/Rostelecom', 'https://цфа.рф/reshenie/Mosbirzha/Gazpromneft', 'https://цфа.рф/reshenie/Mosbirzha/GPB'] 


urls = [url for url in urls if not url.endswith('.pdf')]

def sync_scrap_pdf():
  '''
  for target_url in urls[::-1]: #examples_404 + examples_200:
    scrap_pdf_url(target_url)
  '''
  import random
  for i in range(10):
    target_url = random.choice(urls)
    scrap_pdf_url(target_url)
    

sync_scrap_pdf()

def async_scrap_pdf():
  import concurrent.futures
  with concurrent.futures.ThreadPoolExecutor() as executor:
    logger.debug(f'{executor._max_workers=}')
    scrap_pdf_jobs = {
      executor.submit(scrap_pdf_url, url): url
      for url in urls
    }
    for done_job in concurrent.futures.as_completed(scrap_pdf_jobs):
      url = scrap_pdf_jobs[done_job]
      cfa_articles = done_job.result()
      logger.info(f'Done {url}')

#async_scrap_pdf()

