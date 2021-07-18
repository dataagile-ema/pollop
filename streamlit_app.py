import altair as alt
from altair.vegalite.v4.api import Chart, value
from altair.vegalite.v4.schema.core import Padding
import pandas as pd
import streamlit as st
from PIL import Image
from itertools import compress


class OpinionChart:
    def __init__(self):
        self.titel = ""
        self.df = OpinionChart.läs_och_preparera_tidsserie_data()
        self.partier_urval = None
        self.färger_urval = None
        self.datum_utttryck = None
        self.y_uttryck = None
        self.tool_uttryck = None
        self.små_partier_bool = None
        self.chart = None


    @staticmethod
    def läs_och_preparera_tidsserie_data():
        df = pd.read_csv("polls_edit.csv", delimiter=';')
        df['Publiceringsdatum'] = pd.to_datetime(df.PublDate)
        df.rename(columns={'Company': 'Institut'}, inplace=True)
        df = df[df['Publiceringsdatum'] > '2021-02-01']
        return df


    @staticmethod
    def skapa_block_chart():
        block = ['Regering + stöd', 'Regering + stöd', 'Regering + stöd', 'Regering + stöd', 'Högeropposition', 'Högeropposition', 'Högeropposition', 'Högeropposition']
        färger = ['darkred', 'red', 'darkgreen', 'green', 'deepskyblue', 'blue', 'darkblue', 'yellow']
        partier = ['V', 'S', 'MP','C', 'L', 'M', 'KD', 'SD']
        df = pd.read_csv("polls_edit.csv", delimiter=';')

        parti_urval_bool = df.head(1)[partier]>4.0
        
        partier_urval = list(compress(partier, parti_urval_bool.to_numpy().tolist()[0]))
        färger_urval = list(compress(färger, parti_urval_bool.to_numpy().tolist()[0]))
        block_urval = list(compress(block, parti_urval_bool.to_numpy().tolist()[0]))

        df = df.head(1)
        df = df[partier_urval]
        df.index = ['stöd']
        df = df.T
        df.reset_index(inplace=True)
        df.rename(columns={ df.columns[0]: "parti" }, inplace = True)
        df['block'] = block_urval
        chart = alt.Chart(df).mark_bar().encode(
            x=alt.X('block:O', scale=alt.Scale(domain=['Regering + stöd', 'Högeropposition'])),
            y = alt.Y('sum(stöd)', title = "Procent"),
            color = alt.Color('parti:N',
                scale=alt.Scale(domain = partier_urval, range=färger_urval), legend=alt.Legend(orient='right')),
        ).configure_axisX(
            labelFontSize=15,
            labelAngle = 0,
            titleFontSize=20
        )

        return chart


    @staticmethod
    def skapa_tids_serie_chart(df_tidsserie, små_partier_bool, genomsnitt_bool):
        gräns_småparti = 6.0

        partier = ['V', 'S', 'MP','C', 'L', 'M', 'KD', 'SD']
        färger = ['darkred', 'red', 'darkgreen', 'green', 'deepskyblue', 'blue', 'darkblue', 'yellow']

        if små_partier_bool == False:
            titel = "Opinionssiffror för de större partierna"
            parti_urval_bool = df_tidsserie.head(1)[partier]>gräns_småparti
        else:
            titel = "Opinionssiffror för de små partierna"
            parti_urval_bool = df_tidsserie.head(1)[partier]<gräns_småparti
        
        partier_urval = list(compress(partier, parti_urval_bool.to_numpy().tolist()[0]))
        färger_urval = list(compress(färger, parti_urval_bool.to_numpy().tolist()[0]))
        if genomsnitt_bool:
            y_uttryck = 'mean(stöd):Q'
            datum_utttryck = 'month(Publiceringsdatum)'
            chart = alt.Chart(df_tidsserie, title=titel).mark_line().transform_fold(
                        fold=partier_urval, as_=['Parti', 'stöd'])
            tool_uttryck = ['Parti:N', y_uttryck]
        else:
            y_uttryck = 'stöd:Q'
            datum_utttryck = 'Publiceringsdatum'
            chart = alt.Chart(df_tidsserie, title=titel).mark_circle().transform_fold(
                        fold=partier_urval, as_=['Parti', 'stöd'])
            tool_uttryck = ['Parti:N', y_uttryck, 'Institut']

        chart = OpinionChart.lägg_till_encoding_för_chart(chart, datum_utttryck, y_uttryck, partier_urval, färger_urval, tool_uttryck)
        
        return OpinionChart.villkorligt_lägg_till_linje_för_spärr(små_partier_bool, chart)
    
    @staticmethod
    def lägg_till_encoding_för_chart(chart, datum_utttryck, y_uttryck, partier_urval, färger_urval, tool_uttryck):
        if chart is None:
            Exception("fel!")
        chart = chart.encode(
        x = datum_utttryck,
        y = alt.Y(y_uttryck, title = "Procent"),
        color = alt.Color('Parti:N',
            scale=alt.Scale(domain = partier_urval, range=färger_urval), legend=alt.Legend(orient='top')),
        tooltip = tool_uttryck)
        return chart

    @staticmethod
    def villkorligt_lägg_till_linje_för_spärr(små_partier_bool, chart):
        if små_partier_bool:
            riksdagsgräns_linje_chart = alt.Chart(pd.DataFrame({'y': [4]})).mark_rule(strokeDash=[10, 10]).encode(y='y')
            return (riksdagsgräns_linje_chart + chart)
        else:
            return chart


# navigering
def __sätt_val_0():
    st.session_state.first = 0

def __sätt_val_1():
    st.session_state.first = 1

def __sätt_val_2():
    st.session_state.first = 2

def __vilket_val():
    if 'first' not in st.session_state:
        return 0
    elif st.session_state.first == 0:
        return 0
    elif st.session_state.first == 1:
        return 1
    elif st.session_state.first == 2:
        return 2


# sida
im = Image.open("favicon.ico")
st.set_page_config(
    page_title="Pollop",
    page_icon=im
)
"""
# Hur går det för..
"""

# grunddata navigering
användar_val = ['de små partierna', 'de större partierna', 'de två blocken']


# navigering
left, mid, right = st.beta_columns(3)
with left:
    st.button(användar_val[0], on_click=__sätt_val_0, help="Ligger nära riksdagsspärren i undersökningarna")
with mid:
    st.button(användar_val[1], on_click=__sätt_val_1, help="Har minst 6% i undersökningarna")
with right:
    st.button(användar_val[2], on_click=__sätt_val_2, help="Nuvarande regeringsunderlag jämfört med högeroppositionen")

visa_månadsgenomsnitt = st.checkbox("Visa snittvärden för tidsserier", value=True, help="Visa medelvärden för undersökningar publicerade under en kalendermånad")

df = OpinionChart.läs_och_preparera_tidsserie_data()

if ((__vilket_val() == 0) or (__vilket_val() == 1)):
    chart_u = OpinionChart.skapa_tids_serie_chart(df, (__vilket_val() == 0), visa_månadsgenomsnitt)
else:
    chart_u = OpinionChart.skapa_block_chart()
    st.write("Partierna under riksdagsspärren räknas inte med. I nuläget är det ett parti i vardera block som ligger under spärren i opinionsundersökningarna.")
    


st.altair_chart(
    chart_u
    .configure_legend(
        strokeColor='gray',
        fillColor='#EEEEEE',
        padding=10,
        cornerRadius=10,
        orient='top-right',
        title = None,
        labelFontSize = 14,
        symbolStrokeWidth = 8)
    .properties(
            width=420,
            height=340).configure_axis(
            labelFontSize=20,
            titleFontSize=20
    ) 
)

with st.beta_expander("Data referenser"):
     st.write("""
         Avmarkera snittvärden och välj enskilda punkter för att se vilket opinionsinstitut som utfört undersökningen.
         All statistik kan hittas på https://val.digital/"
         Appen använder val.digitals publika repo där opinionssiffror finns samlade: https://github.com/hampusborgos/SwedishPolls/tree/master/Data
     """)



