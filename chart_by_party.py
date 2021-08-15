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
        self.c = self.c.mark_line()

    def add_encode(self):
        y_uttryck = "mean(stöd):Q"
        datum_uttryck = "month(Publiceringsdatum):T"
        self.c = self.c.encode(
            x=alt.X(datum_uttryck, title="Månad"),
            y=alt.Y(y_uttryck, title="Procent"),
            color=self.get_alt_color_by_parti_and_urval(),
            tooltip=["Parti:N", y_uttryck],
        )


class ChartByPartyDateTimeSeries(ChartByPartyBase):
    """ klass som visar opinionsläge för partier per datum """
    def add_marker(self):
        self.c = self.c.mark_point(opacity=0.4, size=40)

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
        self.c = self.c.mark_line(size=1.7, opacity=1)


