### Import
import streamlit as st
import pandas as pd

# Cach data @st.cache_data
### Config
st.set_page_config(
    page_title="Streamlit",
    page_icon="🧑",
    layout="wide",
    initial_sidebar_state="expanded",
)

### Title et markdown : st.title et st.markdown
st.title("My streamlit App")

### Checkbox st.checkbox
@st.cache_data
def load_data():
    df = pd.read_csv("train.csv", sep=';')
    return df

df = load_data()

if st.checkbox("Show Dataframe"):
    st.write(df)


### Selectbox st.selectbox



### Forms st.form, st.form_submit_button et st.select_slider



### Columns st.columns



### Graphique Histogramme avec matplotlib.pyplot, seaborn et st.pyplot


### Image avec st.image


### Graphique Histogramme px.histogram et st.plotly_chart



### Graphique Pie chart px.pie et st.plotly_chart



### + De graphiques ici : https://plotly.com/python/


