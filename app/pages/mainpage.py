#mainpage for the project interface

import streamlit as st
from queries import get_stations_by_postal_code

st.title("Map View")

postal_code = st.text_input("Search by Postal Code:")
if postal_code:
    results = get_stations_by_postal_code(postal_code)
    st.map(results)
