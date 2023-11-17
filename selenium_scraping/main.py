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
        chrome_options.page_load_strategy='normal'

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


    def select_element(self, by: By , selector, time=30):
        try:
            self.element = WebDriverWait(self.driver, time).until(
                EC.presence_of_element_located(
                    (by, selector)
                )
            )
        except Exception as e:
            print('error to select element:', e)


    def find_elements(self, by: By, selector):
        sleep(10)
        try:
            return self.driver.find_elements(by, selector)
        except Exception as e:
            print('error to find elements:', e)


    def find_element(self, by: By, selector, time=10):
        sleep(time)
        try:
            return self.driver.find_element(by, selector)
        except Exception as e:
            print('error to find element:', e)

    def send_keys(self, keys, time=1):
        sleep(time)
        try:
            self.element.send_keys(keys)
        except Exception as e:
            print('error to send keys:', e)


    def enter(self, time=5):
        try:
            self.element.send_keys(Keys.ENTER)
            sleep(time)
        except Exception as e:
            print('error to press enter:', e)
    

    def click_element(self, by: By, selector, time=1, aftertime=0):
        sleep(time)
        try:
            self.driver.find_element(
               by, selector
            ).click()     
            sleep(aftertime)
            
        except Exception as e:
            print('error to open link:', e)


if __name__ == '__main__':
    driver = Selenium()

    # ENTRAR NA SALA
    # entra na pagina de login
    driver.access('https://estudante.estacio.br/disciplinas')

    # clica em entrar na pagina inicial de login
    driver.click_element(
        By.XPATH, '//*[@id="section-login"]/div/div/div[1]/section/div[1]/button', 3
        )
    # seleciona input de email
    driver.select_element(By.ID, 'i0116')
    # insere o email
    driver.send_keys(env.EMAIL)
    # da enter depois que insere o email
    driver.enter()
    # seleciona input de senha
    driver.select_element(By.ID, 'i0118')
    # insere a senha
    driver.send_keys(env.PASSWORD)
    # da enter depois que insere a senha
    driver.enter()
    # clica em confirmar para avançar o login
    driver.click_element(By.ID, 'idSIButton9')

    # clica em não mostrar de novo no aviso
    driver.click_element(By.ID, 'KmsiCheckboxField')
    # clica em yes/sim para entrar na sala
    driver.click_element(By.ID, 'idSIButton9')

    # ACESSAR DISCIPLINA
    # pega a section que contem todos os cards de disciplina
    disciplines_parent = driver.find_element(By.XPATH,'//*[@id="app"]/section')
    # pega todos os elementos que indicam o progresso da disciplina
    progress_bar = disciplines_parent.find_elements(By.CLASS_NAME, 'css-1wp63ts')
    # EM ANDAMENTO - pega todos os botões de abrir a disciplina 
    disciplines = disciplines_parent.find_elements(By.ID, 'btn-acessar-disciplina')
    
    # encontra disciplinas que não estão completas
    for index in range(len(progress_bar)):
        if '%' in progress_bar[index].text:
            if '100%' not in progress_bar[index].text:
                print(f'text = {progress_bar[index].text} --- index = {index}')

    logger.info('Scraping finalizado')
