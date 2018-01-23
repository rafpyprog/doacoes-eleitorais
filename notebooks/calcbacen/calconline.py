import locale
import re
import unicodedata
import time
from urllib.parse import unquote

import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from requests_futures.sessions import FuturesSession
import grequests
import numpy as np
import pandas as pd
import requests

locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')


def parse_valor_corrigido(soup):
    tab = soup.findAll('div', {'class': 'centralizado'})[0].find('table')
    texto_valor = tab.findAll('td')[-1].text
    valor = unicodedata.normalize('NFKD', texto_valor)
    valor = re.search('[0-9]+.*?(?=\s)', valor).group()
    return locale.atof(valor)


def check_for_error(soup):
    '''
    Verifica se a calculadora retornou alguma mensagem de erro para a
    pesquisa do usuário. Levanta exceção em caso de erro.
    '''

    erro = soup.findAll('div', {'class': 'msgErro'})
    if not erro:
        return False
    else:
        erro_txt = erro[0].text
        erro_txt = (unicodedata.normalize('NFKD', erro_txt)
                    .encode('utf-8')
                    .strip())
        raise(ValueError(erro_txt.strip()))


def corrigir_por_indice_preco(valor, data_inicial, data_final, indice):
    ''' Utiliza a Calculadora do Cidadão do Banco Central para atualizar um
    valor utilizando um índice de inflação.

    Parameters
    ----------
    valor: int or float
        Valor para atualização.
    data_inicial: str
        Data inicial no formato MM/AAAA.
    data_final: str
        Data final no formato MM/AAAA.
    indice: str
        Índices suportados pela calculadora:
            * IGP-DI     (a partir de 02/1944)
            * IGP-M      (a partir de 06/1989)
            * INPC       (a partir de 06/1979)
            * IPC-A      (a partir de 01/1980)
            * IPC-BRASIL (a partir de 01/19990)
            * IPC-SP     (a partir de 11/1942)
            * IPCA-E     (a partir de 01/1992)
    '''

    indices = {'IGP-DI': '00190IGP-DI',
               'IGP-M': '00189IGP-M',
               'INPC': '00188INPC',
               'IPC-A': '00433IPC-A',
               'IPC-BRASIL': '00191IPC-BRASIL',
               'IPC-SP': '00193IPC-SP',
               'IPCA-E': '10764IPC-E'}

    codigo_indice = indices[indice]

    URL = ('https://www3.bcb.gov.br/CALCIDADAO/publico/corrigirPorIndice.do?'
           'method=corrigirPorIndice')
    session = requests.Session()
    data = {'aba': '1',
            'selIndice': codigo_indice,
            'dataInicial': data_inicial,
            'dataFinal': data_final,
            'valorCorrecao': locale.format('%.2f', valor),
            'idIndice': '',
            'nomeIndicePeriodo': ''}

    response = session.post(URL, data=data)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'lxml')
    check_for_error(soup)
    valor_corrigido = parse_valor_corrigido(soup)
    return valor_corrigido





class CalcOnline():
    def __init__(self, max_workers=4):
        self.max_workers = max_workers
        self.indices = {'IGP-DI': '00190IGP-DI',
                        'IGP-M': '00189IGP-M',
                        'INPC': '00188INPC',
                        'IPC-A': '00433IPC-A',
                        'IPC-BRASIL': '00191IPC-BRASIL',
                        'IPC-SP': '00193IPC-SP',
                        'IPCA-E': '10764IPC-E'}
        self.URL = ('https://www3.bcb.gov.br/CALCIDADAO/publico/corrigirPorIndice.do?'
                    'method=corrigirPorIndice')

    def get_payload(self, valor, data_inicial, data_final, indice):
        codigo_indice = self.indices[indice]

        payload = {'aba': '1',
                   'selIndice': codigo_indice,
                   'dataInicial': data_inicial,
                   'dataFinal': data_final,
                   'valorCorrecao': locale.format('%.2f', valor),
                   'idIndice': '',
                   'nomeIndicePeriodo': ''}
        return payload

    def post_async(self, iterable):
        session = FuturesSession(executor=ThreadPoolExecutor(max_workers=self.max_workers))
        fs = [session.post(self.URL, data=self.get_payload(*i))
              for i in iterable]
        fs = concurrent.futures.as_completed(fs)

        valores = []

        for future in fs:
            resp = future.result()
            body = resp.request.body
            data = [unquote(i.split('=')[1]) for i in body.split('&')]
            soup = BeautifulSoup(resp.content, 'lxml')
            check_for_error(soup)
            valor_corrigido = parse_valor_corrigido(soup)
            valores.append([data[4], data[2], data[3], valor_corrigido])
        return valores

    def post_sync(self, valor, data_inicial, data_final, indice):
        valor = corrigir_por_indice_preco(valor, data_inicial, data_final, indice)
        return valor

#d = [[100, '01/2000', '01/2010', 'IPC-A']] * 10 + [[150, '01/2005', '01/2009', 'IPC-A']] * 10

#c = CalcOnline(10)
#r = c.post_async(d)
#print(r)
