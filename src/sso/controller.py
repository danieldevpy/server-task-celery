from controller.driver import ChromeDriverController
from selenium.webdriver.common.by import By
import time
from sso.entity import Error, DadosFormSSO
from selenium.webdriver.support.ui import Select
from controller.response import ResponseController


class SSOFunctions:

    def __init__(self, chrome: ChromeDriverController) -> None:
        self.chrome = chrome
        self.xpath_login = '//*[@id="txtLogin"]'
        self.xpath_pass = '//*[@id="txtSenha"]'
        self.xpath_btn = '//*[@id="btnLogin"]'
        self.xpath_btn_update ='//*[@id="btnAtualizar"]'
        self.xpath_btn_create = '//*[@id="ctl00_cphBody_FormView1_UpdateCancelButton0"]'
        self.xpath_input_name = '//*[@id="ctl00_cphBody_FormView1_NomeCompletoTextBox"]'
        self.xpath_input_login = '//*[@id="ctl00_cphBody_FormView1_NomeTextBox"]'
        self.xpath_input_cpf = '//*[@id="ctl00_cphBody_FormView1_txtCPF"]'
        self.xpath_select = '//*[@id="ctl00_cphBody_FormView1_ddlNivelAcesso"]'
        self.xpath_btn_save = '//*[@id="ctl00_cphBody_FormView1_InsertButton"]'
        self.xpath_close = '//*[@id="ctl00_MenuSistema"]/ul/li[8]/a'

    def create(self, datas: DadosFormSSO) -> ResponseController:
        try:
            not_permited = ['da', 'do', 'dos', 'das', '', ' ']
            self.chrome.driver.get('http://192.168.1.250/SSONOVAIGUACU/Gerenciamento/GerenciamentoUsuario.aspx')
            btn_create = self.chrome.get_element(self.xpath_btn_create, By.XPATH)
            self.chrome.driver.execute_script("arguments[0].scrollIntoView(true);", btn_create)
            btn_create.click()
            name_split = datas.name.split(' ')
            err = None
            login = None
            for index in range(len(name_split) - 1, 0, -1):
                sobrename = name_split[index].lower()
                login = None
                if sobrename not in not_permited:
                    user = f'{name_split[0]}.{sobrename}'
                    err = self.register(datas.name, user, datas.cpf, datas.get_index())
                    if not err.e:
                        login = user
                        err = None
                        break
                time.sleep(1)
        
    
            btn_close = self.chrome.get_element(self.xpath_close, By.XPATH)
            self.chrome.driver.execute_script("arguments[0].scrollIntoView(true);", btn_close)            
            btn_close.click()
            
            if err:
                message = f'Não foi possivel criar o login de {datas.name}, motivo: {err}'
                return ResponseController(False, message)

            if login:
                message = f'Olá, o login foi criado no sistema SSO!! Usuario: {login} Senha: samu192'
                return ResponseController(True, message)
            
            return ResponseController(False, 'erro desconhecido')
        except Exception as e:
            return ResponseController(False, str(e))
        
    def register(self, name: str, login: str, cpf: str, index: int) -> Error:
        self.chrome.clear_and_set_value(self.xpath_input_name, By.XPATH, name)
        self.chrome.clear_and_set_value(self.xpath_input_login, By.XPATH, login)
        self.chrome.clear_and_set_value(self.xpath_input_cpf, By.XPATH, cpf)
        select_element = self.chrome.get_element(self.xpath_select, By.XPATH)
        select = Select(select_element)
        select.select_by_index(index)
        btn_save = self.chrome.get_element(self.xpath_btn_save, By.XPATH)
        self.chrome.driver.execute_script("arguments[0].scrollIntoView(true);", btn_save)
        btn_save.click()

        xpaths_erros = ['//*[@id="ctl00_cphBody_FormView1_CustomValidator1"]']
        for xpath in xpaths_erros:
            try:
                element = self.chrome.get_element(xpath, By.XPATH, 3)
                if element:
                    return Error(True, element.text)
            except:
                pass

        return Error(False)        
        

    def login(self):
        self.chrome.driver.get('http://192.168.1.250/SSONOVAIGUACU/login.aspx')
        self.chrome.set_value(self.xpath_login, By.XPATH, 'Daniel.Fernandes')
        self.chrome.set_value(self.xpath_pass, By.XPATH, '42658265', True)
        time.sleep(2)
        alert = self.chrome.get_alert()
        try:
            alert.accept()
        except:
            pass
            
        try:
            self.chrome.get_element_if_clicable(self._xpath_btn_update, By.XPATH).click()
        except:
            pass
