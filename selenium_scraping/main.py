from time import sleep
from loguru import logger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import env


class Selenium:
    def __init__(self) -> None:
        logger.info('Iniciando Scraping')
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--no-headless')
        chrome_options.add_argument('--disable-dev-shm-usage')

        logger.info('Iniciando Chrome')
        self.driver = webdriver.Chrome(
            options=chrome_options,
            service=Service(ChromeDriverManager().install())
        )


    def access( self, url, time=1):
        try:
            logger.info('Iniciando acesso')
            self.driver.get(url)
            sleep(time)
        except Exception as e:
            print('error to access:', e)


    def select_element(self, by: By , selector, time=1, ):
        try:
            self.find_element = WebDriverWait(self.driver, time).until(
                EC.presence_of_element_located(
                    (by, selector)
                )
            )
        except Exception as e:
            print('error to select element:', e)


    def send_keys(self, keys, time=1):
        try:
            self.find_element.send_keys(keys)
            sleep(time)
        except Exception as e:
            print('error to send keys:', e)


    def enter(self, time=5):
        try:
            self.find_element.send_keys(Keys.ENTER)
            sleep(time)
        except Exception as e:
            print('error to press enter:', e)
    

    def click_element(self, by: By, selector, time=1):
        try:
            self.driver.find_element(
               by, selector
            ).click()     
            
        except Exception as e:
            print('error to open link:', e)

        sleep(time)

if __name__ == '__main__':
    driver =  Selenium()

    # entrar no site
    driver.access('https://www.google.com')
    driver.select_element(By.NAME, 'q')
    driver.send_keys('linkedin')
    driver.enter()
    driver.click_element(
        By.CSS_SELECTOR,
        '#rso > div.hlcw0c > div > div > div > div > div >\
        div > div > div.yuRUbf > div > span > a'        
        )
    
    # preencher informações e entrar
    driver.select_element(By.NAME, 'session_key')
    driver.send_keys(env.EMAIL)
    driver.select_element(By.NAME, 'session_password')
    driver.send_keys(env.PASSWORD)
    driver.select_element(
        By.XPATH,
        '//*[@id="main-content"]/section[1]/div/div/form/div[2]/button'
        )
    driver.enter()

    # pesquisar vagas
    driver.click_element(By.XPATH, '//*[@id="global-nav"]/div/nav/ul/li[3]/a')
    driver.select_element(By.ID, 'jobs-search-box-keyword-id-ember2918', 20)

    logger.info('Scraping finalizado')
