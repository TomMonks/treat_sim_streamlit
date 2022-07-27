import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from zmq import PROBE_ROUTER
import model as md
from PIL import Image

INFO_1 = '''**A simple simulation model of a urgent care and treatment centre.**'''
INFO_1a = '''**Change the model parameters and rerun to see the effect on waiting times and 
utilisation of rooms**'''

INFO_2 = '**Run 5 pre-specified scenarios and compare results.**'

INFO_3 = '''**Trauma arrivals:**
patients with severe illness and trauma that must first be stablised in a 
trauma room. These patients then undergo treatment in a cubicle before being 
discharged.'''

INFO_4 = '''**Non-trauma arrivals**
patients with minor illness and no trauma go through registration and 
examination activities. A proportion of non-trauma patients require treatment
in a cubicle before being dicharged. '''

SC_TABLE = '''
|   | Scenario                | Description                                                          |
|---|-------------------------|----------------------------------------------------------------------|
| 1 | As-is                   | Uses default settings - represents how the system currently operates |
| 2 | Triage + 1              | Add an additional triage bay for new patients                        |
| 3 | Exam + 1                | Add an additional examination cubicle for the non-trauma pathway     |
| 4 | Treat + 1               | Add an extra non-trauma treatment cubicle                            |
| 5 | Swap Exam & Treat       | Convert an exam room into a non_trauma treatment cubicle             |
| 6 | Scenario 5 + short exam | Scenario 5 changes + examination takes 4 mins less on average        |

'''

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


st.set_page_config(
     #page_title="Ex-stream-ly Cool App",
     #page_icon="🧊",
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={
     #    'Get Help': 'https://www.extremelycoolapp.com/help',
     #    'Report a bug': "https://www.extremelycoolapp.com/bug",
         'About': "## Treatment centre sim.  Adapted from Nelson (2013)."
     }
 )

st.title('Treatment Centre Simulation Model')

image = Image.open('img/nihr.png')
st.image(image)

st.markdown(INFO_1)

# Using "with" notation
with st.sidebar:
    st.markdown('# Parameters')
    
    st.markdown('## Capacity constraints')
   
    triage_bays = st.slider('Triage bays', 1, 5, md.DEFAULT_N_TRIAGE)
    exam_rooms = st.slider('Exam rooms', 1, 5, md.DEFAULT_N_EXAM)
    treat_rooms = st.slider('Treatment cubicles', 1, 5, md.DEFAULT_N_CUBICLES_1, 
                            help='Set the number of non trauma pathway treatment cubicles')

    st.markdown('## Trauma Pathway') 
    # proportion of patients triaged as trauma
    trauma_p = st.slider('Probability trauma patient', 0.0, 1.0, 
                          md.DEFAULT_PROB_TRAUMA, 0.01)

    trauma_mean = st.slider('Mean treatment time', 0.0, 100.0, 
                          md.DEFAULT_TRAUMA_TREAT_MEAN, 1.0)

    trauma_var = st.slider('Variance of treatment time', 0.0, 10.0, 
                             md.DEFAULT_TRAUMA_TREAT_VAR, 0.5)

    st.markdown('## Non-Trauma Pathway') 

    #examination mean
    exam_mean = st.slider('Mean examination time', 0.0, 45.0, 
                          md.DEFAULT_EXAM_MEAN, 1.0)
    
    exam_var = st.slider('Variance of examination time', 0.0, 15.0, 
                          md.DEFAULT_EXAM_VAR, 0.5)

    # proportion of non-trauma patients that require treatment
    nontrauma_treat = st.slider('Probability non-trauma treatment', 0.0, 1.0, 
                          md.DEFAULT_NON_TRAUMA_TREAT_P)

    nt_trauma_mean = st.slider('Mean treatment time', 0.0, 100.0, 
                          md.DEFAULT_NON_TRAUMA_TREAT_MEAN, 1.0)

    nt_trauma_var = st.slider('Variance of treatment time', 0.0, 10.0, 
                             md.DEFAULT_NON_TRAUMA_TREAT_VAR, 0.5)
                            

    st.markdown('## Model execution')
    replications = st.slider('Multiple runs', 1, 50, 10)

# put info in columns
col1, col2 = st.columns(2)
with col1.expander('Treatment process', expanded=False):
    st.image('img/process_flow_img.jpg')
    st.markdown(INFO_3)
    st.markdown(INFO_4)

with col2.expander('Daily Arrival Pattern', expanded=False):
    st.pyplot(get_arrival_chart())

st.markdown(INFO_1a)

# set up scenario    
args = md.Scenario()
args.n_triage = triage_bays
args.n_exam = exam_rooms
args.treat_trauma_mean = trauma_mean
args.treat_trauma_var = trauma_var
args.nt_treat_prob = nontrauma_treat
args.nt_treat_mean = nt_trauma_mean
args.nt_treat_var = nt_trauma_var
args.prob_trauma = trauma_p
args.exam_mean = exam_mean
args.exam_var = exam_var

if st.button('Simulate treatment centre'):
    # Get results
    with st.spinner('Simulating the treatment centre...'):
        results = md.multiple_replications(args, n_reps = replications)
    st.success('Done!')
    st.table(results.mean().round(1))