from altair.vegalite.v4.schema.core import Legend
from chart_base import ChartBase
import pandas as pd
from urval import UrvalsLista
from grunddata import Grunddata
import altair as alt

class Chart4PercentLineRule(ChartBase):
    def __init__(self):
        super().__init__(pd.DataFrame(data={"y": [Grunddata.riksdagsspärr]}), title='', subtitle='', urval=None)
        
    def add_transform_fold(self):
        pass

    def add_marker(self):
        self.c = self.c.mark_rule(color="black", strokeWidth=1)

    def add_encode(self):
        self.c = self.c.encode(
            y="y"
        )
            

class ChartElectionDayRule(ChartBase):
    def __init__(self):
        # create a date object for the election day
        election_day = pd.to_datetime(Grunddata.valdag)
        super().__init__(pd.DataFrame(data={"x": [election_day]}), title='', subtitle='', urval=None)
        
    def add_transform_fold(self):
        pass

    def add_marker(self):
        self.c = self.c.mark_rule(color="grey", strokeWidth=1.8, strokeDash=[2, 2])

    def add_encode(self):
        self.c = self.c.encode(
            x="x"
        )