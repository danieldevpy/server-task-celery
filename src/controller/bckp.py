import os

def encontrar_bckp_diretorio():
    diretorio_atual = os.getcwd()  # Obter o diretório atual

    diretorio_bckp = None
    
    for nome_arquivo in os.listdir(diretorio_atual):
        if os.path.isdir(nome_arquivo) and nome_arquivo == 'bckp':
            diretorio_bckp = os.path.join(diretorio_atual, nome_arquivo)
            break

    return diretorio_bckp

class BackupErros:

    @classmethod
    def save_image(cls, name: str, bt: bytes):
        path = encontrar_bckp_diretorio()
        print(path)
        with open(f'{path}/{name}', 'wb') as arquivo:
            arquivo.write(bt)


BackupErros.save_image('teste.png', b'teste')
