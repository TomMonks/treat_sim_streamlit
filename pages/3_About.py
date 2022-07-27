import streamlit as st
import urllib

FILE = 'txt/acknowledgement.md'

def get_file_content_as_string(path):
    '''
    Download the content of a file from the GitHub Repo and return as a utf-8 string

    Notes:
    -------
        temporarily this is pointing at the `dev` branch

        adapted from 'https://github.com/streamlit/demo-self-driving'

    Parameters:
    ----------
    path: str
        e.g. file_name.md

    Returns:
    --------
    utf-8 str

    '''
    url = 'https://raw.githubusercontent.com/TomMonks/treat_sim_streamlit/dev/' + path
    response = urllib.request.urlopen(url)
    return response.read().decode("utf-8")

st.markdown(get_file_content_as_string(FILE))

