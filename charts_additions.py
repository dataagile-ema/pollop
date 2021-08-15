from altair.vegalite.v4.schema.core import Legend
from chart_base import ChartBase
import pandas as pd
from types_def import Urval
from types_def import riksdagsspärr
import altair as alt

class Chart4PercentLineRule(ChartBase):
    def __init__(self):
        super().__init__(pd.DataFrame(data={"y": [riksdagsspärr]}), title='', subtitle='', urval=None)
        
    def add_transform_fold(self):
        pass

    def add_marker(self):
        self.c = self.c.mark_rule(strokeDash=[10, 10], color="black")

    def add_encode(self):
        self.c = self.c.encode(
            y="y"
        )
            
