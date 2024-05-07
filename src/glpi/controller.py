import tempfile, os, re, base64, json
from typing import List
from selenium.webdriver.common.by import By
from controller.driver import ChromeDriverController
from glpi.entity import DatasRegister, Archive
from controller.response import ResponseController


class GLPIFunctions:

    def __init__(self, chrome: ChromeDriverController) -> None:
        self.chrome = chrome
        self.xpath_login = '//*[@id="login_name"]'
        self.xpath_pass = '/html/body/div[1]/div/div/div[2]/div/form/div/div[1]/div[3]/input'
        self.name_title_chamado = 'name'
        self.css_iframe = 'tox-edit-area__iframe'
        self.name_input = '_uploader_filename[]'
        self.xpath_btn = '//*[@id="itil-form"]/div/div[4]/button'

    def login(self, user: str = 'Portal Chamado', passw: str = 'Cisbaf2023'):
        try:
            self.chrome.driver.get("http://192.168.1.235/index.php?noAUTO=1")
            self.chrome.set_value(self.xpath_login, By.XPATH, user)
            self.chrome.set_value(self.xpath_pass, By.XPATH, passw, True)
            if self.chrome.driver.title != "Home - GLPI": # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! warning
                raise Exception("Usuário ou senha invalida")
        except Exception as e:
            raise Exception("ERROR LOGIN - " + str(e))
        
    def open_request(self, datas: DatasRegister, archives: List[Archive] = None) -> ResponseController:
        try:
            self.chrome.driver.get("http://192.168.1.235/front/ticket.form.php")
            self.chrome.set_value(self.name_title_chamado, By.NAME, f'{datas.reason}')
            iframe = self.chrome.get_element(self.css_iframe, By.CLASS_NAME)
            self.chrome.driver.switch_to.frame(iframe)
            paragrafo_element = self.chrome.get_element("p", By.TAG_NAME)
            paragrafo_element.send_keys(datas.desc)
            self.chrome.driver.switch_to.default_content()
            
            if archives and len(archives) > 0:
                for archive in archives:
                    temp_dir = tempfile.mkdtemp()
                    temp_file_path = os.path.join(temp_dir, archive.name)
                    with open(temp_file_path, 'wb') as temp_file:
                        temp_file.write(archive.bts)
                    try:
                        input = self.chrome.get_element(self.name_input, By.NAME)
                        input.send_keys(temp_file_path)
                        self.chrome.progress_bar('uploadbar', By.CLASS_NAME)
                    except:
                        pass
                    os.remove(temp_file_path)    
        
            button = self.chrome.get_element(self.xpath_btn, By.XPATH)
            self.chrome.driver.execute_script("arguments[0].click();", button)
            message_group =  '*CHAMADO ABERTO NO GLPI* \n' + datas.desc.replace('\n', '')
            if self.chrome.driver.title != "Interface simplificada - GLPI": # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! warning
                raise Exception("Por algum motivo o chamado não foi finalizado")
            
            # if datas.reason == 'Criação de Login':
            #     matches = re.findall(r'\*(.*?)\*', datas.desc)
            #     for match in matches:
            #         text = match.strip()
            #         string_split_underscore = text.split('-')[1]
            #         string_split_virgula = string_split_underscore.split(',')
            #         name = string_split_virgula[0][1:]
            #         cpf = string_split_virgula[1][1:]
            #         cargo = string_split_virgula[2][1:]
            #         objeto_json = {"name": name, "cpf": cpf, "cargo": cargo, "contact": datas.contact}
            #         json_codificado = base64.b64encode(json.dumps(objeto_json).encode('utf-8')).decode('utf-8')
            #         message = f"\n*Acesse o link abaixo para criar automaticamente*\nhttp://192.168.1.232:8005/sso/{json_codificado}"
                    # message_group += message

            return ResponseController(True, message_group)

        except Exception as e:
            self.chrome.driver.close()
            return ResponseController(False, "ERROR OPEN REQUEST - " + str(e))
