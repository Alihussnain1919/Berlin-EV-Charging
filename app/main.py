import streamlit as st
from queries import get_stations_by_postal_code, get_feedback_for_station, insert_feedback
import pandas as pd
import folium
from streamlit_folium import st_folium
import sqlite3
st.title("Charging Stations Finder 🚗⚡")

# Input for postal code
postal_code = st.text_input("Enter Postal Code to Find Charging Stations:")

# Show charging stations on the map
if postal_code:
    # Fetch charging stations for the postal code
    stations = get_stations_by_postal_code(postal_code)

    if not stations.empty:
        total_stations = len(stations)

        # Display the total number of stations
        st.markdown(
            f"### Total Charging Stations Found: **{total_stations}**"
        )

        # Ensure latitude and longitude are numeric
        stations['latitude'] = pd.to_numeric(stations['latitude'], errors='coerce')
        stations['longitude'] = pd.to_numeric(stations['longitude'], errors='coerce')

        # Remove rows with invalid lat/lon values
        stations = stations.dropna(subset=['latitude', 'longitude'])

        # Add Google Maps link
        stations["google_maps_url"] = stations.apply(
            lambda row: f"https://www.google.com/maps/search/?api=1&query={row['latitude']},{row['longitude']}",
            axis=1
        )
        # Plot on the map using Folium
        if not stations.empty:
            # Create a Folium map
            m = folium.Map(
                location=[stations["latitude"].mean(), stations["longitude"].mean()],
                zoom_start=15
            )

            # Add markers for each station
            for _, row in stations.iterrows():
                # Popup with clickable link
                popup_html = f"""
                <div style="font-size: 14px;">
                    <b>Operator:</b> {row['operator']}<br>
                    <b>Address:</b> {row['street']} {row['house_number']}, {row['city']}<br>
                    <b>State:</b> {row['state']}<br>
                    <a href="{row['google_maps_url']}" target="_blank">Open in Google Maps</a>
                </div>
                """
                folium.Marker(
                    location=[row['latitude'], row['longitude']],
                    popup=folium.Popup(popup_html, max_width=300),
                    tooltip=f"{row['operator']} ({row['street']} {row['house_number']})"
                ).add_to(m)

            # Render the Folium map
            st.subheader("Charging Stations Map")
            st_folium(m, width=700, height=500)
            
            #------------start
            # Sidebar for listing charging stations and selecting one
            st.sidebar.header("Available Charging Stations")
    
            # Create a dictionary of station_id and operator name + address for display
            station_options = {
                row['station_id']: f"{row['operator']} ({row['street']} {row['house_number']}, {row['city']})"
                for _, row in stations.iterrows()
            }
    
            # Sidebar select box to choose a station
            selected_station_id = st.sidebar.selectbox(
                "Select a Charging Station", 
                options=station_options.keys(), 
                format_func=lambda x: station_options[x]
            )
    
            # Display feedback for the selected station
            st.subheader(f"Feedback for {station_options[selected_station_id]}")
            feedback = get_feedback_for_station(selected_station_id)
    
            if not feedback.empty:
                for _, row in feedback.iterrows():
                    st.write(f"**Rating:** {row['rating']} ⭐")
                    st.write(f"**Comments:** {row['comments']}")
                    st.write(f"**Timestamp:** {row['timestamp']}")
                    st.markdown("---")
            else:
                st.write("No feedback available for this station.")
    
            # Allow user to provide feedback for the selected station
            st.subheader("Provide Your Feedback")
            user_id = st.session_state.get("user_id", 1)  # Replace with logged-in user ID logic
            rating = st.slider("Rating", 1, 5, 3)
            comments = st.text_area("Comments", placeholder="Enter your feedback...")
            submit_feedback = st.button("Submit Feedback")
    
            if submit_feedback:
                conn = sqlite3.connect('charging_stations.db')
                query = """
                INSERT INTO Feedback (station_id, user_id, rating, comments, timestamp)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP);
                """
                conn.execute(query, (selected_station_id, user_id, rating, comments))
                conn.commit()
                st.success("Thank you for your feedback!")
        #------------stop
        else:
            st.write("No valid charging stations found for this postal code.")
        
    else:
        st.write("No charging stations found for the entered postal code.")






 #   if st.sidebar.button("Submit Feedback"):
 #       if user_id and comments:
 #           insert_feedback(station_id, user_id, rating, comments)
 #           st.sidebar.success("Feedback submitted successfully!")
 #       else:
 #           st.sidebar.error("Please fill in all fields to submit feedback.")
