from numpy import double
from pandas.core.frame import DataFrame
import requests
import pandas as pd
import io
import locale
from itertools import compress
import datetime
from types_def import Urval


class DataAccess:
    block = [
        "Regering + stöd",
        "Regering + stöd",
        "Regering + stöd",
        "Regering + stöd",
        "Högeropposition",
        "Högeropposition",
        "Högeropposition",
        "Högeropposition",
    ]
    färger_partier = [
        "#B00000",
        "#ed1b34",
        "#83CF39",
        "#009933",
        "#6BB7EC",
        "#1B49DD",
        "#231977",
        "#dddd00",
    ]
    partier = ["V", "S", "MP", "C", "L", "M", "KD", "SD"]
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

    gräns_småparti = 6.0



    @staticmethod
    def hämta_data(start_datum: datetime.date=None):
        url = "https://raw.githubusercontent.com/hampusborgos/SwedishPolls/master/Data/Polls.csv"  # Make sure the url is the raw version of the file on GitHub
        download = requests.get(url).content

        # Reading the downloaded content and turning it into a pandas dataframe
        df = pd.read_csv(io.StringIO(download.decode("utf-8")))
        zip_iterator = zip(DataAccess.orginal_kolumner, DataAccess.kolumner)
        rename_dict = dict(zip_iterator)
        df = df[DataAccess.orginal_kolumner]
        df = df.rename(columns=rename_dict)
        df["Publiceringsdatum"] = pd.to_datetime(df["Publiceringsdatum"])
        if start_datum is not None:
            df = df[df["Publiceringsdatum"] > start_datum]
        df.set_index('Publiceringsdatum')
        df.sort_index(inplace=True, ascending=False)

        return df

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
        series = df[DataAccess.partier].apply("mean")
        return series

    @staticmethod
    def hämta_urval_enligt_30_dagars_medel(df: pd.DataFrame, över_gräns: bool, gräns: double):
        """ Returnerar filtrerad tidsserie, partier och färger baserat på om de är över gräns för småparti """

        serie = DataAccess.hämta_medelvärde_senaste_30_dagarna(df)

        if över_gräns == False:
            parti_urval_bool = list(serie > gräns)
        else:
            parti_urval_bool = list(serie < gräns)

        partier_urval = list(compress(DataAccess.partier, parti_urval_bool))
        färger_partier_urval = list(
            compress(DataAccess.färger_partier, parti_urval_bool)
        )
        up = Urval(färger_partier_urval, partier_urval)
        return up

    @staticmethod
    def hämta_urval_alla_partier():
        up = Urval(DataAccess.färger_partier, DataAccess.partier)
        return up

    @staticmethod
    def hämta_df_för_uppslag_block():
        df_uppslag_block = pd.DataFrame()
        df_uppslag_block["Parti"] = DataAccess.partier
        df_uppslag_block["Block"] = DataAccess.block
        return df_uppslag_block
