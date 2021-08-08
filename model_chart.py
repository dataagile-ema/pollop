from data_access import DataAccess
from data_access import Urval
from chart_by_block import ChartByBlockBar, ChartByBlockDateTimeSeries, ChartByBlockDateTimeSeries
from chart_by_block import ChartByBlockAddText
from chart_by_party import ChartByPartyDateTimeSeries
from chart_by_party import ChartByPartyMonthMeanTimeSeries
from charts_additions import Chart4PercentLineRule

import pandas as pd

class ModelChart:
    def __init__(self) -> None:
        self.df = DataAccess.hämta_data("2021-02-01")
        self.uv_små_partier = DataAccess.hämta_urval_enligt_30_dagars_medel(
            self.df, True, DataAccess.gräns_småparti
        )
        self.uv_större_partier = DataAccess.hämta_urval_enligt_30_dagars_medel(
            self.df, False, DataAccess.gräns_småparti
        )

        self.uv_alla_partier = DataAccess.hämta_urval_alla_partier()
        self.df_sista_30_dagar = DataAccess.ge_data_for_sista_30_dagarna(self.df)
        self.df_uppslag_block = DataAccess.hämta_df_för_uppslag_block()

    def visa_linje_små_partier(self):
        titel = "Opinionsdata för små partier"
        subtitel = ["Visar medel för kalendermånad"]

        chart_obj1 = ChartByPartyMonthMeanTimeSeries(data=self.df, title=titel, subtitle=subtitel, urval=self.uv_små_partier)
        c1 = chart_obj1.get_chart()

        chart_obj2 = Chart4PercentLineRule()
        c2 = chart_obj2.get_chart()

        exp = chart_obj1.assemple_charts((c1+c2), 14)
        return exp

    def visa_linje_större_partier(self):
        titel = "Opinionsdata för större partier"
        subtitel = ["Visar medel för kalendermånad"]

        chart_obj1 = ChartByPartyMonthMeanTimeSeries(data=self.df, title=titel, subtitle=subtitel, urval=self.uv_större_partier)
        c1 = chart_obj1.get_chart()

        exp = chart_obj1.assemple_charts((c1), 14)
        return exp


    def visa_spridningsdiagram_små_partier(self):
        titel = "Opinionsdata för små partier"
        subtitel = ["Visar alla opinionsundersökningar"]

        chart_obj1 = ChartByPartyDateTimeSeries(data=self.df, title=titel, subtitle=subtitel, urval=self.uv_små_partier)
        c1 = chart_obj1.get_chart()

        chart_obj2 = Chart4PercentLineRule()
        c2 = chart_obj2.get_chart()

        exp = chart_obj1.assemple_charts((c1+c2), 14)
        return exp

    def visa_spridningsdiagram_större_partier(self):
        titel = "Opinionsdata för större partier"
        subtitel = ["Visar alla opinionsundersökningar"]

        chart_obj1 = ChartByPartyDateTimeSeries(data=self.df, title=titel, subtitle=subtitel, urval=self.uv_större_partier)
        c1 = chart_obj1.get_chart()

        exp = chart_obj1.assemple_charts((c1), 14)
        return exp


    def visa_block_som_stacked_bar_30_dagars_medel(self):
        subtitel = ["Visar medel för de senaste 30 dagarna"]
        df_data = self.df_sista_30_dagar

        exp = self.__visa_block_som_stacked_bar(subtitel, df_data)
        return exp

    def visa_block_som_stacked_bar_senaste_undesökning(self):
        subtitel = ["Visa senaste opinionsundersökning"]
        df_data = self.df.head(1)
        exp = self.__visa_block_som_stacked_bar(subtitel, df_data)
        return exp

    def __visa_block_som_stacked_bar(self, subtitel, df_data):
        titel = "Opinionsdata för block"

        chart_obj1 = ChartByBlockBar(
            data=df_data,
            title=titel,
            subtitle=subtitel,
            urval=self.uv_alla_partier,
            lookup_block=self.df_uppslag_block,
        )
        c1 = chart_obj1.get_chart()
        chart_obj2 = ChartByBlockAddText(
            data=df_data,
            urval=self.uv_alla_partier,
            lookup_block=self.df_uppslag_block,
        )
        c2 = chart_obj2.get_chart()
        exp = chart_obj1.assemple_charts((c1 + c2), 14)
        return exp
    
    def visa_linje_för_block(self):
        titel = "Opinionsdata för block"
        subtitel = ["Visar medel per datum"]

        chart_obj1 = ChartByBlockDateTimeSeries(title=titel, subtitle=subtitel, data=self.df, urval=self.uv_alla_partier, lookup_block=self.df_uppslag_block)
        c1 = chart_obj1.get_chart()
        exp = chart_obj1.assemple_charts((c1), labelfont_size=14)
        return exp

    @staticmethod
    def ge_meddelande_om_dagar_kvar_till_valet():
        dagar = DataAccess.ge_dagar_kvar_till_valet()
        return f"Dagar till valet: {dagar}"
