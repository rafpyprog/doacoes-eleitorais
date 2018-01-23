import os
from typing import Dict, List

import pandas as pd
from pandas.core.frame import DataFrame
from .common import data_file

CANDIDATOS_FILE = 'consulta_cand_{}_{}.txt'  # type: str


class LayoutArquivo():
    layouts = {2008: ['DATA_GERACAO', 'HORA_GERACAO', 'ANO_ELEICAO',
                      'NUM_TURNO', 'DESC_ELEICAO', 'SIGLA_UF', 'SIGLA_UE',
                      'DESC_UE', 'COD_CARGO', 'DESC_CARGO', 'NOME_CANDIDATO',
                      'SEQUENCIAL_CANDIDATO', 'NUMERO_CANDIDATO',
                      'CPF_CANDIDATO', 'NOME_URNA_CANDIDATO',
                      'COD_SITUACAO_CANDIDATURA', 'DESC_SITUACAO_CANDIDATURA',
                      'NUM_PARTIDO', 'SIGLA_PARTIDO', 'NOME_PARTIDO',
                      'COD_LEGENDA', 'SIGLA_LEGENDA', 'COMPOSICAO_LEGENDA',
                      'NOME_LEGENDA', 'COD_OCUPACAO', 'DESC_OCUPACAO',
                      'DATA_NASCIMENTO', 'NUM_TITULO_ELEITORAL_CANDIDATO',
                      'IDADE_DATA_ELEICAO', 'COD_SEXO', 'DESC_SEXO',
                      'COD_GRAU_INSTRUCAO', 'DESC_GRAU_INSTRUCAO',
                      'COD_ESTADO_CIVIL', 'DESC_ESTADO_CIVIL',
                      'CODIGO_NACIONALIDADE', 'DESC_NACIONALIDADE',
                      'SIGLA_UF_NASCIMENTO', 'COD_MUNICIPIO_NASCIMENTO',
                      'NOME_MUNICIPIO_NASCIMENTO', 'DESPESA_MAX_CAMPANHA',
                      'COD_SIT_TOT_TURNO', 'DESC_SIT_TOT_TURNO'],
                2010: ['DATA_GERACAO', 'HORA_GERACAO', 'ANO_ELEICAO',
                      'NUM_TURNO', 'DESC_ELEICAO', 'SIGLA_UF', 'SIGLA_UE',
                      'DESC_UE', 'COD_CARGO', 'DESC_CARGO', 'NOME_CANDIDATO',
                      'SEQUENCIAL_CANDIDATO', 'NUMERO_CANDIDATO',
                      'NOME_URNA_CANDIDATO',
                      'COD_SITUACAO_CANDIDATURA', 'DESC_SITUACAO_CANDIDATURA',
                      'NUM_PARTIDO', 'SIGLA_PARTIDO', 'NOME_PARTIDO',
                      'COD_LEGENDA', 'SIGLA_LEGENDA', 'COMPOSICAO_LEGENDA',
                      'NOME_LEGENDA', 'COD_OCUPACAO', 'DESC_OCUPACAO',
                      'DATA_NASCIMENTO', 'NUM_TITULO_ELEITORAL_CANDIDATO',
                      'IDADE_DATA_ELEICAO', 'COD_SEXO', 'DESC_SEXO',
                      'COD_GRAU_INSTRUCAO', 'DESC_GRAU_INSTRUCAO',
                      'COD_ESTADO_CIVIL', 'DESC_ESTADO_CIVIL',
                      'CODIGO_NACIONALIDADE', 'DESC_NACIONALIDADE',
                      'SIGLA_UF_NASCIMENTO', 'COD_MUNICIPIO_NASCIMENTO',
                      'NOME_MUNICIPIO_NASCIMENTO', 'DESPESA_MAX_CAMPANHA',
                      'COD_SIT_TOT_TURNO', 'DESC_SIT_TOT_TURNO'],
               # Em 2012 for acrescentado o campo de email e cpf
               2012: ['DATA_GERACAO', 'HORA_GERACAO', 'ANO_ELEICAO',
                      'NUM_TURNO', 'DESC_ELEICAO', 'SIGLA_UF', 'SIGLA_UE',
                      'DESC_UE', 'COD_CARGO', 'DESC_CARGO', 'NOME_CANDIDATO',
                      'SEQUENCIAL_CANDIDATO', 'NUMERO_CANDIDATO',
                      'CPF_CANDIDATO', 'NOME_URNA_CANDIDATO',
                      'COD_SITUACAO_CANDIDATURA', 'DESC_SITUACAO_CANDIDATURA',
                      'NUM_PARTIDO', 'SIGLA_PARTIDO', 'NOME_PARTIDO',
                      'COD_LEGENDA', 'SIGLA_LEGENDA', 'COMPOSICAO_LEGENDA',
                      'NOME_LEGENDA', 'COD_OCUPACAO', 'DESC_OCUPACAO',
                      'DATA_NASCIMENTO', 'NUM_TITULO_ELEITORAL_CANDIDATO',
                      'IDADE_DATA_ELEICAO', 'COD_SEXO', 'DESC_SEXO',
                      'COD_GRAU_INSTRUCAO', 'DESC_GRAU_INSTRUCAO',
                      'COD_ESTADO_CIVIL', 'DESC_ESTADO_CIVIL',
                      'CODIGO_NACIONALIDADE', 'DESC_NACIONALIDADE',
                      'SIGLA_UF_NASCIMENTO', 'COD_MUNICIPIO_NASCIMENTO',
                      'NOME_MUNICIPIO_NASCIMENTO', 'DESPESA_MAX_CAMPANHA',
                      'COD_SIT_TOT_TURNO', 'DESC_SIT_TOT_TURNO', 'NM_EMAIL'],
               # Em 2014 foi acrescentada a informação de cor/raça
               2014: ['DATA_GERACAO', 'HORA_GERACAO', 'ANO_ELEICAO',
                      'NUM_TURNO', 'DESC_ELEICAO', 'SIGLA_UF', 'SIGLA_UE',
                      'DESC_UE', 'COD_CARGO', 'DESC_CARGO', 'NOME_CANDIDATO',
                      'SEQUENCIAL_CANDIDATO', 'NUMERO_CANDIDATO',
                      'CPF_CANDIDATO', 'NOME_URNA_CANDIDATO',
                      'COD_SITUACAO_CANDIDATURA', 'DESC_SITUACAO_CANDIDATURA',
                      'NUM_PARTIDO', 'SIGLA_PARTIDO', 'NOME_PARTIDO',
                      'COD_LEGENDA', 'SIGLA_LEGENDA', 'COMPOSICAO_LEGENDA',
                      'NOME_LEGENDA', 'COD_OCUPACAO', 'DESC_OCUPACAO',
                      'DATA_NASCIMENTO', 'NUM_TITULO_ELEITORAL_CANDIDATO',
                      'IDADE_DATA_ELEICAO', 'COD_SEXO', 'DESC_SEXO',
                      'COD_GRAU_INSTRUCAO', 'DESC_GRAU_INSTRUCAO',
                      'COD_ESTADO_CIVIL', 'DESC_ESTADO_CIVIL',
                      'COD_COR_RACA', 'DESC_COR_RACA', 'CODIGO_NACIONALIDADE',
                      'DESC_NACIONALIDADE', 'SIGLA_UF_NASCIMENTO',
                      'COD_MUNICIPIO_NASCIMENTO', 'NOME_MUNICIPIO_NASCIMENTO',
                      'DESPESA_MAX_CAMPANHA', 'COD_SIT_TOT_TURNO',
                      'DESC_SIT_TOT_TURNO', 'NM_EMAIL']
               }  # type: Dict[int, list]

    def __init__(self, ano: int) -> None:        
        if ano == 2004:
            self.colunas = self.layouts[2008]
        if ano == 2008:
            self.colunas = self.layouts[2008]
        if ano == 2010:
            self.colunas = self.layouts[2010]
        if ano == 2012:
            self.colunas = self.layouts[2012]
        if ano > 2012:
            self.colunas = self.layouts[2014]


def dados_candidatos(ano_eleicao: int, sigla_uf: str,
                     sigla_ue: int) -> DataFrame:
    filepath: str = data_file(ano_eleicao, sigla_uf, 'candidatos', CANDIDATOS_FILE)
    names: List[str] = LayoutArquivo(ano_eleicao).colunas
    converters = {'NUM_TITULO_ELEITORAL_CANDIDATO': str,
                  'CPF_CANDIDATO': str,
                }
    df: DataFrame = pd.read_csv(filepath, sep=';', encoding='Latin1',
                                header=None, names=names,
                                converters=converters,
                                na_values=['#NULO#', -1, '#NE', -3],
                                low_memory=False, dayfirst=True,
                                skipinitialspace=True)

    return df.query('SIGLA_UE == @sigla_ue')
