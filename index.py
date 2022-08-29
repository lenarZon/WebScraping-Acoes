import csv
import imp
import requests
import pandas as pd
from bs4 import BeautifulSoup

# Variaveis globais
masterurl = "" # URL do Scraping
arq_temp = "" # Caminho do arquivo temporario
arq = "" # Arquivo Final
pathfile = "" # Arquivo dos ativos
param = "" # Responsavel por raspar os dados pelo tema desejado ( Fi ou Acao)
           # param = "Range" + input("Digite o tipo de ativo")
           # Com isso pegará o valores das classes do site


# Inicio do código
def replaceText(textvalue):   
    textvalue = textvalue.replace("%","").replace(",",'.').replace("-",'0')
    return textvalue


def myFile(url, param, pathfile):

    # Parametros dos valores
    tableValues = {
        'ColumnsAcao': ['DY', 'PL', 'PVP', 'DV', 'ML', 'ROE', 'ROIC'],
        'RangeAcao': [10, 11, 13, 25, 33, 34, 36],
        'RangeFi': [3, None, None, None, None, None, None]
    }


    # Começo do WebScraping
    with open(pathfile, newline='') as file:
         file_reader = csv.reader(file)
         listfile = list(file_reader)

         # Loop
         for iAcao in listfile:
            for listen in iAcao:

                cod = url + listen.lower()
                site = requests.get(cod)
                soup = BeautifulSoup(site.content, 'html.parser')
                values = soup.find_all('strong', class_='value')  # Valores do Container

                # Pandas
                t_df = pd.DataFrame(tableValues) # Temporario
                df = t_df.dropna(subset = param) # Removendo os nulos

                for index, row in df.iterrows():
                    headers = row['ColumnsAcao']
                    dados = replaceText( values[int(row[param])].get_text().strip() )

                    # Todos os valores acima de 100.000, sera inserido como 1000
                    if len(dados) > 7:
                        dados = '1000'
                    else:
                        dados

                    with open(arq_temp, 'a', encoding="utf-8") as f:
                        result = listen + ';' + headers + ';' + dados + '\n'
                        print(listen.upper() + ' sendo gravado!')
                        f.write(result)
# Chamando a função
myFile(masterurl, param, pathfile)

# Transformando e gravando o csv 
columns_data = [] # Colunas do arquivo
df = pd.read_csv(arq_temp, sep=";")
df.columns = columns_data
table = df.pivot_table(values='VALORES',index=['CodigoAcao'], columns='INDICADOR')
table.to_csv(arq, index=True)

# Truncando os dados
f = open(arq_temp, "w+")
f.close()





