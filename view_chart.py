import pandas as pd
import altair as alt
from abc import ABC, abstractmethod
from types_def import Urval

# tranformationer som återanvänds
def add_tranform_fold_wide_to_long_by_party(c: alt.Chart, partier_urval):
    c = c.transform_fold(fold=partier_urval, as_=["Parti", "stöd"])
    return c

def add_transform_lookup_for_block(c: alt.Chart, lookup_block: pd.DataFrame):
    c = c.transform_lookup(
        lookup="Parti",
        from_=alt.LookupData(data=lookup_block, key="Parti", fields=["Block"]),
    )
    return c


class ChartBase(ABC):
    def __init__(
        self,
        data: pd.DataFrame,
        title: str = "",
        subtitle: list[str] = [""],
        urval: Urval = None,
        lookup_block: pd.DataFrame = pd.DataFrame(['']),
    ):
        plot_title = alt.TitleParams(title, subtitle=subtitle)
        self.c: alt.Chart = alt.Chart(data=data, title=plot_title)
        self.urval: Urval = urval
        self.lookup_block = lookup_block
        self.add_configuration()

    def get_chart(self):
        return self.c

    def add_configuration(self):
        self.add_transform_fold()
        self.add_transform_aggregate()
        self.add_transform_lookup()
        self.add_marker()
        self.add_encode()

    @abstractmethod
    def add_transform_fold(self):
        pass

    @abstractmethod
    def add_marker(self):
        pass

    @abstractmethod
    def add_encode(self):
        pass

    def add_transform_lookup(self):
        """ måste inte vara med i subbklasser"""
        pass

    def add_transform_aggregate(self):
        """ måste inte vara med i subbklasser"""
        pass


class ChartLine(ChartBase):
    """ skapar ett tidsseriediagram med linjer """

    def add_transform_fold(self):
        self.c = add_tranform_fold_wide_to_long_by_party(
            self.c, self.urval.partier_urval
        )

    def add_marker(self):
        self.c = self.c.mark_line()

    def add_encode(self):
        y_uttryck = "mean(stöd):Q"
        self.c = self.c.encode(
            x=alt.X("month(Publiceringsdatum)", title="Månad"),
            y=alt.Y(y_uttryck, title="Procent"),
            color=alt.Color(
                "Parti:N",
                scale=alt.Scale(
                    domain=self.urval.partier_urval,
                    range=self.urval.färger_partier_urval,
                ),
                legend=alt.Legend(orient="top"),
            ),
            tooltip=["Parti:N", y_uttryck],
        )


class ChartCircle(ChartBase):
    """ skapar ett tidsseriediagram med punkter """

    def add_transform_fold(self):
        self.c = add_tranform_fold_wide_to_long_by_party(
            self.c, self.urval.partier_urval
        )

    def add_marker(self):
        self.c = self.c.mark_circle()

    def add_encode(self):
        y_uttryck = "stöd:Q"
        datum_uttryck = "Publiceringsdatum"
        self.c = self.c.encode(
            x=alt.X("Publiceringsdatum", title="Månad"),
            y=alt.Y(y_uttryck, title="Procent"),
            color=alt.Color(
                "Parti:N",
                scale=alt.Scale(
                    domain=self.urval.partier_urval,
                    range=self.urval.färger_partier_urval,
                ),
                legend=alt.Legend(orient="top"),
            ),
            tooltip=["Parti:N", y_uttryck, datum_uttryck, "Institut"],
        )


class ChartBlockBar(ChartBase):
    def add_transform_fold(self):
        self.c = add_tranform_fold_wide_to_long_by_party(
            self.c, self.urval.partier_urval
        )

    def add_transform_aggregate(self):
        self.c = self.c.transform_aggregate(medel_stöd="mean(stöd)", groupby=["Parti"])

    def add_transform_lookup(self):
        self.c = add_transform_lookup_for_block(
            c=self.c, lookup_block=self.lookup_block
        )

    def add_marker(self):
        self.c = self.c.mark_bar()

    def add_encode(self):
        self.c = self.c.encode(
            x=alt.X(
                "Block:O",
                scale=alt.Scale(domain=["Regering + stöd", "Högeropposition"]),
            ),
            y=alt.Y("medel_stöd:Q", title="Procent"),
            color=alt.Color(
                "Parti:N",
                scale=alt.Scale(
                    domain=self.urval.partier_urval,
                    range=self.urval.färger_partier_urval,
                ),
                legend=alt.Legend(orient="right"),
            ),
            tooltip=["Parti:N", "medel_stöd:Q"],
        )


class ChartBlockText(ChartBase):
    def add_transform_fold(self):
        self.c = add_tranform_fold_wide_to_long_by_party(
            self.c, self.urval.partier_urval
        )

    def add_transform_aggregate(self):
        self.c = self.c.transform_aggregate(medel_stöd="mean(stöd)", groupby=["Parti"])

    def add_transform_lookup(self):
        self.c = add_transform_lookup_for_block(
            c=self.c, lookup_block=self.lookup_block
        )

    def add_marker(self):
        self.c = self.c.mark_text(dx=0, baseline="middle", dy=-8, color="darkslategrey")

    def add_encode(self):
        self.c = self.c.encode(
            x=alt.X("Block:O", stack="zero"),
            y=alt.Y("sum(medel_stöd):Q"),
            text=alt.Text("sum(medel_stöd):Q", format=".1f"),
        )


class ChartSpärr(ChartBase):
    def add_transform_fold(self):
        pass

    def add_marker(self):
        self.c = self.c.mark_rule(strokeDash=[10, 10])

    def add_encode(self):
        self.c = self.c.encode(y="y")


class CreateCompleteCharts:
    """ Skapar ett komplett diagram utifrån ett eller flera chartobjekt """

    def __init__(self, chart_exp, label_font_size: int = 14) -> None:
        self.chart_exp = chart_exp
        self.label_font_size = label_font_size
        self.create_complete_charts()

    def get_complete_charts(self):
        return self.chart_exp

    def create_complete_charts(self):
        self.add_configure_legend()
        self.add_properties()
        self.add_configure_title()

    def add_configure_legend(self):
        self.chart_exp = self.chart_exp.configure_legend(
            strokeColor="gray",
            fillColor="#EEEEEE",
            padding=10,
            cornerRadius=10,
            orient="top-right",
            title=None,
            labelFontSize=14,
            symbolStrokeWidth=8,
        )

    def add_properties(self):
        self.chart_exp = self.chart_exp.properties(
            width=420, height=340
        ).configure_axis(
            labelFontSize=self.label_font_size, labelAngle=0, titleFontSize=14
        )

    def add_configure_title(self):
        self.chart_exp = self.chart_exp.configure_title(fontSize=14)
