from chart_base import ChartBase
from urval import UrvalsLista
import pandas as pd
import altair as alt
from altair import datum
from grunddata import Grunddata



class ChartByBlockBase(ChartBase):
    def __init__(self, data: pd.DataFrame, title: str, subtitle, urval: UrvalsLista, lookup_block: pd.DataFrame, spärr: bool=True):
        self.spärr = spärr
        self.lookup_block = lookup_block
        super().__init__(data=data, title=title, subtitle=subtitle, urval=urval)

    def add_transform_fold(self):
        self.add_tranform_fold_wide_to_long_by_party()
    
    def add_transform_lookup(self):
        self.c = self.c.transform_lookup(lookup='Parti', from_=alt.LookupData(self.lookup_block, key='Parti', fields=['Block']))

    def add_filter(self):
        if self.spärr:
            self.c = self.c.transform_filter(
                        (datum.medel_stöd > Grunddata.riksdagsspärr)
                    )
    


class ChartByBlockBar(ChartByBlockBase):
    def add_marker(self):
        self.c = self.c.mark_bar()

    def add_transform_aggregate(self):
        self.c = self.c.transform_aggregate(medel_stöd="mean(stöd)", groupby=["Parti"])

    def add_encode(self):
        self.c = self.c.encode(
            x=alt.X(
                "Block:O",
                scale=alt.Scale(domain=["Regering + stöd", "Högeropposition"]),
            ),
            y=alt.Y("medel_stöd:Q", title="Procent"),
            color= self.get_alt_color_by_parti_and_urval(orient='right'),
            tooltip=["Parti:N", "medel_stöd:Q"],
        )
    

class ChartByBlockAddText(ChartByBlockBase):
    def __init__(self, data: pd.DataFrame, urval: UrvalsLista, lookup_block: pd.DataFrame, spärr: bool):

        super().__init__(data, title = '', subtitle= '', urval=urval, lookup_block=lookup_block, spärr=spärr)

    def add_transform_aggregate(self):
        self.c = self.c.transform_aggregate(medel_stöd="mean(stöd)", groupby=["Parti"])

    def add_marker(self):
        self.c = self.c.mark_text(dx=0, baseline="middle", dy=-8, color="darkslategrey")

    def add_encode(self):
        self.c = self.c.encode(
            x=alt.X("Block:O", stack="zero"),
            y=alt.Y("sum(medel_stöd):Q"),
            text=alt.Text("sum(medel_stöd):Q", format=".1f"),
        )


class ChartByBlockDateTimeSeries(ChartByBlockBase):
    def add_marker(self):
        self.c = self.c.mark_circle(opacity=0.45, size=32)
    
    def add_transform_aggregate(self):
        self.c = self.c.transform_aggregate(medel_stöd="mean(stöd)", groupby=["Publiceringsdatum", "Parti"])


    def add_encode(self):
        y_uttryck = "sum(medel_stöd):Q"
        datum_uttryck = "Publiceringsdatum:T"
        self.c = self.c.encode(
            x=alt.X(datum_uttryck, title="Månad"),
            y=alt.Y(y_uttryck, title="Procent", scale=alt.Scale(domain=(39, 54))),
            color = alt.Color(
                    "Block:O",
                     scale=alt.Scale(
                        domain=["Regering + stöd", "Högeropposition"],
                        range=["#FF8080", "#80C0FF"],
                    ),
                    legend=alt.Legend(orient='top'),
                ),
            tooltip=[y_uttryck, "Block:O", datum_uttryck]
        )
    
class ChartByBlockDateTimeSeriesLine(ChartByBlockDateTimeSeries):

    def add_marker(self):
        self.c = self.c.mark_line(size=1.8, opacity=1)

