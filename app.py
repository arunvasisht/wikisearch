import streamlit as st

st.title("My Wiki Search")
if search_keyword := st.text_input("Search Keyword(s)"):
    st.write("searching...")