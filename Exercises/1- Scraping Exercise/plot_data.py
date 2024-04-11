import streamlit as st
import pandas as pd
import plotly.express as px
from exercise import DATA_FILE


st.title("Average World Temperature")

df = pd.read_csv(DATA_FILE)

figure = px.line(x=df['date'], y=df['temperature'], labels={
    'x': 'Dates', 'y': 'Temperatures (C)'})

st.plotly_chart(figure)
