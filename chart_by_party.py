from chart_base import ChartBase
from abc import abstractmethod
import altair as alt



class ChartByPartyBase(ChartBase):
    """ basklass för diagram för att visa opinionsläge för partier """

    def add_transform_fold(self):
        self.add_tranform_fold_wide_to_long_by_party()
    


class ChartByPartyMonthMeanTimeSeries(ChartByPartyBase):
    """ klass som visar opinionsläge för partier med medelvärden för kalendermånader"""
    def add_marker(self):
        self.c = self.c.mark_tick(size=30, thickness=3, cornerRadius=2)

    def add_encode(self):
        antal_m = alt.Tooltip("count(stöd):Q", title="antal mätningar")
        y_uttryck = "mean(stöd):Q"
        datum_uttryck = "month(Publiceringsdatum):O"
        self.c = self.c.encode(
            x=alt.X(datum_uttryck, title="Månad"),
            y=alt.Y(y_uttryck, title="Procent"),
            color=self.get_alt_color_by_parti_and_urval(),
            tooltip=["Parti:N", 
                alt.Tooltip(y_uttryck, title = "medel" ),
                alt.Tooltip("count(stöd):Q", title="antal mätningar")],
            size=alt.Size("count(stöd):Q", legend = None),
        )


class ChartByPartyDateTimeSeries(ChartByPartyBase):
    """ klass som visar opinionsläge för partier per datum """
    def add_marker(self):

        self.c = self.c.mark_circle(opacity=0.36, size=32)

    def add_encode(self):
        y_uttryck = "stöd:Q"
        datum_uttryck = "Publiceringsdatum:T"
        self.c = self.c.encode(
            x=alt.X(datum_uttryck, title="Månad"),
            y=alt.Y(y_uttryck, title="Procent"),
            color=self.get_alt_color_by_parti_and_urval(suppress_legend=False),
            tooltip=["Parti:N", y_uttryck, datum_uttryck],
        )

class ChartByPartyDateTimeSeriesLine(ChartByPartyDateTimeSeries):
    def add_marker(self):
        self.c = self.c.mark_line(size=1.65, opacity=1)


