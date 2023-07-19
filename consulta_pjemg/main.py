import os
import driver
import navegador
import time
import pandas as pd
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


INPUT_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'input')
OUTPUT_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'output')
CAMINHO_INPUT = os.path.join(INPUT_PATH, 'input.csv')

linhas_tabela = []
dados_polo_ativo = []
erro_busca = []

driver = driver.abrir_navegador()
df_input = pd.read_csv(CAMINHO_INPUT)
processos = df_input['PROCESSOS']
wait = WebDriverWait(driver, 10)

for lista in processos:      
        try:
            navegador.acessar_url(driver, 'https://pje-consulta-publica.tjmg.jus.br/')
            digitar_processo = navegador.aguardar_clicavel(driver, '//*[@id="fPP:numProcesso-inputNumeroProcessoDecoration:numProcesso-inputNumeroProcesso"]', tempo_espera=20)
            navegador.escrever(digitar_processo, lista)
            navegador.clicar(navegador.encontrar_elemento(driver, '//*[@id="fPP:searchProcessos"]'))
            time.sleep(10)
            navegador.clicar(navegador.encontrar_elemento(driver, "//a[@title='Ver Detalhes']"))
        except Exception as e:   
            print('Erro ao entrar no processo',lista,e)  
            erro_busca.append(lista)
        else:
            print('Processo', lista, 'encontrado!')
            wait.until(EC.number_of_windows_to_be(2))
            driver.switch_to.window(driver.window_handles[1])
            tabela_polo_ativo = navegador.encontrar_elemento(driver,'//*[@id="j_id132:processoPartesPoloAtivoResumidoList:tb"]')
            try: 
                linhas_tabela = tabela_polo_ativo.find_elements(By.TAG_NAME, 'tr')         
                for linhas in linhas_tabela:
                    if '(REQUERENTE)'in linhas.text:
                        dados_polo_ativo.append(lista + '-' + linhas.text)
                    else: 
                        dados_polo_ativo.append(linhas.text)
                if driver.title == "Detalhe do Processo · Processo Judicial Eletrônico - 1º Grau": 
                    time.sleep(2) 
                    driver.close() 
                    driver.switch_to.window(driver.window_handles[0])
                print('Dados do processo',lista,'coletados.')
            except Exception as e:
                print('Não foi possível coletar os dados do processo', lista, e)
                erro_busca.append(lista)
driver.close() 


dados_dict = {}
num_advogados = 0
requerentes = []
advogados = []
advogados_atual = []
LISTA_TERMOS_EXCLUIR = ['CPF:', 'CNPJ:']

for dado in dados_polo_ativo:
    if "(REQUERENTE)" in dado:
        requerente_info = dado.split("(REQUERENTE)\nAtivo")[0]
        requerente_parts = requerente_info.split("-")
        if len(requerente_parts) >=6:
            requerente = requerente_parts[2]  + '-' +  requerente_parts[3]
        else:
            requerente = requerente_parts[2]
        documento = requerente_parts[-2] + '-' +  requerente_parts[-1]
        for excluir in LISTA_TERMOS_EXCLUIR:
            documento = documento.replace(excluir, '')
        processo = requerente_parts[0] + '-' +  requerente_parts[1]
        requerentes.append(requerente)
        dados_dict[requerente] = {"Documento": documento, "Processo": processo}
        num_advogados = 0
    elif "(ADVOGADO)" in dado:
        num_advogados += 1
        advogado_info = dado.split("(ADVOGADO)\nAtivo")[0]
        advogado_parts = advogado_info.split("-")
        advogado = advogado_parts[0]
        if len(advogado_parts) >= 5:
            documento_adv =  advogado_parts[-2] + '-' + advogado_parts[-1]
        else:
            documento_adv =  advogado_parts[2] + '-' + advogado_parts[3]
        for excluir in LISTA_TERMOS_EXCLUIR:
            documento_adv = documento_adv.replace(excluir, '')
        oab = advogado_parts[1] 
        oab = oab.replace('OAB','')
        advogados.append(advogado)
        dados_dict[requerente][f"Advogado{num_advogados}"] = advogado
        dados_dict[requerente][f"Advogado{num_advogados}" + '-' + 'OAB'] = oab
        dados_dict[requerente][f"Advogado{num_advogados}" + '-' + 'Documento'] = documento_adv


df = pd.DataFrame.from_dict(dados_dict, orient='index')
df.to_excel(f'{OUTPUT_PATH}\\output_tratado.xlsx', engine='xlsxwriter', index_label='Beneficiário')
lista_erros = pd.DataFrame(erro_busca, columns=['Prcessos com Erro'])
lista_erros.drop_duplicates(subset=['Prcessos com Erro'], inplace=True)
lista_erros.to_excel(f'{OUTPUT_PATH}\\lista_erros.xlsx', engine='xlsxwriter', index=False)












