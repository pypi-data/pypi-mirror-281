import streamlit as st
from qhelper.client import init_client

def main():

    futures = init_client()

    st.sidebar.header('量化投资助手')

    data = st.Page("pages/data.py", title="数据", icon=":material/add_circle:")
    setting = st.Page("pages/setting.py", title="设置", icon=":material/add_circle:")

    pg = st.navigation([data, setting])

    pg.run()

    st.title('量化投资助手')
    st.write(futures["scheduler"].key)
    st.write(futures["scheduler"].status)

if __name__ == '__main__':
    main()