import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import model as md
from PIL import Image

INFO_1 = '''A simple simulation model of a urgent care and treatment centre.  
Change the model parameters and rerun to see the effect on waiting times and 
utilisation of rooms '''

INFO_2 = 'Run a total of 5 pre-specified scenarios and compare results'

def get_arrival_chart():
    '''
    Quick and load of arrival pattern as matplotlib ax

    Returns:
    --------
    fig 
    '''
    arrivals = pd.read_csv(md.NSPP_PATH)
    # visualise
    ax = arrivals.plot(y='arrival_rate', x='period', rot=45,
                                    kind='bar',figsize=(12,5), legend=False)
    ax.set_xlabel('hour of day')
    ax.set_ylabel('mean arrivals')

    return ax.figure

st.title('Treatment Centre Simulation Model')
st.text(INFO_1)

# Using "with" notation
with st.sidebar:
    st.markdown('# Parameters')
   
    triage_bays = st.slider('Triage bays', 1, 5, 1)
    exam_rooms = st.slider('Exam rooms', 1, 5, 1)
    treat_rooms = st.slider('Treatment rooms', 1, 5, 1)

    # proportion of patients triaged as trauma
    trauma_p = st.slider('Probability trauma patient', 0.0, 1.0, 
                          md.DEFAULT_PROB_TRAUMA)
    
    # proportion of non-trauma patients that require treatment
    nontrauma_treat = st.slider('Probability non-trauma treatment', 0.0, 1.0, 
                          md.DEFAULT_NON_TRAUMA_TREAT_P)

    replications = st.slider('Multiple runs', 1, 50, 10)

with st.expander('Daily Arrival Pattern', expanded=False):
    st.pyplot(get_arrival_chart())

with st.expander('Pre-specified Scenarios', expanded=False):
    st.text(INFO_2)

    if st.button('Run all scenarios and compare'):
        scenarios = md.get_scenarios()
        with st.spinner('Running scenario analysis'):
            results = md.run_scenario_analysis(scenarios, 
                                               md.DEFAULT_RESULTS_COLLECTION_PERIOD,
                                               replications)
            st.success('Done!')
            st.dataframe(md.scenario_summary_frame(results).round(1))

    
args = md.Scenario()
args.n_triage = triage_bays
args.n_exam = exam_rooms
args.p_trauma_dist = trauma_p
args.p_trauma = nontrauma_treat

if st.button('Run Single Scenario'):
    # Get results
    with st.spinner('Simulating the treatment centre...'):
        results = md.multiple_replications(args, n_reps = replications)
    st.success('Done!')
    st.dataframe(results.mean().round(1))
    
image = Image.open('img/nihr.png')
st.image(image)