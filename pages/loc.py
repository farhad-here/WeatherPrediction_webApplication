import streamlit as st
from geopy.geocoders import Nominatim

st.title('📍LatLong')

def get_city_coordinates(city_name):
    # Initialize the Nominatim API
    geolocator = Nominatim(user_agent="geoapilolat")

    # Geocode the city
    location = geolocator.geocode(city_name)

    if location:
        st.write(f"City: {location.address}")
        st.write(f"Latitude: {location.latitude}")
        st.write(f"Longitude: {location.longitude}")
    else:
        st.write("City not found")

# Example usage
city = st.text_input("Enter the city name: ")
if city:
    get_city_coordinates(city)
