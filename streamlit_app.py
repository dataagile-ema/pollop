import streamlit as st
from PIL import Image
from itertools import compress
import data_access as da
from model_chart import ModelChart
from grunddata import Grunddata


def visa_tabell_senaste_under_sökningarna(modell: ModelChart):
    st.write("Senaste undersökningarna")
    df_show = modell.hämta_df_senaste_undersökningar()
    
    # make dictionary with partier from Grunddata as first column and "{}" as the second column
    partier_dict = {parti: "{:.1f}" for parti in Grunddata.partier}
    st.table(df_show.style.format(partier_dict,))


# navigering
def __sätt_val_0():
    st.session_state.first = 0

def __sätt_val_1():
    st.session_state.first = 1

def __sätt_val_2():
    st.session_state.first = 2


def __vilket_val():
    if "first" not in st.session_state:
        return 0
    elif st.session_state.first == 0:
        return 0
    elif st.session_state.first == 1:
        return 1
    elif st.session_state.first == 2:
        return 2


# sida
im = Image.open("favicon.ico")
st.set_page_config(page_title="Pollop", page_icon=im)
"""
# Hur går det för..
"""
dagar_kvar_till_val_text = ModelChart.ge_meddelande_om_dagar_kvar_till_valet()
@st.cache
def get_model():
    return ModelChart(dagar_kvar_till_val_text)
modell = get_model()

# grunddata navigering
användar_val = ["Blocken", "Partierna", "Partier nära spärren"]

# navigering
left, mid, right = st.columns(3)
with left:
    st.button(
        användar_val[0],
        on_click=__sätt_val_0,
        help="Nuvarande regeringsunderlag jämfört med högeroppositionen",
    )

with mid:
    st.button(
    användar_val[1], on_click=__sätt_val_2, help="Alla partier")

with right:
    st.button(label=användar_val[2], on_click=__sätt_val_1, help="Ligger nära riksdagsspärren i undersökningarna")



if __vilket_val() == 0:
    spärr = st.checkbox("Ta bort partier under spärr", False)
    chart_u1 = modell.visa_linje_för_block(spärr)
    chart_u2 = modell.visa_block_som_stacked_bar_senaste_n_undesökningsdagar(spärr, Grunddata.antal_undersökningsdagar_n_stacked)
elif __vilket_val() == 1:
    chart_u1 = modell.visa_spridningsdiagram_små_partier()
    chart_u2 = modell.visa_linje_små_partier()
else:
    chart_u1 = modell.visa_spridningsdiagram_partier_regering_stöd()
    chart_u2 = modell.visa_spridningsdiagram_partier_högeropposition()


st.altair_chart(chart_u1, use_container_width=True)

if (__vilket_val() == 1):
    st.write(modell.dagar_kvar_text)
    visa_tabell_senaste_under_sökningarna(modell)
    st.altair_chart(chart_u2, use_container_width=True)
else:
    st.altair_chart(chart_u2, use_container_width=True)
    st.write(modell.dagar_kvar_text)
    visa_tabell_senaste_under_sökningarna(modell)

st.write(
    """
        All sammanställd opinionsdata kommer från Hampus Joakim Borgos Github:
        https://github.com/hampusborgos/SwedishPolls eller från Måns Magnusseons Github: https://github.com/MansMeg/SwedishPolls.
        För att hitta mer statistik för opinionsundersökningar rekommenderas https://val.digital/
    """    )

with st.expander("Referenser"):
    st.markdown("Se https://github.com/dataagile-ema för kontaktuppgifter")
st.markdown('![Tick](https://shields-io-visitor-counter.herokuapp.com/badge?page=https://share.streamlit.io/dataagile-ema/pollop&label=Tick&labelColor=000000&logo=GitHub&logoColor=FFFFFF&color=1D70B8&style=for-the-badge)')
