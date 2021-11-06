import pandas as pd
import altair as alt
from abc import ABC, abstractmethod
from urval import UrvalsLista
from assemple_charts import AssembleCharts

class ChartBase(ABC):
    def __init__(
        self,
        data: pd.DataFrame,
        title: str = "",
        subtitle = [""],
        urval: UrvalsLista = None,
    ):
        plot_title = alt.TitleParams(title, subtitle=subtitle)
        self.c: alt.Chart = alt.Chart(data=data, title=plot_title)
        self.urval: UrvalsLista = urval
        self.add_configuration()

    def get_chart(self):
        return self.c

    def add_configuration(self):
        self.add_transform_fold()
        self.add_transform_aggregate()
        self.add_transform_lookup()
        self.add_marker()
        self.add_encode()
        self.add_filter()
    

    @abstractmethod
    def add_transform_fold(self):
        pass

    @abstractmethod
    def add_marker(self):
        pass

    @abstractmethod
    def add_encode(self):
        pass


    def add_filter(self):
        """ måste inte vara med i subbklasser"""
        pass

    def add_transform_lookup(self):
        """ måste inte vara med i subbklasser"""
        pass

    def add_transform_aggregate(self):
        """ måste inte vara med i subbklasser"""
        pass

    def add_tranform_fold_wide_to_long_by_party(self):
        self.c = self.c.transform_fold(fold = self.urval.partier_urval, as_=["Parti", "stöd"])

    def get_alt_color_by_parti_and_urval(self, orient="top", suppress_legend=False):
        if suppress_legend:
            legend_var = None
        else:
            legend_var = alt.Legend(orient=orient)

        color = alt.Color(
                    "Parti:N",
                    scale=alt.Scale(
                        domain=self.urval.partier_urval,
                        range=self.urval.färger_partier_urval,
                    ),
                    legend=legend_var,
                )
        return color

    @staticmethod
    def assemple_charts(chart_exp, labelfont_size: int = 14):
        ac = AssembleCharts(chart_exp=chart_exp, label_font_size=labelfont_size)
        chart_exp = ac.get_assembled_charts()
        return chart_exp

    





