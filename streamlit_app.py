import streamlit as st
from PIL import Image
from itertools import compress
import data_access as da
from streamlit.caching import cache
import model_chart


def visa_senaste_under_sökningarna(modell):
    st.write("Senaste undersökningarna")
    df_show = modell.df.tail(4)[::-1][["Publiceringsdatum", "V", "S", "MP", "C", "L", "M", "KD", "SD", "Institut"]]
    df_show["Institut"] = df_show["Institut"] + df_show["Publiceringsdatum"].dt.strftime(" %m-%d")
    df_show.set_index("Institut", inplace=True)
    df_show = df_show[["V", "S", "MP", "C", "L", "M", "KD", "SD"]]
    st.table(df_show.style.format({
    "V": "{:.1f}",
    "S": "{:.1f}",
    "MP": "{:.1f}",
    "C": "{:.1f}",
    "L": "{:.1f}",
    "M": "{:.1f}",
    "KD": "{:.1f}",
    "SD": "{:.1f}"},
    ))

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
@st.cache
def get_model():
    return model_chart.ModelChart()
modell = get_model()

# grunddata navigering
användar_val = ["de små partierna", "de större partierna", "de två blocken"]

# navigering
left, mid, right = st.columns(3)
with left:
    #st.button(
    st.button(label=användar_val[0], on_click=__sätt_val_0, help="Ligger nära riksdagsspärren i undersökningarna")
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


if __vilket_val() == 0:
    chart_u1 = modell.visa_spridningsdiagram_små_partier()
    chart_u2 = modell.visa_linje_små_partier()
elif __vilket_val() == 1:
    chart_u1 = modell.visa_spridningsdiagram_större_partier()
    chart_u2 = modell.visa_linje_större_partier()
else:
    chart_u1 = modell.visa_linje_för_block()
    chart_u2 = modell.visa_block_som_stacked_bar_senaste_4_undesökningar()


st.altair_chart(chart_u1)

if (__vilket_val() != 2):
    st.write(modell.ge_meddelande_om_dagar_kvar_till_valet())
    visa_senaste_under_sökningarna(modell)
    st.altair_chart(chart_u2)
else:
    st.altair_chart(chart_u2)
    st.write(modell.ge_meddelande_om_dagar_kvar_till_valet())
    visa_senaste_under_sökningarna(modell)

with st.expander("Data referens"):
    st.write(
        """
            Mer statistik kan hittas på 
            https://val.digital/".
            Den här sidan använder 
            val.digitals publika github repo 
            där opinions finns samlade.
        """
    )

