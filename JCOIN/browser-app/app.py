import streamlit as st
import pandas as pd
import numpy as np
import subprocess
from gen3.auth import Gen3Auth
from gen3.tools.download import drs_download

st.title('Uber pickups in NYC')

DATE_COLUMN = 'date/time'

def download_data():
    auth = Gen3Auth()
    drs_download.download_drs_object(hostname='jcoin.datacommons.io', auth=auth,
                                     object_id='dg.6VTS/ea37e427-f142-4ddc-a9d4-4c2a9d2b3385',
                                     output_dir='.')
    subprocess.run(['gpg', '--batch', '--yes', '--passphrase', st.secrets['PASSPHRASE'],
                    '--output', 'uber-raw-data-sep14.csv.gz',
                    '--decrypt', 'uber-raw-data-sep14.csv.gz.gpg'])

@st.cache
def load_data(nrows):
    data = pd.read_csv('uber-raw-data-sep14.csv.gz', nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

download_data()
data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Done! (using st.cache)")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Number of pickups by hour')
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

# Some number in the range 0-23
hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

st.subheader('Map of all pickups at %s:00' % hour_to_filter)
st.map(filtered_data)
