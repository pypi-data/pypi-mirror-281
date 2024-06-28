import streamlit as st
from dask.distributed import Client
from .scheduler import init_scheduler

@st.cache_resource
def init_client():
    client = Client()
    futures = {
        "scheduler": client.submit(init_scheduler)
    }

    print(client.dashboard_link)
    return futures