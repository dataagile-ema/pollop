import altair as alt
from altair.vegalite.v4.api import Chart
import pandas as pd
import streamlit as st
# ny rubrik
# läsbarhet på telefon, se över typsnitt.
# lägg pren så att det märks när polls-fils ändras.
# lägg legend under så att den synns.
# lägg någon checkbox under?
# ha fast 3 månad minus, sista kvartalet.
# under 6% någon av de sista 4 mätningarna
"""
# Hur går det för de små partierna?
"""


partier = ['V', 'S', 'MP','C', 'L', 'M', 'KD', 'SD']
färger = ['darkred', 'red', 'darkgreen', 'green', 'deepskyblue', 'blue', 'darkblue', 'yellow']

close_to_cut_off = True # st.checkbox("Visa endast partier som ligger nära spärren", value=True)
visa_sista_måndaerna = True # st.checkbox("Visa bara sista måndaderna", value=True)
visa_snitt = st.checkbox("Visa snittvärden", value=True)

df = pd.read_csv("polls_edit.csv", delimiter=';')
df['Datum'] = pd.to_datetime(df.PublYearMonth)

if close_to_cut_off:
    valda = df.head(1)[partier]<6.15
    from itertools import compress
    partier = list(compress(partier, valda.to_numpy().tolist()[0]))
    färger = list(compress(färger, valda.to_numpy().tolist()[0]))

if visa_sista_måndaerna:
    df = df[df['Datum'] > '2021-04-01']

if visa_snitt:
    uttryck = 'mean(stöd):Q'
else:
    uttryck = 'stöd:Q'

st.altair_chart(
    alt.Chart(df).mark_line().transform_fold(
        fold=partier, 
        as_=['Parti', 'stöd']
    ).encode(
        x='Datum',
        y = alt.Y(uttryck, title="Procent"),
        color = alt.Color('Parti:N', 
            scale=alt.Scale(domain = partier, 
            range=färger), legend=alt.Legend(orient='top')),
        tooltip = ['Parti:N', uttryck]
    ).configure_legend(
        strokeColor='gray',
        fillColor='#EEEEEE',
        padding=10,
        cornerRadius=10,
        orient='top-right',
        title = None,
        labelFontSize = 14,
        symbolStrokeWidth = 8

    ).properties(
        width=420,
        height=340,

    ).configure_axis(
        labelFontSize=20,
        titleFontSize=20
    )   
)


# chart.encode(
#     #...
#     color=alt.Color('value', legend=alt.Legend(orient='right'))
#     #...
# )



