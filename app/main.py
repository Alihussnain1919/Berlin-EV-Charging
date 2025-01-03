# Main Streamlit app entry point - run file

import streamlit as st
from queries import get_stations_by_postal_code, get_feedback_for_station, insert_feedback
import pandas as pd
st.title("Charging Stations Finder 🚗⚡")

# Input for postal code
postal_code = st.text_input("Enter Postal Code to Find Charging Stations:")

# Show charging stations on the map
if postal_code:
    # Fetch charging stations for the postal code
    stations = get_stations_by_postal_code(postal_code)

    # Debugging: Check raw data
    st.write("Raw Data Preview:")
    st.write(stations)

    # Ensure latitude and longitude are numeric
    stations['latitude'] = pd.to_numeric(stations['latitude'], errors='coerce')
    stations['longitude'] = pd.to_numeric(stations['longitude'], errors='coerce')

    # Remove rows with invalid lat/lon values
    stations = stations.dropna(subset=['latitude', 'longitude'])

    # Debugging: Check cleaned data
    st.write("Cleaned Data Types:")
    st.write(stations.dtypes)
    st.write("Cleaned Data Preview:")
    st.write(stations)

    # Plot on the map
    if not stations.empty:
        st.map(stations[['latitude', 'longitude']])
    else:
        st.write("No valid charging stations found for this postal code.")

# Select a charging station to view feedback or add feedback
st.sidebar.header("Feedback Section")
station_id = st.sidebar.text_input("Enter Station ID to View/Add Feedback:")

if station_id:
    # View feedback
    st.subheader(f"Feedback for Station ID: {station_id}")
    feedback = get_feedback_for_station(station_id)
    if feedback.empty:
        st.write("No feedback available for this station.")
    else:
        st.write(feedback)

    # Add feedback
    st.sidebar.subheader("Add Feedback")
    user_id = st.sidebar.text_input("User ID:")
    rating = st.sidebar.slider("Rating (1-5):", 1, 5)
    comments = st.sidebar.text_area("Comments:")

    if st.sidebar.button("Submit Feedback"):
        if user_id and comments:
            insert_feedback(station_id, user_id, rating, comments)
            st.sidebar.success("Feedback submitted successfully!")
        else:
            st.sidebar.error("Please fill in all fields to submit feedback.")

