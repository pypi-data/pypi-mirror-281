import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import re
import math

def tjsp1(termos_de_busca, ano = None, data_inicio = None, data_fim = None):

    servico = Service(ChromeDriverManager().install())
    navegador = webdriver.Chrome(service=servico)
    navegador.get("https://esaj.tjsp.jus.br/cjpg/")

    wait = WebDriverWait(navegador, 10)

    elemento1 = navegador.find_element(By.XPATH, '//*[@id="iddadosConsulta.pesquisaLivre"]')
    elemento1.send_keys(termos_de_busca)

    if ano == 2024:
        print('does not support 2024 yet')
    elif ano != None:
        elemento2 = navegador.find_element(By.XPATH, '//*[@id="iddadosConsulta.dtInicio"]')
        elemento2.send_keys('01/01/' + ano)
        
        elemento3 = navegador.find_element(By.XPATH, '//*[@id="iddadosConsulta.dtFim"]')
        elemento3.send_keys('31/12/' + ano)
    elif (data_inicio != None) & (data_fim != None):
        elemento2 = navegador.find_element(By.XPATH, '//*[@id="iddadosConsulta.dtInicio"]')
        elemento2.send_keys(data_inicio)
            
        elemento3 = navegador.find_element(By.XPATH, '//*[@id="iddadosConsulta.dtFim"]')
        elemento3.send_keys(data_fim)

    botao_submit = navegador.find_element(By.XPATH, '//*[@id="pbSubmit"]')
    navegador.execute_script("arguments[0].click();", botao_submit)

    html = navegador.page_source
    soup = BeautifulSoup(html, 'html.parser')

    texto_geral = soup.find('div', attrs={'id': 'resultados'}).find('td')
    strong_text = texto_geral.find('strong').get_text().strip()
    td_text = texto_geral.get_text().strip()
    final_text = td_text.replace(strong_text, '').strip()
    final_text = re.sub(r'\D', '', final_text)

    numero_casos = int(final_text)
    numero_maximo_paginas = numero_casos/10
    numero_maximo_paginas = math.ceil(numero_maximo_paginas)

    info_decisoes = []

    for pagina_numero in range(1, numero_maximo_paginas + 1):
        print(str(pagina_numero)+"/"+str(numero_maximo_paginas))
        
        html = navegador.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        element = WebDriverWait(navegador, 120).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="divDadosResultado"]/table/tbody/tr[1]/td[2]/table/tbody/tr[1]/td'))  # Insira o XPath do elemento desejado aqui
        )
        
        lista_de_tr = soup.find('div', attrs={'id': 'divDadosResultado'}).find('table').find('tbody').find_all('tr', class_='fundocinza1')
        
        for tr in lista_de_tr:
            infos = tr.find("tbody").find_all("tr")

            num_processo = infos[0].find("a").text.strip() if infos[0].select_one('a') else ''
            classe = infos[1].select_one('td > strong').next_sibling.strip() if infos[1].select_one('td > strong') else ''
            assunto = infos[2].select_one('td > strong').next_sibling.strip() if infos[2].select_one('td > strong') else ''
            magistrado = infos[3].select_one('td > strong').next_sibling.strip() if infos[3].select_one('td > strong') else ''
            comarca = infos[4].select_one('td > strong').next_sibling.strip() if infos[4].select_one('td > strong') else ''
            foro = infos[5].select_one('td > strong').next_sibling.strip() if infos[5].select_one('td > strong') else ''
            vara = infos[6].select_one('td > strong').next_sibling.strip() if infos[6].select_one('td > strong') else ''
            data = infos[7].select_one('td > strong').next_sibling.strip() if infos[7].select_one('td > strong') else ''
            if len(infos) > 8:
                ementa_maior = infos[8].find("div", style='display: none;').text.strip() if infos[8].find("div", style='display: none;') else ''
            else:
                ementa_maior = ''
            
            info_decisoes.append([num_processo, classe, assunto, magistrado, comarca, foro, vara, data, ementa_maior])#, new_window_url])
        
        if pagina_numero == 1:
            numero_pagina = WebDriverWait(navegador, 120).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="resultados"]/table[1]/tbody/tr[1]/td[2]/div/a[1]'))  # Insira o XPath do elemento desejado aqui
            )
            numero_pagina.click()
        else:
            if pagina_numero == 2:
                numero_pagina = WebDriverWait(navegador, 120).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="resultados"]/table[1]/tbody/tr[1]/td[2]/div/a[3]'))  # Insira o XPath do elemento desejado aqui
                )
                numero_pagina.click()
            else:
                if pagina_numero == numero_maximo_paginas - 1:
                    numero_pagina = WebDriverWait(navegador, 120).until(
                        EC.visibility_of_element_located((By.XPATH, '//*[@id="resultados"]/table[1]/tbody/tr[1]/td[2]/div/a[5]'))  # Insira o XPath do elemento desejado aqui
                    )
                    numero_pagina.click()
                elif pagina_numero < numero_maximo_paginas:
                    numero_pagina = WebDriverWait(navegador, 180).until(
                        EC.visibility_of_element_located((By.XPATH, '//*[@id="resultados"]/table[1]/tbody/tr[1]/td[2]/div/a[4]'))  # Insira o XPath do elemento desejado aqui
                    )
                    numero_pagina.click()        
        time.sleep(4)

    return info_decisoes