#!/bin/sh

#############################################################################
# Candidatos: Informações acerca do perfil dos candidatos nas eleições
# Eleitorado: Informações acerca do perfil do eleitorado de cada pleito
# Prestação de Contas: Contas (receitas e despesas de campanha) de candidatos,
#                      de partidos e de comitês. 
# Resultados: Votação nominal por município e zona eleitoral.
##############################################################################

clear

ANO=$1


echo 'TSE - Repositório de dados eleitorais - Ano base: '${ANO}
echo '------------------------------------------------------\n'

# Cria a estrutura de pastas de repositório de dados
DIR_CANDIDATOS=$ANO/candidatos
DIR_RESULTADOS=$ANO/resultados
DIR_PRESTCONTA=$ANO/prestconta
DIR_ELEITORADO=$ANO/eleitorado

mkdir -p $DIR_CANDIDATOS \
	 $DIR_RESULTADOS \
	 $DIR_PRESTCONTA \
	 $DIR_ELEITORADO

ls ./$ANO -R | grep ":$" | sed -e 's/:$//' -e 's/[^-][^\/]*\//--/g' -e 's/^/   /' -e 's/-/|/'
echo ' \n'

URL_REPOSITORIO=http://agencia.tse.jus.br/estatistica/sead/odsele 

URL_CANDIDATOS=${URL_REPOSITORIO}/consulta_cand/consulta_cand_${ANO}.zip

URL_RESULTADOS=${URL_REPOSITORIO}/votacao_partido_munzona/votacao_partido_munzona_${ANO}.zip


if [ "$ANO" -lt 2012 ]; then
    filename=prestacao_contas_${ANO}.zip
else
    filename=prestacao_contas_final_${ANO}.zip	
fi

URL_PRESTCONTA=${URL_REPOSITORIO}/prestacao_contas/${filename} 
URL_ELEITORADO=${URL_REPOSITORIO}/perfil_eleitorado/perfil_eleitorado_${ANO}.zip


echo Realizando download dos dados
echo [1/4] $URL_CANDIDATOS & curl --progress-bar -o ./$DIR_CANDIDATOS/canditados.zip $URL_CANDIDATOS
echo [2/4] $URL_RESULTADOS & curl --progress-bar -o ./$DIR_RESULTADOS/resultados.zip $URL_RESULTADOS
echo [3/4] $URL_ELEITORADO & curl --progress-bar -o ./$DIR_ELEITORADO/eleitorado.zip $URL_ELEITORADO 
echo [4/4] $URL_PRESTCONTA & curl --progress-bar -o ./$DIR_PRESTCONTA/prestconta.zip $URL_PRESTCONTA



echo 'Descompactando arquivos'
unzip ./$ANO/candidatos/canditados.zip -d $DIR_CANDIDATOS
unzip ./$ANO/resultados/resultados.zip -d $DIR_RESULTADOS
unzip ./$ANO/eleitorado/eleitorado.zip -d $DIR_ELEITORADO
unzip ./$ANO/prestconta/prestconta.zip -d $DIR_PRESTCONTA
