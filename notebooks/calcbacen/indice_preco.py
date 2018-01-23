import locale
import re
import unicodedata

from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import requests

locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')


def parse_valor_corrigido(soup):
    tab = soup.findAll('div', {'class': 'centralizado'})[0].find('table')
    return tab
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


class CalculadoraBacen():
    def __init__(self):
        self.file_serie_temporal = 'STP-20180121060223947.csv'
        self.serie_temporal = self.load_serie_temporal()

    def load_serie_temporal(self):
        serie_temporal = pd.read_csv('STP-20180121060223947.csv', sep=';',
                                     index_col=0, squeeze=True,
                                     encoding='Latin1',
                                     converters={1: locale.atof},
                                     skipfooter=1, engine='python')
        return serie_temporal

    def corrige_IPCA(self, valor, data_inicial, data_final):
        indices = self.serie_temporal[data_inicial: data_final] / 100 + 1
        indice_periodo = np.prod(indices.values)
        return indice_periodo * valor
