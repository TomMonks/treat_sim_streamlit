import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
# widgets and JS events from bokeh to execute copy to clipboard
from bokeh.models.widgets import Button
from bokeh.models import CustomJS

# return bokeh events from streamlit
from streamlit_bokeh_events import streamlit_bokeh_events

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

@st.cache(show_spinner=False)
def run_experiments(scenarios, n_reps):
    return  md.run_scenario_analysis(scenarios, 
                                     md.DEFAULT_RESULTS_COLLECTION_PERIOD,
                                     n_reps)


def main():

    st.title(TITLE)
    st.markdown(INFO_2)

    st.markdown(SC_TABLE)
    st.markdown('')

    # get all the scenarios
    df_results = pd.DataFrame()

    if st.button('Run all scenarios and compare'):

        scenarios = md.get_scenarios()
        print(scenarios)
        
        with st.spinner('Running scenario analysis'):
            # will only compute once... due to cache
            results = run_experiments(scenarios, 5)
            st.success('Done!')
            df_results = md.scenario_summary_frame(results).round(1)
            #with st.expander('Tabular Results', expanded=True):


            st.table(df_results)
            print(df_results.to_csv().encode('utf-8'))

            # this removes the table above from the app - how to avoid?
            st.download_button(
            "Download results as .csv",
            df_results.to_csv().encode('utf-8'),
            "experiment_results.csv",
            "text/csv",
            key='download-csv'
            )

            # copy paste workaround for STREAMLIT Bug
            # code based on https://discuss.streamlit.io/t/copy-dataframe-to-clipboard/2633
            copy_button = Button(label="Copy results to clipboard")
            copy_button.js_on_event("button_click", CustomJS(args=dict(df=df_results.to_csv(sep='\t')), code="""
                navigator.clipboard.writeText(df);
                """))
                
            no_event = streamlit_bokeh_events(
                copy_button,
                events="GET_TEXT",
                key="get_text",
                refresh_on_update=True,
                override_height=75,
                debounce_time=0)

if __name__ == '__main__':
    main()


    

    


    

    


