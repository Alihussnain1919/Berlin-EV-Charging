import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from core.services.search_service import get_stations_by_postal_code
from core.services.feedback_service import get_feedback_for_station, insert_feedback
import streamlit as st
import folium
from streamlit_folium import st_folium


# --- Helper Functions ---
def render_map(stations):
    """
    Renders a Folium map with markers for charging stations.
    """
    # Create a Folium map centered around the average latitude/longitude
    map_center = [stations[0].latitude, stations[0].longitude]
    m = folium.Map(location=map_center, zoom_start=13)

    for station in stations:
        popup_html = f"""
        <div style="font-size: 14px;">
            <b>Operator:</b> {station.operator}<br>
            <b>Address:</b> {station.get_full_address()}<br>
            <a href="https://www.google.com/maps/search/?api=1&query={station.latitude},{station.longitude}" target="_blank">Open in Google Maps</a>
        </div>
        """
        folium.Marker(
            location=[station.latitude, station.longitude],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"{station.operator} ({station.get_full_address()})",
            icon=folium.Icon(icon="map-marker", color="red")
        ).add_to(m)

    return m


def display_feedback(selected_station_id):
    """
    Fetches and displays feedback for the selected charging station.
    """
    feedback = get_feedback_for_station(selected_station_id)

    if not feedback:
        st.write("No feedback available for this station.")
    else:
        for item in feedback:
            st.write(f"**Rating:** {item.rating} ⭐")
            st.write(f"**Comments:** {item.comments}")
            st.write(f"**Date:** {item.timestamp}")
            st.markdown("---")


def provide_feedback(selected_station_id):
    """
    Allows the user to provide feedback for the selected station.
    """
    st.subheader("Provide Your Feedback")
    user_id = st.session_state.get("user_id", 1)  # Replace with logged-in user ID logic
    rating = st.slider("Rating", 1, 5, 3)
    comments = st.text_area("Comments", placeholder="Enter your feedback...")
    submit_feedback = st.button("Submit Feedback")

    if submit_feedback:
        insert_feedback(selected_station_id, user_id, rating, comments)
        st.success("Thank you for your feedback!")


# --- Streamlit App ---
st.title("Charging Stations Finder 🚗⚡")

# Input for postal code
postal_code = st.text_input("Enter Postal Code to Find Charging Stations:")

if postal_code:
    # Fetch charging stations by postal code
    stations = get_stations_by_postal_code(postal_code)

    if stations:  # Check if any stations were found
        st.markdown(f"### Total Charging Stations Found: **{len(stations)}**")

        # Render the map
        map_object = render_map(stations)
        st.subheader("Charging Stations Map")
        st_folium(map_object, width=700, height=500)

        # Sidebar for selecting a charging station
        st.sidebar.header("Available Charging Stations")
        station_options = {
            station.station_id: f"{station.operator} ({station.get_full_address()})"
            for station in stations
        }
        selected_station_id = st.sidebar.selectbox(
            "Select a Charging Station",
            options=station_options.keys(),
            format_func=lambda x: station_options[x]
        )

        # Display feedback for the selected station
        st.subheader(f"Feedback for {station_options[selected_station_id]}")
        display_feedback(selected_station_id)

        # Allow the user to provide feedback
        provide_feedback(selected_station_id)

    else:
        st.write("No charging stations found for the entered postal code.")
