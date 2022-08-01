import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

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

@st.cache
def convert_df(df):
   return df.to_csv().encode('utf-8')

@st.cache(show_spinner=False)
def run_experiments(scenarios, n_reps):
    return  md.run_scenario_analysis(cust_scenarios, 
                                     md.DEFAULT_RESULTS_COLLECTION_PERIOD,
                                     n_reps)

@st.cache
def results_as_summary_frame(results):
    return md.scenario_summary_frame(results).round(1)

if 'executed' not in st.session_state:
    st.session_state['executed'] = False

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
    
    button_txt = SHOW_TXT if st.session_state['executed'] else EXECUTE_TXT
    if st.button(button_txt):

        # create the cust scenarios based on upload
        cust_scenarios = create_scenarios(df_scenarios) 
        with st.spinner('Running scenario analysis'):
            # results = md.run_scenario_analysis(cust_scenarios, 
            #                                    md.DEFAULT_RESULTS_COLLECTION_PERIOD,
            #                                    n_reps)
            results = run_experiments(df_scenarios, n_reps)
            st.success('Done!')
            df_results = results_as_summary_frame(results)
            # display in the app
            st.table(df_results)
            st.session_state['executed'] = True
            st.session_state.custom_results = convert_df(df_results)
            

        # this cycles between working and 404 error...
        st.download_button(
        "Download results as .csv",
        st.session_state.custom_results,
        "experiment_results.csv",
        "text/csv",
        key='download-csv'
        )

    

    


    

    


