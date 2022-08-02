import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pyperclip

# widgets and JS events from bokeh to execute copy to clipboard
from bokeh.models.widgets import Button
from bokeh.models import CustomJS

# return bokeh events from streamlit
from streamlit_bokeh_events import streamlit_bokeh_events

import model as md

TITLE = 'Create custom experiments'
INFO_3 = '### Upload custom scenarios and compare results.'
INFO_4 = '> Notes: values are interpretted as relative changes to parameters. '
INFO_5 = 'Resources counts are bounded at 0.'
EXECUTE_TXT = 'Execute custom experiments'
SHOW_TXT = 'Show results'

def create_scenarios(df_scenarios):
    '''
    Returns dictionary of Scenario object based on contents of a dataframe

    Params:
    ------
    df_scenarios: pandas.DataFrame
        Dataframe of scenarios.  First two columns are id, name followed by variable names.  
        no fixed width

    Returns:
    --------
    dict

    Notes:
    -----
    No validation is currently done.  This will crash when format or variable names do not 
    meet assumptions or are invalid.
    '''
    cust_scenarios = {}
    for index, row in df_scenarios.iterrows():
        scenario_i = md.Scenario()
        # loop through variable names
        for var_name in df_scenarios.columns.tolist()[2:]:
            # get the value for update
            current_value = getattr(scenario_i, var_name)

            # update the variable using the relative
            setattr(scenario_i, var_name, current_value + row[var_name])

        cust_scenarios[row['name']] = scenario_i

    return cust_scenarios

@st.cache(show_spinner=False)
def convert_df(df):
   return df.to_csv().encode('utf-8')

@st.cache(show_spinner=False)
def run_experiments(scenarios, n_reps):
    return  md.run_scenario_analysis(scenarios, 
                                     md.DEFAULT_RESULTS_COLLECTION_PERIOD,
                                     n_reps)

@st.cache
def results_as_summary_frame(results):
    return md.scenario_summary_frame(results).round(1)


st.title(TITLE)
st.markdown(INFO_3)


uploaded_file = st.file_uploader("Choose a file")
df_results = pd.DataFrame()
if uploaded_file is not None:
    # assumes CSV
    df_scenarios = pd.read_csv(uploaded_file, index_col=0)
    st.write('**Loaded Experiments**')
    st.table(df_scenarios)
    st.markdown(INFO_4 + INFO_5)

    # loop through scenarios, create and run model
    n_reps = st.slider('Replications', 3, 30, 5, step=1)
    
    if st.button(EXECUTE_TXT):

        # create the cust scenarios based on upload
        cust_scenarios = create_scenarios(df_scenarios) 
        with st.spinner('Running scenario analysis'):
            results = run_experiments(cust_scenarios, n_reps)
            st.success('Done!')
            df_results = results_as_summary_frame(results)
            # display in the app via table
            st.table(df_results)
            

        # STREAMLIT BUG: this cycles between working and 404 error...
        st.download_button(
        "Download results as .csv",
        convert_df(df_results),
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
    

    


