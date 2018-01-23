import pandas as pd
from pandas.core.frame import DataFrame
import unidecode

from .common import data_file


#DATA_FILES = {2008: 'despesas_candidatos_{}_{}.txt',
#              2012: 'despesas_candidatos_{}_{}.txt',
#              2016: 'despesas_candidatos_{}_{}.txt'}


def dados_despesas(ano_eleicao: int, sigla_uf: str,
                   cod_municipio: int) -> DataFrame:
    datafile = 'despesas_candidatos_{}_{}.txt'
    filepath: str = data_file(ano_eleicao, sigla_uf, 'prestconta',
                              datafile)
    
    converters = {'Valor Despesa': float,                                 
                  'CPF/CNPJ do fornecedor': str,
                  'CPF do candidato': str}

    df: DataFrame = pd.read_csv(filepath, sep=';', encoding='Latin1',
                                header=0, names=None, decimal=',',
                                thousands='.',
                                converters=converters,
                                na_values=['#NULO', -1, '#NE', -3],
                                low_memory=False
                                )
    
    cols_to_rename = {    
                      'Sigla da UE': 'cod_municipio',      
                      'Número UE': 'cod_municipio',
                      'Nome da UE': 'nom_municipio',
                      'Município': 'nom_municipio',
                      }

    for col in cols_to_rename:
        df.rename(columns={col: cols_to_rename[col]}, inplace=True)

    # padroniza a nomenclatura das columnas
    new_names = []
    for col in df.columns:
        remove_accent = unidecode.unidecode(col).lower()
        words = remove_accent.split(' ')
        if len(words) > 1:            
            new_col_name = '_'.join(''.join(filter(lambda x: x.isalpha(), i))
                                    for i in words
                                    if len(i) > 2)
        else:
            new_col_name = remove_accent
        new_names.append(new_col_name)
    
    df.columns = new_names
    
    return df[df['cod_municipio'] == cod_municipio]





