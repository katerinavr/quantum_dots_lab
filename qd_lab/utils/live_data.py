import time
import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts
import streamlit as st  # 🎈 data web app development
import matplotlib.pyplot as plt

# read csv from the data file or a cloud adress if available
dataset_url = "qd_lab/data/temperature_vs_time.csv"

# read csv from a URL
#@st.experimental_memo
def get_data():# -> pd.DataFrame:
    return pd.read_csv(dataset_url)

def live_temperature_data():
    placeholder = st.empty()
    df = get_data()
    #print(df.columns.values)
    fig = plt.figure()
    counter = 0
    for seconds in range(200):
        counter += 1
        df["temperature_new"] = df["temperature"] * np.random.choice(range(1, 5))
        df["time_new"] = counter

    with placeholder.container():
        #st.markdown("### First Chart")
        fig = px.scatter(df, x = 'time_new', y= 'temperature_new')
        #plt.xlabel('Time')
        #plt.ylabel('Temperature')
        #st.write(fig)
        #st.markdown("### Detailed Data View")
        #st.dataframe(df)
        time.sleep(1)
        st.write(fig)