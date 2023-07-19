from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def acessar_url(driver: WebDriver, url: str):
       try:
           return driver.get(url)   
       except Exception as e:
                print('Erro ao acessar URL', e)
 
def encontrar_elemento(driver: WebDriver, elemento):
    try:
        return driver.find_element(by= By.XPATH, value = elemento)
    except Exception as e:
                print('Erro ao procurar elemento', e)

def encontrar_elemento_id(driver: WebDriver, elemento):
    try:
        return driver.find_element(by= By.ID, value = elemento)
    except Exception as e:
                print('Erro ao procurar elemento', e)

def encontrar_elementos(driver: WebDriver, elemento):
    try:
        return driver.find_elements(by = By.ID, value = elemento)
    except Exception as e:
                print('Erro ao procurar elemento', e)
                
def clicar(elemento: WebElement) -> None:
    return elemento.click()

def escrever(elemento: WebElement, texto: str) -> None:
    elemento.send_keys(texto)

def aguardar_clicavel(driver: WebDriver, localizador_elemento: str, tipo_elemento: str = 'XPATH', tempo_espera: int = 60) -> WebElement:
    return WebDriverWait(driver, tempo_espera).until(EC.presence_of_element_located((By().__getattribute__(tipo_elemento.upper()), localizador_elemento)))

