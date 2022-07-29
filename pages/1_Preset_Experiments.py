import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import model as md

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

TITLE = 'Run multiple experiments'
INFO_2 = '### Run 5 pre-specified scenarios and compare results.'


@st.cache
def convert_df(df):
   return df.to_csv().encode('utf-8')

st.title(TITLE)
st.markdown(INFO_2)

st.markdown(SC_TABLE)
st.markdown('')
if st.button('Run all scenarios and compare'):
    scenarios = md.get_scenarios()
    with st.spinner('Running scenario analysis'):
        results = md.run_scenario_analysis(scenarios, 
                                            md.DEFAULT_RESULTS_COLLECTION_PERIOD,
                                            5)
        st.success('Done!')

        df_results = md.scenario_summary_frame(results).round(1)
        st.table(df_results)

        # this removes the table above from the app - how to avoid?
        st.download_button(
        "Download results as .csv",
        convert_df(df_results),
        "experiment_results.csv",
        "text/csv",
        key='download-csv'
        )




    

    


    

    


