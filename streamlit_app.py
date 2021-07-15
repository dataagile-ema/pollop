import altair as alt
from altair.vegalite.v4.api import Chart
import pandas as pd
import streamlit as st

"""
# Test av Streamlit!
Interaktiv graf för opinionsundersökningar
"""

partier = ['V', 'S', 'MP','C', 'L', 'M', 'KD', 'SD']
färger = ['darkred', 'red', 'darkgreen', 'green', 'deepskyblue', 'blue', 'darkblue', 'yellow']

close_to_cut_off = st.checkbox("Visa endast partier som ligger nära spärren", value=True)
visa_sista_måndaerna = st.checkbox("Visa bara sista måndaderna", value=True)
Visa_snitt = st.checkbox("visa snittvärden", value=True)

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
        as_=['parti', 'stöd']
    ).encode(
        x='Datum',
        y = alt.Y(uttryck, title="Procent"),

        color = alt.Color('parti:N', 
            scale=alt.Scale(domain = partier, 
            range=färger)),
        tooltip = ['parti:N', uttryck]
    ).interactive()
)
