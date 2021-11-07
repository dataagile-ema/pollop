from grunddata import Grunddata
from data_access import DataAccess
from itertools import compress
from numpy import double
import pandas as pd

class UrvalsLista:
    def __init__(self, färger_partier_urval, partier_urval) -> None:
        self.färger_partier_urval = färger_partier_urval
        self.partier_urval = partier_urval

class Urval:
    @staticmethod
    def hämta_urval_enligt_30_dagars_medel(df: pd.DataFrame, över_gräns: bool, gräns: double):
        """ Returnerar filtrerad tidsserie, partier och färger baserat på om de är över gräns för småparti """
        medelvärde_per_parti = DataAccess.hämta_medelvärde_senaste_30_dagarna(df)

        if över_gräns == False:
            parti_urval_bool = list(medelvärde_per_parti > gräns)
        else:
            parti_urval_bool = list(medelvärde_per_parti < gräns)

        # filter Grunddata.parter from parti_urval_bool
        partier_urval = list(compress(Grunddata.partier, parti_urval_bool))
        färger_partier_urval = list(compress(Grunddata.färg_för_parti, parti_urval_bool))        

        up = UrvalsLista(färger_partier_urval, partier_urval)
        return up

    @staticmethod
    def hämta_urval_alla_partier():
        up = UrvalsLista(Grunddata.färg_för_parti, Grunddata.partier)
        return up

    @staticmethod
    def hämta_urval_för_block(block_namn: str):
        # index for all högeropposition in block
        index_partier_för_block = [i for i, x in enumerate(Grunddata.block_för_parti) if x == block_namn]
        # list of partier in index
        partier = [Grunddata.partier[i] for i in index_partier_för_block]
        # create list of färger in aktuelltblock_index
        färger = [Grunddata.färg_för_parti[i] for i in index_partier_för_block]
        return UrvalsLista(färger, partier)