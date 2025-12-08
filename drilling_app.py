# Import Python Libraries
import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from PIL import Image



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