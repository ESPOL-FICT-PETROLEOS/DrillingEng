# Import Python Libraries
import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from PIL import Image

# Import Python Libraries
import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from PIL import Image

# SECCIÓN AGREGADA: LIBRERÍAS MATEMÁTICAS
import numpy as np
from collections import namedtuple
from math import radians, acos, asin, cos, sin, tan, atan, degrees, sqrt

# Insert an icon
icon = Image.open("Resources/dd.jpg")

# State the design of the app
st.set_page_config(page_title="Drilling App", page_icon=icon)

# Inset CSS Codes to improve the design of the app
st.markdown(
    """
<style>
h1 {text-align: center;
}
body {background-color: #DCE3D5;
      width: 1400px;
      margin: 15px auto;
}
footer {
  display: none;
}
</style>""",
    unsafe_allow_html=True,
)


# Insert title for app
st.title("Drilling Engineering App")

st.write("---")

# Add information of the app
st.markdown("""
This app is going to be used to visualize 3D Wells, as well as
to calculate directional parameters of deviated wells.

**Python Libraries:** **streamlit**, *plotly*, pandas, Pillow.
""")


# Add additional information (expander)
expander = st.expander("Information")
expander.write("This app is used to calculate drilling parameters.")


# Insert an image
image = Image.open("Resources/well.jpg")
st.image(image, width=1400, use_container_width=True)

# Insert subheader
st.subheader("**Drilling Parameters**")

# Insert a video
video = open("Resources/drilling.mp4", "rb")
st.video(video)

# Insert caption
st.caption("*Video about directional wells.*")

# Sidebar section
logo = Image.open("Resources/ESPOL.png")
st.sidebar.image(logo, use_container_width=True)

# Add title to the sidebar section
st.sidebar.title("⬇ Navigation")

# Upload files
file = st.sidebar.file_uploader("Upload your csv file")

# Add sections of the app
with st.sidebar:
    options = option_menu(menu_title="Menu", options=["Home", "Data", "3D Plots", "Basic Calculations"],
                          icons=["house", "database-fill", "tv-fill", "calculator"])


# Useful functions to activate each section
# Function to check data
def data(dataframe):
    # Check first 5 rows
    st.subheader("Dataframe")
    st.write(dataframe.head())
    # Check statistical summary
    st.subheader("Statistical summary")
    st.write(dataframe.describe())


# Function to visualize 3D Wells
def plots(dataframe):
    st.subheader("Visualize 3D Trajectory of a well")
    x = st.selectbox("Choose DispNS", dataframe.columns)
    y = st.selectbox("Choose DispEW", dataframe.columns)
    z = st.selectbox("Choose TVD", dataframe.columns)
    fig = px.line_3d(dataframe, x, y, z)
    st.plotly_chart(fig)


# Call data and sections
if file:
    df = pd.read_csv(file)

    if options == "Data":
        data(df)

    elif options == "3D Plots":
        plots(df)



# Marco Aspiazu (Sanyu)
# Estructuras de datos
Data_J = namedtuple("Input_J", "TVD KOP BUR DH")
Output_J = namedtuple("Output_J", "R Theta TVD_EOB Md_EOB Dh_EOB Tan_len Md_total")

Data_S = namedtuple("Input_S", "TVD KOP BUR DOR DH")
Output_S = namedtuple("Output_S",
                      "R1 R2 Theta TVD_EOB Md_EOB Dh_EOB Tan_len Md_SOD TVD_SOD Dh_SOD Md_total")

Data_H = namedtuple("Input_H", "TVD KOP BUR1 BUR2 DH")
Output_H = namedtuple("Output_H",
                      "R1 R2 Theta TVD_EOB1 Md_EOB1 Dh_EOB1 Tan_len Md_SOB2 Md_total")


# Función Tipo J
def well_J(data: Data_J, unit='ingles') -> Output_J:
    tvd = data.TVD;
    kop = data.KOP;
    bur = data.BUR;
    dh = data.DH

    if unit == 'ingles':
        R = 5729.58 / bur
    else:
        R = 1718.87 / bur

    if dh > R:
        dc = dh - R
    elif dh < R:
        dc = R - dh
    else:
        dc = 0

    do = tvd - kop
    doc = degrees(atan(dc / do))
    oc = sqrt(dc ** 2 + do ** 2)

    # Manejo seguro de acos
    val_acos = R / oc
    if val_acos > 1: val_acos = 1
    if val_acos < -1: val_acos = -1
    boc = degrees(acos(val_acos))

    if R < dh:
        bod = boc - doc
    elif R > dh:
        bod = boc + doc
    else:
        bod = boc

    theta = 90 - bod
    tvd_eob = kop + abs(R * sin(radians(theta)))
    dh_eob = R - R * cos(radians(theta))
    tan_len = sqrt(oc ** 2 - R ** 2)

    if unit == 'ingles':
        md_eob = kop + (theta / bur) * 100
        md_total = kop + (theta / bur) * 100 + tan_len
    else:
        md_eob = kop + (theta / bur) * 30
        md_total = kop + (theta / bur) * 30 + tan_len

    return Output_J(R, theta, tvd_eob, md_eob, dh_eob, tan_len, md_total)


# Función Tipo S
def well_S(data: Data_S, unit='ingles'):
    tvd = data.TVD;
    kop = data.KOP;
    bur = data.BUR;
    dor = data.DOR;
    dh = data.DH

    if unit == 'ingles':
        R1 = 5729.58 / bur; R2 = 5729.58 / dor
    else:
        R1 = 1718.87 / bur; R2 = 1718.87 / dor

    if dh > (R1 + R2):
        fe = dh - (R1 + R2)
    elif dh < (R1 + R2):
        fe = R1 - (dh - R2)
    else:
        fe = 0

    eo = tvd - kop
    foe = degrees(atan(fe / eo))
    of = sqrt(fe ** 2 + eo ** 2)
    fg = R1 + R2

    val_asin = fg / of
    if val_asin > 1: val_asin = 1
    fog = degrees(asin(val_asin))

    theta = fog - foe
    tvd_eob = kop + R1 * sin(radians(theta))
    dh_eob = R1 - abs(R1 * cos(radians(theta)))
    tan_len = sqrt(of ** 2 - fg ** 2)
    tvd_sod = tvd_eob + tan_len * abs(cos(radians(theta)))
    dh_sod = dh_eob + abs(tan_len * sin(radians(theta)))

    if unit == 'ingles':
        md_eob = kop + (theta / bur) * 100
        md_sod = kop + (theta / bur) * 100 + tan_len
        md_total = kop + (theta / bur) * 100 + tan_len + (theta / dor) * 100
    else:
        md_eob = kop + (theta / bur) * 30
        md_sod = kop + (theta / bur) * 30 + tan_len
        md_total = kop + (theta / bur) * 30 + tan_len + (theta / dor) * 30

    return Output_S(R1, R2, theta, tvd_eob, md_eob, dh_eob, tan_len, md_sod, tvd_sod,
                    dh_sod, md_total)


# Función Tipo Horizontal
def Well_H(data_h: Data_H, unit="ingles") -> Output_H:
    tvd = data_h.TVD;
    kop = data_h.KOP;
    bur1 = data_h.BUR1;
    bur2 = data_h.BUR2;
    dh = data_h.DH

    if unit == 'ingles':
        R1 = 5729.58 / bur1; R2 = 5729.58 / bur2
    else:
        R1 = 1718.87 / bur1; R2 = 1718.87 / bur2

    EG = (tvd - kop) - R2
    EO = dh - R1
    A_GOE = np.arctan(EG / EO) * 180 / np.pi
    OG = (EG * 2 + EO) * 0.5
    OF = R1 - R2

    val_arccos = OF / OG
    if val_arccos > 1: val_arccos = 1
    if val_arccos < -1: val_arccos = -1
    A_GOF = np.arccos(val_arccos) * 180 / np.pi

    A_AOB = 180 - A_GOE - A_GOF
    TVD_V2 = kop + R1 * np.sin(A_AOB * np.pi / 180)

    D1 = R1 - R1 * np.cos(A_AOB * np.pi / 180)
    BC = (OG * 2 - OF) * 0.5
    D2 = D1 + BC * np.sin(A_AOB * np.pi / 180)
    A_GCD = 90 - (90 - A_GOF) - (90 - A_GOE)

    if unit == 'ingles':
        MD_EOB1 = kop + (A_AOB / bur1) * 100
        MD_SOB2 = MD_EOB1 + BC
        MDT = MD_SOB2 + (A_GCD / bur2) * 100
    else:
        MD_EOB1 = kop + (A_AOB / bur1) * 30
        MD_SOB2 = MD_EOB1 + BC
        MDT = MD_SOB2 + (A_GCD / bur2) * 30

    return Output_H(R1, R2, A_AOB, TVD_V2, MD_EOB1, D1, BC, MD_SOB2, MDT)


# SECCIÓN AGREGADA: LÓGICA DE BASIC CALCULATIONS

if options == "Basic Calculations":
    st.header("Directional Calculations")

    # Units
    st.subheader("Units")
    unit_system = st.selectbox("Units", ["English", "Metric"])
    unit_key = 'ingles' if unit_system == "English" else 'metrico'
    suffix = "ft" if unit_system == "English" else "m"
    bur_suffix = "°/100ft" if unit_system == "English" else "°/30m"

    # Well Type
    st.subheader("Well Type")
    check_j = st.checkbox("J-Type")
    check_s = st.checkbox("S-Type")
    check_h = st.checkbox("Horizontal")

    st.write("---")

    # ---------- J-TYPE ----------
    if check_j:
        st.subheader("J-Type Inputs")
        c1, c2 = st.columns(2)

        with c1:
            j_tvd = st.number_input("TVD", min_value=0.0, value=8000.0)
            j_kop = st.number_input("KOP", min_value=0.0, value=500.0)

        with c2:
            j_bur = st.number_input(f"BUR [{bur_suffix}]", min_value=0.1, value=2.0)
            j_dh = st.number_input("DH", min_value=0.0, value=970.8)

        if st.button("Calculate"):
            st.subheader("J-Type Results")
            res = well_J(Data_J(j_tvd, j_kop, j_bur, j_dh), unit=unit_key)

            st.success(f"R: {res.R:.3f} {suffix}")
            st.success(f"θ max: {res.Theta:.3f} °")
            st.success(f"TVD@EOB: {res.TVD_EOB:.3f} {suffix}")
            st.success(f"MD@EOB: {res.Md_EOB:.3f} {suffix}")
            st.success(f"DH@EOB: {res.Dh_EOB:.3f} {suffix}")
            st.success(f"Tangent: {res.Tan_len:.3f} {suffix}")
            st.success(f"MD total: {res.Md_total:.3f} {suffix}")

    # ---------- S-TYPE ----------
    if check_s:
        st.write("---")
        st.subheader("S-Type Inputs")
        c1, c2 = st.columns(2)

        with c1:
            s_tvd = st.number_input("TVD", min_value=0.0, value=12000.0)
            s_kop = st.number_input("KOP", min_value=0.0, value=6084.0)
            s_dh = st.number_input("DH", min_value=0.0, value=3500.0)

        with c2:
            s_bur = st.number_input(f"BUR [{bur_suffix}]", min_value=0.1, value=3.0)
            s_dor = st.number_input(f"DOR [{bur_suffix}]", min_value=0.1, value=2.0)

        if st.button("Calculate"):
            st.subheader("S-Type Results")
            res = well_S(Data_S(s_tvd, s_kop, s_bur, s_dor, s_dh), unit=unit_key)

            st.success(f"R₁: {res.R1:.3f} {suffix}")
            st.success(f"R₂: {res.R2:.3f} {suffix}")
            st.success(f"θ max: {res.Theta:.3f} °")
            st.success(f"TVD@EOB: {res.TVD_EOB:.3f} {suffix}")
            st.success(f"MD@EOB: {res.Md_EOB:.3f} {suffix}")
            st.success(f"DH@EOB: {res.Dh_EOB:.3f} {suffix}")
            st.success(f"Tangent: {res.Tan_len:.3f} {suffix}")
            st.success(f"MD@SOD: {res.Md_SOD:.3f} {suffix}")
            st.success(f"TVD@SOD: {res.TVD_SOD:.3f} {suffix}")
            st.success(f"DH@SOD: {res.Dh_SOD:.3f} {suffix}")
            st.success(f"MD total: {res.Md_total:.3f} {suffix}")

    # ---------- HORIZONTAL ----------
    if check_h:
        st.write("---")
        st.subheader("Horizontal Inputs")
        c1, c2 = st.columns(2)

        with c1:
            h_tvd = st.number_input("TVD", min_value=0.0, value=3800.0)
            h_kop = st.number_input("KOP", min_value=0.0, value=2000.0)
            h_dh = st.number_input("DH", min_value=0.0, value=1800.0)

        with c2:
            h_bur1 = st.number_input(f"BUR₁ [{bur_suffix}]", min_value=0.1, value=5.73)
            h_bur2 = st.number_input(f"BUR₂ [{bur_suffix}]", min_value=0.1, value=9.55)

        if st.button("Calculate"):
            st.subheader("Horizontal Results")
            res = Well_H(Data_H(h_tvd, h_kop, h_bur1, h_bur2, h_dh), unit=unit_key)

            st.success(f"R₁: {res.R1:.3f} {suffix}")
            st.success(f"R₂: {res.R2:.3f} {suffix}")
            st.success(f"θ: {res.Theta:.3f} °")
            st.success(f"TVD@EOB1: {res.TVD_EOB1:.3f} {suffix}")
            st.success(f"MD@EOB1: {res.Md_EOB1:.3f} {suffix}")
            st.success(f"DH@EOB1: {res.Dh_EOB1:.3f} {suffix}")
            st.success(f"Tangent: {res.Tan_len:.3f} {suffix}")
            st.success(f"MD@SOB2: {res.Md_SOB2:.3f} {suffix}")
            st.success(f"MD total: {res.Md_total:.3f} {suffix}")
