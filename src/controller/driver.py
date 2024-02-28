from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert


class ChromeDriverController:

    def __init__(self, hadless=False, cache=False) -> None:
        chrome_options = Options()
        if hadless:
            chrome_options.add_argument("--headless=new")
        if cache:
            chrome_options.add_argument('--user-data-dir=~/.config/google-chrome')

        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        self.driver.get('http://google.com')

    def get_element(self, element_search: str, type: None, time=30):
        element = WebDriverWait(self.driver, time).until(
            EC.visibility_of_element_located((type, element_search))
        )
        return element
    
    def get_element_if_clicable(self, element_search: str, type: None, time=30):
        element = WebDriverWait(self.driver, time).until(
            EC.element_to_be_clickable((type, element_search))
        )
        return element

    def set_value(self, element_search: str, type: None, value: str, confirm=False ,time=30):
        element = self.get_element(element_search, type, time)
        if confirm:
            element.send_keys(value, Keys.ENTER)
        else:
            element.send_keys(value)

    def clear_and_set_value(self, element_search: str, type: None, value: str, confirm=False ,time=30):
        element = self.get_element(element_search, type, time)
        element.clear()
        if confirm:
            element.send_keys(value, Keys.ENTER)
        else:
            element.send_keys(value)

    def get_value(self, element_search: str, type: None) -> str:
        element = self.get_element(element_search, type)
        return element.text()
    
    def progress_bar(self, element_search, type: None):
        WebDriverWait(self.driver, 10).until(EC.text_to_be_present_in_element((type, element_search), "Enviado com sucesso"))

    def get_alert(self) -> Alert | bool:
        try:
            return Alert(self.driver)
        except:
            False

        
