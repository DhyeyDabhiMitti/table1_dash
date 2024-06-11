import streamlit as st
import folium
from streamlit_folium import st_folium,folium_static
import pandas as pd

@st.cache_resource
def load_data():
    df1 = pd.read_csv('edited_Table1.csv',index_col=0)
    coords = [{'x':row['x'],'y':row['y']} for index,row in df1.iterrows()]
    return coords,df1

st.title("Soil Properties with Marked Coordinates for Orissa")

@st.cache_resource
def main():

    # Define coordinates
    coordinates,df1 = load_data()

    # Create a Folium map centered around the first location
    cent_X = 0
    cent_Y = 0
    for coords in coordinates:
        cent_X+=coords['x']
        cent_Y+=coords['y']
    cent_X = cent_X/len(coordinates)
    cent_Y = cent_Y/len(coordinates)
    map_center = (cent_X, cent_Y)
    m = folium.Map(location=map_center, zoom_start=5)

    # Add district layer
    indian_district_polygon = (
        "https://github.com/geohacker/india/blob/c3df722d136666b6b663f9359336ae1543809a48/district/india_district.geojson"
    )
    folium.GeoJson(indian_district_polygon).add_to(m)

    # Add markers to the map
    for coord in coordinates:
        html = pd.DataFrame(df1[df1['x']==coord['x']][df1['y']==coord['y']].iloc[:,0:9]).to_html(
                classes="table table-striped table-hover table-condensed table-responsive"
            )
        popup = folium.Popup(html, max_width=500)
        folium.Marker(
            location=(coord["x"], coord["y"]),
            tooltip = str(coord['x']) + ' , ' + str(coord['y']),
            popup = popup
        ).add_to(m)

    # Display the map in Streamlit
    return m

load_data()
if 'map' not in st.session_state:
    map = main()
    st.session_state['map'] = map
folium_static(st.session_state['map'], width=800, height=500)
