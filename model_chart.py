from data_access import DataAccess
from data_access import Urval
import view_chart as wc
import pandas as pd


class ModelChart:
    def __init__(self) -> None:
        self.df = DataAccess.hämta_data("2021-02-01")
        self.uv_små_partier = DataAccess.hämta_urval(
            self.df, True, DataAccess.gräns_småparti
        )
        self.uv_större_partier = DataAccess.hämta_urval(
            self.df, False, DataAccess.gräns_småparti
        )
        self.uv_partier_över_spärr = DataAccess.hämta_urval(
            self.df, False, DataAccess.riksdagsspärr
        )
        self.df_sista_30_dagar = DataAccess.ge_data_for_sista_30_dagarna(self.df)
        self.df_uppslag_block = DataAccess.hämta_df_för_uppslag_block()

    def visa_linje_små_partier(self):
        titel = "Opinionsdata för små partier"
        subtitel = ["Visar medel för kalendermånad"]
        chart_b1 = wc.ChartLine(
            data=self.df, title=titel, subtitle=subtitel, urval=self.uv_små_partier
        )
        c1 = chart_b1.get_chart()
        chart_b2 = wc.ChartSpärr(pd.DataFrame(data={"y": [4]}))
        c2 = chart_b2.get_chart()
        comp_charts = wc.CreateCompleteCharts((c1 + c2), 14)
        exp = comp_charts.get_complete_charts()
        return exp

    def visa_linje_större_partier(self):
        titel = "Opinionsdata för större partier"
        subtitel = ["Visar medel för kalendermånad"]
        chart_b1 = wc.ChartLine(
            data=self.df, title=titel, subtitle=subtitel, urval=self.uv_större_partier
        )
        c1 = chart_b1.get_chart()
        comp_charts = wc.CreateCompleteCharts((c1), 14)
        exp = comp_charts.get_complete_charts()
        return exp

    def visa_spridningsdiagram_små_partier(self):
        titel = "Opinionsdata för små partier"
        subtitel = ["Visar alla opinionsundersökningar"]
        chart_b1 = wc.ChartCircle(
            data=self.df, title=titel, subtitle=subtitel, urval=self.uv_små_partier
        )
        c1 = chart_b1.get_chart()
        chart_b2 = wc.ChartSpärr(pd.DataFrame(data={"y": [4]}))
        c2 = chart_b2.get_chart()
        comp_charts = wc.CreateCompleteCharts((c1 + c2), 14)
        exp = comp_charts.get_complete_charts()
        return exp

    def visa_spridningsdiagram_större_partier(self):
        titel = "Opinionsdata för större partier"
        subtitel = ["Visar alla opinionsundersökningar"]
        chart_b1 = wc.ChartCircle(
            data=self.df, title=titel, subtitle=subtitel, urval=self.uv_större_partier
        )
        c1 = chart_b1.get_chart()
        comp_charts = wc.CreateCompleteCharts((c1), 14)
        exp = comp_charts.get_complete_charts()
        return exp

    def visa_block_som_stacked_bar_30_dagars_medel(self):
        subtitel = ["Visar medel för de senaste 30 dagarna"]
        df_data = self.df_sista_30_dagar

        exp = self.__visa_block_som_stacked_bar(subtitel, df_data)
        return exp

    def visa_block_som_stacked_bar_30_senaste_undesökning(self):
        subtitel = ["Visa senaste opinionsundersökning"]
        df_data = self.df.head(1)
        exp = self.__visa_block_som_stacked_bar(subtitel, df_data)
        return exp

    def __visa_block_som_stacked_bar(self, subtitel, df_data):
        titel = "Opinionsdata för block"
        chart_b1 = wc.ChartBlockBar(
            data=df_data,
            title=titel,
            subtitle=subtitel,
            urval=self.uv_partier_över_spärr,
            lookup_block=self.df_uppslag_block,
        )
        c1 = chart_b1.get_chart()
        chart_b2 = wc.ChartBlockText(
            data=df_data,
            title=titel,
            urval=self.uv_partier_över_spärr,
            lookup_block=self.df_uppslag_block,
        )
        c2 = chart_b2.get_chart()
        comp_charts = wc.CreateCompleteCharts((c1 + c2), 14)
        exp = comp_charts.get_complete_charts()
        return exp

    @staticmethod
    def ge_meddelande_om_dagar_kvar_till_valet():
        dagar = DataAccess.ge_dagar_kvar_till_valet()
        return f"Dagar till valet: {dagar}"
