import altair as alt
from altair.vegalite.v4.api import Chart
import pandas as pd
import streamlit as st

"""
# Test av Streamlit!
Interaktiv graf för opinionsundersökningar
"""

df = pd.read_csv("polls_edit.csv", delimiter=';')
df['Datum'] = pd.to_datetime(df.PublYearMonth)



st.altair_chart(
    alt.Chart(df).mark_line().transform_fold(
        fold=['V', 'S', 'MP','C', 'L', 'M', 'KD', 'SD'], 
        as_=['parti', 'stöd']
    ).encode(
        x='Datum',
        y = alt.Y('mean(stöd):Q', title="Procent"),

        color = alt.Color('parti:N', 
            scale=alt.Scale(domain = ['V', 'S', 'MP','C', 'L', 'M', 'KD', 'SD'], 
            range=['darkred', 'red', 'green', 'darkgreen', 'deepskyblue', 'blue', 'darkblue', 'yellow'])),
        tooltip = ['parti:N', 'mean(stöd):Q']
    ).interactive()
)
