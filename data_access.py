from numpy import double
from pandas.core.frame import DataFrame
import requests
import pandas as pd
import io
import locale
from itertools import compress
import datetime
from grunddata import Grunddata


orginal_kolumner = [
    "M",
    "L",
    "C",
    "KD",
    "S",
    "V",
    "MP",
    "SD",
    "PublDate",
    "collectPeriodFrom",
    "collectPeriodTo",
    "house",
]
kolumner = [
    "M",
    "L",
    "C",
    "KD",
    "S",
    "V",
    "MP",
    "SD",
    "Publiceringsdatum",
    "Insamlingsdatum_fr_o_m",
    "Insamlingsdatum_t_o_m",
    "Institut",
]

visa_kolumner = [
    "Publiceringsdatum",
    "V",
    "S",
    "MP",
    "C",
    "L",
    "M",
    "KD",
    "SD",
    "Insamlingsdatum_fr_o_m",
    "Insamlingsdatum_t_o_m",
    "Institut",
]

class DataAccess:
    @staticmethod
    def hämta_data(start_datum: datetime.date=None):
 
        #url = "https://raw.githubusercontent.com/MansMeg/SwedishPolls/master/Data/Polls.csv" 
        url = "https://raw.githubusercontent.com/dataagile-ema/SwedishPolls/master/Data/Polls.csv"
        download = requests.get(url).content
        # Reading the downloaded content and turning it into a pandas dataframe
        df = pd.read_csv(io.StringIO(download.decode("utf-8")))
        
        #df = pd.read_csv("polls.csv")
        zip_iterator = zip(orginal_kolumner, kolumner)
        rename_dict = dict(zip_iterator)
        df = df[orginal_kolumner]
        df = df.rename(columns=rename_dict)
        df["Publiceringsdatum"] = pd.to_datetime(df["Publiceringsdatum"])
        df = df.reindex(columns=visa_kolumner)
        if start_datum is not None:
            df = df[df["Publiceringsdatum"] > start_datum]
        df.set_index('Publiceringsdatum')
        df.sort_index(inplace=True, ascending=False)

        return df

    @staticmethod 
    def skapa_rullande_medel(data: pd.DataFrame, window: int):
        df_rol = data.set_index('Publiceringsdatum')
        df_rol = df_rol.rolling(window).mean()
        df_rol.reset_index(inplace=True)
        df_rol = df_rol[df_rol["Publiceringsdatum"] > '2021-02-01']
        return df_rol

    @staticmethod 
    def ge_data_for_sista_30_dagarna(df: pd.DataFrame):
        datum_30_dagar_sedan = pd.to_datetime("today") + pd.DateOffset(-30)
        df = df[df["Publiceringsdatum"] > datum_30_dagar_sedan]
        return df

    @staticmethod
    def ge_dagar_kvar_till_valet():
        idag = pd.to_datetime("today")
        valdag = pd.to_datetime("2022-09-11")
        antal_dagar_till_valet = (valdag - idag).days + 1
        return antal_dagar_till_valet

    @staticmethod
    def hämta_medelvärde_senaste_30_dagarna(df: pd.DataFrame):
        df = DataAccess.ge_data_for_sista_30_dagarna(df)
        series = df[Grunddata.partier].apply("mean")
        return series


    @staticmethod
    def hämta_df_för_uppslag_block():
        df_uppslag_block = pd.DataFrame()
        df_uppslag_block["Parti"] = Grunddata.partier
        df_uppslag_block["Block"] = Grunddata.block_för_parti
        return df_uppslag_block
