import streamlit as st
import pandas as pd
import numpy as np
import base64
import os, urllib
from utils.get_plots import *
from utils.plottly_test import *
from utils.live_data import *
from lab import *
from multiprocessing import Process
import streamlit as st
import time
import os
import signal
from simple_pid import PID
pid = PID(1, 0.1, 0.05, setpoint=1)

#from uv_vis.save_spectra import *

#table with the results we want next to and download it as csv
# add pressure vs time

st.markdown(f'''
    <style>
    section[data-testid="stSidebar"] .css-ng1t4o {{width: 54rem;}}
    </style>
''',unsafe_allow_html=True)

st.sidebar.markdown("## Setting the Quantum Dots lab")
st.sidebar.markdown("### Select lab equipment")
col1, col2, col3 = st.sidebar.columns([1.2, 0.8, 0.9])

with col1:   
    pump1 = st.selectbox('Select the lab components',  ['Chemyx', 'Milligat_A', 'Milligat_B', 'Milligat_C', 'EuroTherm'])
    pump2 = st.selectbox("",['Chemyx', 'Milligat_A', 'Milligat_B', 'Milligat_C', 'EuroTherm'],  key=0)
    pump3 = st.selectbox("", ['Chemyx', 'Milligat_A', 'Milligat_B', 'Milligat_C', 'EuroTherm'], key=1)

with col2:
    com1 = st.text_input('COM channel') 
    com2 =st.text_input("", key=2)
    com3 =st.text_input("",  key=3)

with col3:
    rate1 = st.text_input('[min, max, step]')
    rate2 = st.text_input("", key=4)
    rate3 = st.text_input("", key=5)

col4, col5 = st.sidebar.columns([1, 1])

with col4:   
    st.selectbox('Analytical equipment',  ['Abs_spectra', 'PL_spectra'], key=6)
    st.selectbox("",  ['Abs_spectra', 'PL_spectra'], key = 7)

with col5:
    st.text_input('Enter the COM channel', key=7) 
    st.text_input("", key=8)


st.sidebar.markdown("## Select the Optimization Strategy")
optimizer = st.sidebar.selectbox('Select optimizer',
                                    ['Single run', 'TSEMO', 'MVMOO', 'External']) 

obj = st.sidebar.checkbox('Set objectives')

if obj:
    left_col, right_col = st.sidebar.columns([1, 1])
    with left_col:
        st.selectbox("", ['Quantum yield', 'Absorption peak', 'FWHM'] , key=8) 
    with right_col:
        st.selectbox("", ['minimize', 'maximize'] , key=8) 

     
#st.sidebar.markdown("## Select the number of optimizations")
number_of_experiments = st.sidebar.slider(
            "# of experiments",
            min_value=1,
            max_value=30,
            value=10,
            help="Select the number of optimizations")

residence_time = st.sidebar.slider(
            "residence time (min)",
            min_value=5,
            max_value=30,
            value=1,
            help="Select the residence time")

col_1, col_2 = st.sidebar.columns([1, 1])
with col_1:
    start = st.sidebar.button("Start")
with col_2:
    stop = st.sidebar.button("Stop")

state =  st.session_state.get(pid=None)


def job():
    for _ in range(100):
        print("In progress")
        time.sleep(1)

if start:
    p = Process(target=job)
    p.start()
    state.pid = p.pid
    st.write("Started process with pid:", state.pid)
    start_experiment(pump_rate_A=rate1, pump_rate_B=rate2, pump_rate_C=None, temperature=None, sampling_time=residence_time*60, com_A=com1, com_B=com2)

if stop:
    os.kill(state.pid, signal.SIGKILL)
    st.write("Stopped process with pid:", state.pid)
    start_experiment(pump_rate_A=0, pump_rate_B=0, pump_rate_C=0, temperature=None, sampling_time=0, com_A=com1, com_B=com2)
    state.pid = None

#if st.sidebar.button('Start the autonomous experiment'):
    
    # with click write these parameters in the config file and run the lab manager
#    st.write('Experiment is now running!')
#    start_experiment(pump_rate_A=rate1, pump_rate_B=rate2, pump_rate_C=None, temperature=None, sampling_time=residence_time*60, com_A=com1, com_B=com2)


#if st.sidebar.button('Stop experiment'):    
#    start_experiment(pump_rate_A=0, pump_rate_B=0, pump_rate_C=0, temperature=None, sampling_time=0, com_A=com1, com_B=com2)


st.markdown('Control Plots: Live monitoring of the experiments')
col6, col7 = st.columns([1, 1])

with col6:
    #st.markdown('Temperature VS time')
    fig1 = temperature_vs_time() # live_temperature_data() #
    st.pyplot(fig1, clear_figure=True)
    #st.image(fig)# call the plot funtion

with col7:
    #st.title('Pump rates VS time')
    fig1 = pump_rate_vs_time()
    st.pyplot(fig1, clear_figure=True)

st.markdown('Results Plots: generated at the end of each completed experiment')
col8, col9 = st.columns([1, 1])
with col8:
    #st.title('UV-VIS spectra')
    fig3 = Abs() # get_absorption(0) #PL_spectra()
    st.pyplot(fig3, clear_figure=True)

with col9:
    fig4= UV_VIS() # get_emmision(0) #  UV_VIS() 
    st.pyplot(fig4, clear_figure=True)

#with col9:
fig = exp_surface()
st.plotly_chart(fig, use_container_width=True)

#col10, col11, col12 = st.columns([1, 1, 1])

#with col10:
#    st.markdown('Quantum Yield')
    # call the plot funtion

#with col11:
#    st.markdown('FWHM')
    #FWHM(df)





# Side bar settings



#col111, col22, col33 = st.sidebar.columns([1, 1, 1])

    



# plot the response surface in 3D by user defined x,y,z in side bar
