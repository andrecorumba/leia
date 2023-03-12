import streamlit as st

def about():
    st.image('../images/logo.png', width=200)
    with open('../README.md') as f:
        readme = f.read()
    st.markdown(readme, unsafe_allow_html=True)