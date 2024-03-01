import re

string = """ 

    Solicitante: Daniel Fernandes

    Unidade: CENTRAL SAMU

    

    Solicita: Criação de Login - * Sistema SSO - Daniel Fernandes Pereira, 18714933748, Enfermeiro *

    

    Contato: 21991920338.

"""
matches = re.findall(r'\*(.*?)\*', string)

# Imprimindo os resultados encontrados
for match in matches:
    text = match.strip()
    string_split_underscore = text.split('-')[1]
    string_split_virgula = string_split_underscore.split(',')
    name = string_split_virgula[0][1:]
    cpf = string_split_virgula[1][1:]
    cargo = string_split_virgula[2][1:]
    print(name, cpf, cargo)

# pattern = r'Sistema SSO'

# matches = re.findall(pattern, string)

# for match in matches:
#     match = re.search(pattern, string)
#     if match:
#         string_match = string[match.start():]
#         string_split_underscore = string_match.split('-')[1]
#         string_split_virgula = string_split_underscore.split(',')
#         print(string_split_virgula)
#         name = string_split_virgula[0][1:]
#         cpf = string_split_virgula[1][1:]
#         cargo = string_split_virgula[2][1:]
#         print(cargo)