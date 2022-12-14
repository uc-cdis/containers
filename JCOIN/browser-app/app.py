import streamlit as st
import os
import pandas as pd
import numpy as np
import subprocess

from gen3.auth import Gen3Auth
from gen3.tools.download import drs_download


ENCRYPTED_FILE_GUID = "dg.6VTS/ea37e427-f142-4ddc-a9d4-4c2a9d2b3385"
ENCRYPTED_FILE_NAME = "uber-raw-data-sep14.csv.gz.gpg"
DECRYPTED_FILE_NAME = "uber-raw-data-sep14.csv.gz"
DATE_COLUMN = "date/time"


def download_data():
    assert "HOSTNAME" in os.environ, "'HOSTNAME' env var is required"
    assert "NAMESPACE" in os.environ, "'NAMESPACE' env var is required"  # for Gen3Auth
    auth = Gen3Auth()
    drs_download.download_drs_object(
        hostname=os.environ["HOSTNAME"],
        auth=auth,
        object_id=ENCRYPTED_FILE_GUID,
        output_dir=".",
    )
    if not os.path.exists(DECRYPTED_FILE_NAME):
        raise Exception(f"Failed to download '{DECRYPTED_FILE_NAME}' (GUID '{ENCRYPTED_FILE_GUID}')")
    subprocess.run(
        [
            "gpg",
            "--batch",
            "--yes",
            "--passphrase",
            st.secrets["PASSPHRASE"],
            "--output",
            DECRYPTED_FILE_NAME,
            "--decrypt",
            ENCRYPTED_FILE_NAME,
        ]
    )


@st.cache
def load_data(nrows):
    data = pd.read_csv(DECRYPTED_FILE_NAME, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data


if __name__ == "__main__":
    st.title("Uber pickups in NYC")

    download_data()
    data_load_state = st.text("Loading data...")
    data = load_data(10000)
    data_load_state.text("Done! (using st.cache)")

    if st.checkbox("Show raw data"):
        st.subheader("Raw data")
        st.write(data)

    st.subheader("Number of pickups by hour")
    hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0, 24))[0]
    st.bar_chart(hist_values)

    # Some number in the range 0-23
    hour_to_filter = st.slider("hour", 0, 23, 17)
    filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

    st.subheader("Map of all pickups at %s:00" % hour_to_filter)
    st.map(filtered_data)
