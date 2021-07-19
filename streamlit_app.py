import altair as alt
from altair.vegalite.v4.api import Chart, value
from altair.vegalite.v4.schema.channels import Tooltip
from altair.vegalite.v4.schema.core import Padding
import pandas as pd
import streamlit as st
from PIL import Image
from itertools import compress

class GrundData:
    block = ['Regering + stöd', 'Regering + stöd', 'Regering + stöd', 'Regering + stöd', 'Högeropposition', 'Högeropposition', 'Högeropposition', 'Högeropposition']
    färger = ['darkred', 'red', 'darkgreen', 'green', 'deepskyblue', 'blue', 'darkblue', 'yellow']
    partier = ['V', 'S', 'MP','C', 'L', 'M', 'KD', 'SD']
    gräns_småparti = 6.0
    riksdagsspärr = 4.0

class OpinionChart:


    @staticmethod
    def läs_och_preparera_tidsserie_data(tidsserie: bool = True):
        df = pd.read_csv("polls_edit.csv", delimiter=';')
        if tidsserie == False:
            return df
        df['Publiceringsdatum'] = pd.to_datetime(df.PublDate)
        df.rename(columns={'Company': 'Institut'}, inplace=True)
        df = df[df['Publiceringsdatum'] > '2021-02-01']
        return df


    @staticmethod
    def skapa_block_chart():
        df = OpinionChart.läs_och_preparera_tidsserie_data(False)
        parti_urval_bool = df.head(1)[GrundData.partier]>GrundData.riksdagsspärr
        
        partier_urval = list(compress(GrundData.partier, parti_urval_bool.to_numpy().tolist()[0]))
        färger_urval = list(compress(GrundData.färger, parti_urval_bool.to_numpy().tolist()[0]))
        block_urval = list(compress(GrundData.block, parti_urval_bool.to_numpy().tolist()[0]))

        df = df.head(1)
        df = df[partier_urval]
        df.index = ['stöd']
        df = df.T
        df.reset_index(inplace=True)
        df.rename(columns={ df.columns[0]: "Parti" }, inplace = True)
        df['Block'] = block_urval
        chart = alt.Chart(df).mark_bar().encode(
            x=alt.X('Block:O', scale=alt.Scale(domain=['Regering + stöd', 'Högeropposition'])),
            y = alt.Y('sum(stöd)', title = "Procent"),
            color = alt.Color('Parti:N',
                scale=alt.Scale(domain = partier_urval, range=färger_urval), legend=alt.Legend(orient='right')),
            tooltip = ['Parti:N','stöd']
        )
     
        text = alt.Chart(df).mark_text(dx=0,baseline='middle', dy=-8, color='darkslategrey').encode(
                x=alt.X('Block:O', stack='zero'),
                y=alt.Y('sum(stöd)'),
                text=alt.Text('sum(stöd)', format='.1f')
            )

        return OpinionChart.lägg_till_konfiguration_för_legend_properties_och_axlar(chart + text, 15)


    @staticmethod
    def skapa_tidsserie_chart(df_tidsserie, små_partier_bool, genomsnitt_bool):
        
        if små_partier_bool == False:
            titel = "Opinionssiffror för de större partierna"
            parti_urval_bool = df_tidsserie.head(1)[GrundData.partier]>GrundData.gräns_småparti
        else:
            titel = "Opinionssiffror för de små partierna"
            parti_urval_bool = df_tidsserie.head(1)[GrundData.partier]<GrundData.gräns_småparti
        
        partier_urval = list(compress(GrundData.partier, parti_urval_bool.to_numpy().tolist()[0]))
        färger_urval = list(compress(GrundData.färger, parti_urval_bool.to_numpy().tolist()[0]))
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
        chart_och_linje = OpinionChart.villkorligt_lägg_till_linje_för_spärr(små_partier_bool, chart)

        return OpinionChart.lägg_till_konfiguration_för_legend_properties_och_axlar(chart_och_linje)

    @staticmethod
    def lägg_till_konfiguration_för_legend_properties_och_axlar(chart_uttryck, setlabelFontSize:int = 20):
        chart_uttryck = chart_uttryck.configure_legend(
                    strokeColor='gray',
                    fillColor='#EEEEEE',
                    padding=10,
                    cornerRadius=10,
                    orient='top-right',
                    title = None,
                    labelFontSize = 14,
                    symbolStrokeWidth = 8).properties(
                            width=420,
                            height=340).configure_axis(
                            labelFontSize=setlabelFontSize,
                            labelAngle = 0,
                            titleFontSize=20
                    )
        return chart_uttryck

    
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
    chart_u = OpinionChart.skapa_tidsserie_chart(df, (__vilket_val() == 0), visa_månadsgenomsnitt)
else:
    chart_u = OpinionChart.skapa_block_chart()
    st.write("Partierna under riksdagsspärren räknas inte med.")
    

st.altair_chart(
    chart_u
)

with st.beta_expander("Data referenser"):
     st.write("""
         Avmarkera snittvärden och välj enskilda punkter för att se vilket opinionsinstitut som utfört undersökningen.
         All statistik kan hittas på https://val.digital/"
         Appen använder val.digitals publika repo där opinionssiffror finns samlade: https://github.com/hampusborgos/SwedishPolls/tree/master/Data
     """)



