from numpy.core.fromnumeric import size


class AssembleCharts:
    """ Skapar ett komplett diagram utifrån ett eller flera chartobjekt """

    def __init__(self, chart_exp, label_font_size: int = 14) -> None:
        self.chart_exp = chart_exp
        self.label_font_size = label_font_size
        self.create_complete_charts()

    def get_assembled_charts(self):
        return self.chart_exp

    def create_complete_charts(self):
        self.add_configure_legend()
        self.add_properties()
        self.add_configure_title()

    def add_configure_legend(self):
        self.chart_exp = self.chart_exp.configure_legend(
            orient="top-right",
            title=None,
            fillColor="#fbfbfc",
            padding=0,
            labelFontSize=14,
            symbolStrokeWidth=10,
            symbolType = "circle"
        )
        

    def add_properties(self):
        self.chart_exp = self.chart_exp.properties(
            width=250, height=380,
        ).configure_axis(
            labelFontSize=self.label_font_size, labelAngle=0, titleFontSize=14
        )

    def add_configure_title(self):
        self.chart_exp = self.chart_exp.configure_title(fontSize=14)