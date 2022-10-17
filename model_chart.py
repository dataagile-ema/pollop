from re import sub
from data_access import DataAccess
from urval import UrvalsLista
from chart_by_block import ChartByBlockBar, ChartByBlockDateTimeSeries, ChartByBlockDateTimeSeries, ChartByBlockDateTimeSeriesLine
from chart_by_block import ChartByBlockAddText
from chart_by_party import ChartByPartyDateTimeSeries, ChartByPartyDateTimeSeriesLine
from chart_by_party import ChartByPartyMonthMeanTimeSeries
from charts_additions import Chart4PercentLineRule, ChartElectionDayRule
import pandas as pd
from datetime import datetime, timedelta
from urval import Urval
from grunddata import Grunddata
from grunddata import BLOCK_INDEX_REGERING
from grunddata import BLOCK_INDEX_OP



class ModelChart:
    def __init__(self, dagar_kar_text: str) -> None:
        self.dagar_kvar_text = dagar_kar_text

         # calc date 8 months ago
        start_datum = (datetime.now() - timedelta(days=240)).strftime("%Y-%m-%d")

        self.df = DataAccess.hämta_data(start_datum)
        self.df_rullande_n = DataAccess.skapa_rullande_medel(start_datum, DataAccess.hämta_data("2021-01-01"), Grunddata.antal_undersökningsdagar_n_rullande)
        self.df_sista_30_dagar = DataAccess.ge_data_for_sista_30_dagarna(self.df)
        self.df_uppslag_block = DataAccess.hämta_df_för_uppslag_block()
        self.__sätt_urval()

    def __sätt_urval(self):
        self.uv_små_partier = Urval.hämta_urval_enligt_30_dagars_medel(
            self.df, True, Grunddata.gräns_småparti
        )

        self.uv_alla_partier = Urval.hämta_urval_alla_partier()
        self.uv_opposition = Urval.hämta_urval_för_block(Grunddata.blocknamn[BLOCK_INDEX_OP])
        self.uv_regering_stöd = Urval.hämta_urval_för_block(Grunddata.blocknamn[BLOCK_INDEX_REGERING])

    def visa_linje_små_partier(self):
        titel = "Partier nära spärren"
        subtitel = ["Medel för kalendermånad"]

        chart_obj1 = ChartByPartyMonthMeanTimeSeries(self.df, title=titel, subtitle=subtitel, urval=self.uv_små_partier)
        c1 = chart_obj1.get_chart()

        chart_obj2 = Chart4PercentLineRule()
        c2 = chart_obj2.get_chart()

        exp = chart_obj1.assemple_charts((c1+c2), 14)
        return exp


    def visa_spridningsdiagram_små_partier(self):
        titel = "Partier nära spärren"
        subtitel = [f"Rullande medel för {Grunddata.antal_undersökningsdagar_n_rullande} publiceringsdagar"]

        chart_obj1 = Chart4PercentLineRule()
        c1 = chart_obj1.get_chart()

        chart_obj2 = ChartByPartyDateTimeSeriesLine(data=self.df_rullande_n, title=titel, subtitle=subtitel, urval=self.uv_små_partier)
        c2 = chart_obj2.get_chart()

        chart_obj3 = ChartByPartyDateTimeSeries(data=self.df, title=titel, subtitle=subtitel, urval=self.uv_små_partier)
        c3 = chart_obj3.get_chart()

        exp = chart_obj3.assemple_charts((c1+c2+c3), 14)
        return exp

    def visa_spridningsdiagram_partier_opposition(self):
        titel = Grunddata.blocknamn[BLOCK_INDEX_OP]
        subtitel = [f"Rullande medel för {Grunddata.antal_undersökningsdagar_n_rullande} publiceringsdagar"]

        chart_obj1 = ChartByPartyDateTimeSeriesLine(data=self.df_rullande_n, title=titel, subtitle=subtitel, urval=self.uv_opposition)
        c1 = chart_obj1.get_chart()

        chart_obj2 = ChartByPartyDateTimeSeries(data=self.df, title=titel, subtitle=subtitel, urval=self.uv_opposition)
        c2 = chart_obj2.get_chart()

        exp = chart_obj1.assemple_charts((c1+c2), 14)
        return exp

    def visa_spridningsdiagram_partier_regering_stöd(self):
        titel = Grunddata.blocknamn[BLOCK_INDEX_REGERING]
        subtitel = [f"Rullande medel för {Grunddata.antal_undersökningsdagar_n_rullande} publiceringsdagar"]        

        chart_obj1 = ChartByPartyDateTimeSeriesLine(data=self.df_rullande_n, title=titel, subtitle=subtitel, urval=self.uv_regering_stöd)
        c1 = chart_obj1.get_chart()

        chart_obj2 = ChartByPartyDateTimeSeries(data=self.df, title=titel, subtitle=subtitel, urval=self.uv_regering_stöd)
        c2 = chart_obj2.get_chart()

        exp = chart_obj1.assemple_charts((c1+c2), 14)
        return exp
        


    def visa_block_som_stacked_bar_30_dagars_medel(self):
        subtitel = ["Medel för de senaste 30 dagarna"]
        df_data = self.df_sista_30_dagar

        exp = self.__visa_block_som_stacked_bar(subtitel, df_data)
        return exp

    def visa_block_som_stacked_bar_senaste_n_undesökningsdagar(self, spärr: bool, n: int):
        subtitel = [f"Medel för de senaste {n} publiceringsdagarna"]
        df_data = self.df.groupby('Publiceringsdatum').mean()
        
        df_data = df_data.tail(n)
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
        subtitel = [f"Rullande medel för {Grunddata.antal_undersökningsdagar_n_rullande} publiceringsdagar"]        
        chart_obj1 = ChartByBlockDateTimeSeries(title=titel, subtitle=subtitel, data=self.df, urval=self.uv_alla_partier, lookup_block=self.df_uppslag_block, spärr=spärr)
        c1 = chart_obj1.get_chart()

        chart_obj2 = ChartByBlockDateTimeSeriesLine(title=titel, subtitle=subtitel, data=self.df_rullande_n, urval=self.uv_alla_partier, lookup_block=self.df_uppslag_block, spärr=spärr)
        c2 = chart_obj2.get_chart()

        if (DataAccess.ge_dagar_kvar_till_valet() < 20):
            chart_obj3 = ChartElectionDayRule()
            c3 = chart_obj3.get_chart()
            exp = chart_obj1.assemple_charts((c2+c3+c1), labelfont_size=14)
        else:
            exp = chart_obj1.assemple_charts((c2+c1), labelfont_size=14)

        return exp

    def hämta_df_senaste_undersökningar(self):
        df_show = self.df.tail(4)[::-1][["Publiceringsdatum", "V", "S", "MP", "C", "L", "M", "KD", "SD", "Institut"]]
        df_show["Institut"] = df_show["Institut"] + df_show["Publiceringsdatum"].dt.strftime(" %m-%d")
        df_show.set_index("Institut", inplace=True)
        df_show = df_show[["V", "S", "MP", "C", "L", "M", "KD", "SD"]]
        return df_show

    @staticmethod
    def ge_meddelande_om_dagar_kvar_till_valet():
        dagar = DataAccess.ge_dagar_kvar_till_valet()
        import datetime as dt
        # get current time in the swedish time zone
        now = dt.datetime.now(dt.timezone(dt.timedelta(hours=2)))
        # get current hour as text
        current_hour = now.strftime("%H")
        return f"Dagar till valet: {dagar} (uppdaterat {current_hour}:00)"
