import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import model as md



TITLE = 'Create custom experiments'
INFO_3 = '### Upload custom scenarios and compare results.'
INFO_4 = '> Notes: values are interpretted as relative changes to parameters. '
INFO_5 = 'Resources counts are bounded at 0.'


def create_scenarios(df_scenarios):
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

@st.cache
def download_results(results_df):
    results_csv = convert_df(df)

st.title(TITLE)
st.markdown(INFO_3)


uploaded_file = st.file_uploader("Choose a file")
df_scenarios = pd.DataFrame()
if uploaded_file is not None:
    # assumes CSV
    df_scenarios = pd.read_csv(uploaded_file, index_col=0)
    st.write('**Loaded Scenarios**')
    st.table(df_scenarios)
    st.markdown(INFO_4 + INFO_5)

    # loop through scenarios, create and run model

    if st.button('Run custom scenarios'):

        # create the cust scenarios based on upload
        cust_scenarios = create_scenarios(df_scenarios) 
        with st.spinner('Running scenario analysis'):
            results = md.run_scenario_analysis(cust_scenarios, 
                                            md.DEFAULT_RESULTS_COLLECTION_PERIOD,
                                            5)
            st.success('Done!')
            df_results = md.scenario_summary_frame(results).round(1)
            # display in the app
            st.table(df_results)



        st.download_button(
        "Download results",
        convert_df(df_results),
        "experiment_results.csv",
        "text/csv",
        key='download-csv'
        )

    

    


    

    


