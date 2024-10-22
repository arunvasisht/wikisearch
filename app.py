import streamlit as st
import requests
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

SEARCH_API_KEY = os.environ["SEARCH_API_KEY"]
AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
SEARCH_ENGINE_ID = os.environ["SEARCH_ENGINE_ID"]

# API endpoint
url = 'https://www.googleapis.com/customsearch/v1'

st.title("My Wiki Search")
if search_keywords := st.text_input("Search Keyword(s)"):

    # Parameters
    params = {
        'key': SEARCH_API_KEY,
        'cx': SEARCH_ENGINE_ID,
        'q': search_keywords,
    }
    with st.spinner("Searching..."):
        # Send the request
        response = requests.get(url, params=params)
    
    response_code = response.status_code
    if response_code == 200:
        st.success('Search successful!', icon="✅")
        items = response.json()["items"]
        links = [i["link"] for i in items]
        titles = [i["title"] for i in items]
        selections = [False for i in items]

        

        data_df = pd.DataFrame(
            {
                "selected":selections,
                "Title": titles,
                "urls": links,
            }
        )

        edited_data = st.data_editor(
            data_df,
            column_config={
                "selected": st.column_config.CheckboxColumn("",default=False,),
                "urls": st.column_config.LinkColumn(
                    "URL", display_text="Open Link"
                ),
                
            },
            disabled=["widgets"],
            hide_index=True,
        )

        if st.button("Download",help="To scrape selected websites"):
            st.write(len(edited_data[edited_data["selected"] == True]))
    else:
        st.error('Error!', icon="🚨")

    