import os

DATA_DIR = ('/home/rafael/Documentos/IGTI - Análise de Inteligência de '
            'Negócio/TCC/dados/')  # type: str


def data_file(ano: int, UF: str, subfolder: str = '',
              filename: str = '') -> str:
    ''' Retorna o path para um arquivo de dados de um dado ano e estado. '''
    path = os.path.join(DATA_DIR, str(ano), subfolder,
                        filename.format(ano, UF))
    return path
