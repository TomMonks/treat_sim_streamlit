import streamlit as st
from PIL import Image
import urllib

INFO_1 = '''**A simple simulation model of a urgent care and treatment centre.**'''
OVERVIEW_PATH = 'txt/overview.md'

@st.experimental_singleton(show_spinner=True)
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

#plain english summary
st.markdown(get_file_content_as_string(OVERVIEW_PATH))
