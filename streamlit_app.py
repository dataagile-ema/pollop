import streamlit as st
from PIL import Image
from itertools import compress
import model_chart

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


modell = model_chart.ModelChart()

# sida
im = Image.open("favicon.ico")
st.set_page_config(page_title="Pollop", page_icon=im)
"""
# Hur går det för..
"""


# grunddata navigering
användar_val = ["de små partierna", "de större partierna", "de två blocken"]

# navigering
left, mid, right = st.beta_columns(3)
with left:
    st.button(
        användar_val[0],
        on_click=__sätt_val_0,
        help="Ligger nära riksdagsspärren i undersökningarna",
    )
with mid:
    st.button(
        användar_val[1], on_click=__sätt_val_1, help="Har minst 6% i undersökningarna"
    )
with right:
    st.button(
        användar_val[2],
        on_click=__sätt_val_2,
        help="Nuvarande regeringsunderlag jämfört med högeroppositionen",
    )

visa_månadsgenomsnitt = st.checkbox(
    "Visa medelvärden",
    value=True,
    help="Visa medelvärden för flera undersökningar ",
)
if visa_månadsgenomsnitt:
    if __vilket_val() == 0:
        chart_u = modell.visa_linje_små_partier()
    elif __vilket_val() == 1:
        chart_u = modell.visa_linje_större_partier()
    else:
        chart_u = modell.visa_block_som_stacked_bar_30_dagars_medel()
else:
    if __vilket_val() == 0:
        chart_u = modell.visa_spridningsdiagram_små_partier()
    elif __vilket_val() == 1:
        chart_u = modell.visa_spridningsdiagram_större_partier()
    else:
        chart_u = modell.visa_block_som_stacked_bar_30_senaste_undesökning()


st.altair_chart(chart_u)


st.write(modell.ge_meddelande_om_dagar_kvar_till_valet())


with st.beta_expander("Data referenser"):
    st.write(
        """
         Avmarkera snittvärden och välj enskilda punkter för att se vilket opinionsinstitut som utfört undersökningen.
         All statistik kan hittas på https://val.digital/"
         Appen använder val.digitals publika repo där opinionssiffror finns samlade: https://github.com/hampusborgos/SwedishPolls/tree/master/Data
     """
    )

