import pandas as pd
import requests
from bs4 import BeautifulSoup

rename_columns = {'Códigodo fundo':'codigodofundo',
                  'Preço Atual':'precoatual',
                  'Liquidez Diária':'liquidezdiaria',
                  'DY (3M)Acumulado':'dy3acum',
                  'DY (6M)Acumulado':'dy6acum',
                  'DY (12M)Acumulado':'dy12acum',
                  'DY (3M)Média':'dy3med',
                  'DY (6M)Média':'dy6med',
                  'DY (12M)Média':'dy12med',
                  'DY Ano':'dyano',
                  'Variação Preço':'variacaopreco',
                  'Rentab.Período':'rentperiodo',
                  'Rentab.Acumulada':'rentacumulada',
                  'PatrimônioLíq.':'patrimonioliquido',
                  'VariaçãoPatrimonial':'variacaopatrimonial',
                  'Rentab. Patr.no Período':'rentpatrperiodo',
                  'Rentab. Patr.Acumulada':'rentpatracumulada',
                  'VacânciaFísica':'vacanciafisica',
                  'VacânciaFinanceira':'vacanciafinanceira'}

fii_keys = ['codigodofundo', 'Setor', 'precoatual', 'liquidezdiaria', 'Dividendo',
       'DividendYield', 'dy3acum', 'dy6acum', 'dy12acum', 'dy3med', 'dy6med',
       'dy12med', 'dyano', 'variacaopreco', 'rentperiodo', 'rentacumulada',
       'patrimonioliquido', 'VPA', 'P/VPA', 'DYPatrimonial',
       'variacaopatrimonial', 'rentpatrperiodo', 'rentpatrperiodo',
       'vacanciafisica', 'vacanciafinanceira', 'QuantidadeAtivos']

float_columns = {'precoatual':'float64', 'liquidezdiaria':'float64', 'Dividendo':'float64',
                 'DividendYield':'float64', 'dy3acum':'float64', 'dy6acum':'float64',
                 'dy12acum':'float64','dy3med':'float64', 'dy6med':'float64',
                 'dy12med':'float64', 'dyano':'float64', 'variacaopreco':'float64',
                 'rentperiodo':'float64', 'rentacumulada':'float64','patrimonioliquido':'float64',
                 'VPA':'float64', 'P/VPA':'float64', 'DYPatrimonial':'float64',
                 'variacaopatrimonial':'float64', 'rentpatrperiodo':'float64', 'rentpatrperiodo':'float64',
                 'vacanciafisica':'float64', 'vacanciafinanceira':'float64', 'QuantidadeAtivos':'float64'}

class GetData:

    def __init__(self,url):
        self.url = url
        self.response = requests.get(self.url)
        if self.CheckResponse(self.response):
            self.df = self.FormatData(self.response)
        else:
            print("Erro de requisição")

    def __str__(self):
        return str(self.df)

    def CheckResponse(self,response):
        if response.status_code == 200:
            return True
        else:
            return False

    def CheckKey(self,key):
        return self.df[key]

    def ReturnFundsCode(self):
        return self.df["codigodofundo"]

    def info(self):
        return self.df

    def ReturnHeader(self):
        return self.df.keys()

    def SelectCodeInfo(self, fundo):
        return self.df[self.df["codigodofundo"] == fundo]



    def FormatData(self,response):
        soup = BeautifulSoup(response.text, 'lxml')
        table = soup.find_all('table')[0]
        df = pd.read_html(str(table), decimal=',', thousands='.')[0]
        df_rename = df.rename(columns=rename_columns, inplace=False)

        for key in fii_keys:
            if df_rename[key].dtypes == object:
                df_rename[key] = df_rename[key].str.replace("R\$", "", regex=True)
                df_rename[key] = df_rename[key].str.replace(".", "", regex=True)
                df_rename[key] = df_rename[key].str.replace(",", ".", regex=True)
                df_rename[key] = df_rename[key].str.replace("inf", "", regex=True)
                df_rename[key] = df_rename[key].str.replace("\%", "", regex=True)

        df_rename.astype(float_columns)

        df_rename["liquidezdiaria"] = df_rename["liquidezdiaria"] / 10

        return df_rename

if __name__ == '__main__':
    url = 'https://www.fundsexplorer.com.br/ranking'
    print("Executando backend")
    FII = GetData(url)
    df_list = FII.info()
    header = FII.ReturnHeader()
    lista_de_fundos = FII.ReturnFundsCode()
    fundo = FII.SelectCodeInfo(lista_de_fundos[2])


