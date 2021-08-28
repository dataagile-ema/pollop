from data_access import DataAccess
from data_access import Urval
from chart_by_block import ChartByBlockBar, ChartByBlockDateTimeSeries, ChartByBlockDateTimeSeries, ChartByBlockDateTimeSeriesLine
from chart_by_block import ChartByBlockAddText
from chart_by_party import ChartByPartyDateTimeSeries, ChartByPartyDateTimeSeriesLine
from chart_by_party import ChartByPartyMonthMeanTimeSeries
from charts_additions import Chart4PercentLineRule


import pandas as pd



class ModelChart:
    def __init__(self, dagar_kar_text: str) -> None:
        self.dagar_kvar_text = dagar_kar_text
        self.df = DataAccess.hämta_data("2021-02-01")
        self.df_rullande_4 = DataAccess.skapa_rullande_df(DataAccess.hämta_data("2021-01-01"), 4)
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
        subtitel = ["Medel för kalendermånad"]

        chart_obj1 = ChartByPartyMonthMeanTimeSeries(self.df, title=titel, subtitle=subtitel, urval=self.uv_små_partier)
        c1 = chart_obj1.get_chart()

        chart_obj2 = Chart4PercentLineRule()
        c2 = chart_obj2.get_chart()

        exp = chart_obj1.assemple_charts((c1+c2), 14)
        return exp

    def visa_linje_större_partier(self):
        titel = "Opinionsdata för större partier"
        subtitel = ["Medel för kalendermånad"]

        chart_obj1 = ChartByPartyMonthMeanTimeSeries(self.df, title=titel, subtitle=subtitel, urval=self.uv_större_partier)
        c1 = chart_obj1.get_chart()

        exp = chart_obj1.assemple_charts((c1), 14)
        return exp

    def visa_spridningsdiagram_små_partier(self):
        titel = "Opinionsdata för små partier"
        subtitel = ["Alla opinionsundersökningar"]

        chart_obj1 = Chart4PercentLineRule()
        c1 = chart_obj1.get_chart()

        chart_obj2 = ChartByPartyDateTimeSeriesLine(data=self.df_rullande_4, title=titel, subtitle=subtitel, urval=self.uv_små_partier)
        c2 = chart_obj2.get_chart()

        chart_obj3 = ChartByPartyDateTimeSeries(data=self.df, title=titel, subtitle=subtitel, urval=self.uv_små_partier)
        c3 = chart_obj3.get_chart()

        exp = chart_obj3.assemple_charts((c1+c2+c3), 14)
        return exp

    def visa_spridningsdiagram_större_partier(self):
        titel = "Opinionsdata för större partier"
        subtitel = ["Alla opinionsundersökningar"]

        chart_obj1 = ChartByPartyDateTimeSeriesLine(data=self.df_rullande_4, title=titel, subtitle=subtitel, urval=self.uv_större_partier)
        c1 = chart_obj1.get_chart()

        chart_obj2 = ChartByPartyDateTimeSeries(data=self.df, title=titel, subtitle=subtitel, urval=self.uv_större_partier)
        c2 = chart_obj2.get_chart()

        exp = chart_obj1.assemple_charts((c1+c2), 14)
        return exp


    def visa_block_som_stacked_bar_30_dagars_medel(self):
        subtitel = ["Medel för de senaste 30 dagarna"]
        df_data = self.df_sista_30_dagar

        exp = self.__visa_block_som_stacked_bar(subtitel, df_data)
        return exp

    def visa_block_som_stacked_bar_senaste_4_undesökningar(self, spärr: bool):
        subtitel = ["Medel fyra senaste undersökningarna"]
        df_data = self.df.tail(4)
        exp = self.__visa_block_som_stacked_bar(subtitel, df_data, spärr)
        return exp

    def __visa_block_som_stacked_bar(self, subtitel, df_data, spärr):
        titel = "Opinionsdata för block"

        chart_obj1 = ChartByBlockBar(
            data=df_data,
            title=titel,
            subtitle=subtitel,
            urval=self.uv_alla_partier,
            lookup_block=self.df_uppslag_block,
            spärr=spärr
        )
        c1 = chart_obj1.get_chart()
        chart_obj2 = ChartByBlockAddText(
            data=df_data,
            urval=self.uv_alla_partier,
            lookup_block=self.df_uppslag_block,
            spärr=spärr
        )
        c2 = chart_obj2.get_chart()
        exp = chart_obj1.assemple_charts((c1 + c2), 14)
        return exp
    
    def visa_linje_för_block(self, spärr: bool):
        titel = "Opinionsdata för block"
        subtitel = ["Undersökning per datum"]

        chart_obj1 = ChartByBlockDateTimeSeries(title=titel, subtitle=subtitel, data=self.df, urval=self.uv_alla_partier, lookup_block=self.df_uppslag_block, spärr=spärr)
        c1 = chart_obj1.get_chart()

        chart_obj2 = ChartByBlockDateTimeSeriesLine(title=titel, subtitle=subtitel, data=self.df_rullande_4, urval=self.uv_alla_partier, lookup_block=self.df_uppslag_block, spärr=spärr)
        c2 = chart_obj2.get_chart()

        exp = chart_obj1.assemple_charts((c2+c1), labelfont_size=14)
        return exp

    @staticmethod
    def ge_meddelande_om_dagar_kvar_till_valet():
        dagar = DataAccess.ge_dagar_kvar_till_valet()
        return f"Dagar till valet: {dagar}"
