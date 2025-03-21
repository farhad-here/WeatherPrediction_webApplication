#Library
import requests
import streamlit as st
import pandas as pd
import pydeck as pdk
# streamlit config
st.set_page_config(
    page_title="Weather App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# weather teller function
def weather(entery):
    # site accuweather get your API
    # city
    city = entery
    # location key
    API_KEY = " 4tYKucaDrKO25mj3viVDoxfQxgr2gNz3"
    search_url = f'http://dataservice.accuweather.com/locations/v1/cities/search?apikey={API_KEY}&q={city}'
    search_response = requests.get(search_url)
    search_data = search_response.json()
    if city:
        if search_response.status_code == 200 and search_data:
            location_key = search_data[0]['Key']
            
            #Get current conditions
            weather_url = f'http://dataservice.accuweather.com/currentconditions/v1/{location_key}?apikey={API_KEY}'
            weather_response = requests.get(weather_url)
            weather_data = weather_response.json()
            
            if weather_response.status_code == 200 and weather_data:
                current = weather_data[0]
                st.dataframe({"city":f"{city}",'Temperature':f"{current['Temperature']['Metric']['Value']}°C","Condition":f"{current['WeatherText']}"},use_container_width=True)
            else:
                st.warning("Error fetching weather data.")
        else:
            st.warning("Error fetching location data.")

# weathers data information
def weathermeto_2(n):
    st.markdown('---')
    st.markdown('# 🌊Hourly Weather Variables')
    select_weath = st.selectbox('select what you want:',options=['rain','showers','snowfall','snow_depth','apparent_temperature','temperature_2m','relative_humidity_2m','dew_point_2m','pressure_msl','surface_pressure','cloud_cover','cloud_cover_low','cloud_cover_mid','cloud_cover_high,visibility','evapotranspiration','vapour_pressure_deficit','wind_speed_10m','temperature_80m','soil_temperature_0cm'])
    req =requests.get(n).json()
    lat = req["results"][0]["latitude"]
    long = req["results"][0]["longitude"]
    st.write(f"📍 coordination {city}: lat=> {lat}, lon=> {long}")
    req = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&hourly={select_weath}')
    data = req.json()
    rain = data['hourly'][f'{select_weath}']
    time_data = data['hourly']['time']
    month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    month_w = []
    day_w = []
    time_w = []
    year_w = []
    for i in time_data:
        year,month,day =  i.split('-')
        d,t = day.split('T')
        year_w.append(year)
        day_w.append(d)
        time_w.append(t)
        month_w.append(month_list[int(month)-1])
    df = pd.DataFrame({'Year':year_w,'Month':month_w,'Day':day_w,"Time":time_w,f'{select_weath}':rain})
    df['YMDT']= df['Year']+' '+df['Month']+' '+df['Day']+' '+df['Time']
    button_rain = st.button(label='SHOW Data')    
    st.markdown(f'# 🌧️{select_weath} Detail')
    if button_rain:
        st.dataframe(df)
    cbox = st.checkbox('chart?')
    if cbox:
        x_rainy = st.selectbox(label='select for X',options=df.columns)
        y_rainy = select_weath
        if x_rainy and y_rainy:
            st.title(f"🌍{select_weath}")
           

            st.markdown('#### scatterchart')
            st.scatter_chart(data=df,x=x_rainy,y=y_rainy)
            st.markdown('#### areachart')
            st.area_chart(df,x='YMDT',y=y_rainy)
            st.markdown('#### Barchart')
            st.bar_chart(data=df,x=x_rainy,y=y_rainy)
            st.markdown('#### linechart')
            st.line_chart(data=df,x=x_rainy,y=y_rainy)
            hourly_data = data["hourly"]
            df = pd.DataFrame({
                    "time": hourly_data["time"],
                    select_weath: hourly_data[select_weath]
                })
            df["time"] = pd.to_datetime(df["time"])
            df.set_index("time", inplace=True)
                
            st.line_chart(df)
                
            st.pydeck_chart(
                    pdk.Deck(
                        map_style='mapbox://styles/mapbox/light-v9',
                        initial_view_state=pdk.ViewState(latitude=lat, longitude=long, zoom=10, pitch=50),
                        layers=[
                            pdk.Layer(
                                "ScatterplotLayer",
                                data=pd.DataFrame({"lat": [lat], "lon": [long], f"{select_weath}": [df.iloc[0, 0]]}),
                                get_position='[lon, lat]',
                                get_radius=10000,
                                get_color=f'[{select_weath} * 10, 50, 150, 160]',
                                pickable=True,
                            )
                        ]
                    )
                )
def weathermeto(long,lat):
    st.markdown('---')
    st.markdown('# 🌊Hourly Weather Variables')
    select_weath = st.selectbox('select what you want:',options=['rain','showers','snowfall','snow_depth','apparent_temperature','temperature_2m','relative_humidity_2m','dew_point_2m','pressure_msl','surface_pressure','cloud_cover','cloud_cover_low','cloud_cover_mid','cloud_cover_high,visibility','evapotranspiration','vapour_pressure_deficit','wind_speed_10m','temperature_80m','soil_temperature_0cm'])
    req =requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&hourly={select_weath}')
    data = req.json()
    rain = data['hourly'][f'{select_weath}']
    time_data = data['hourly']['time']
    month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    month_w = []
    day_w = []
    time_w = []
    year_w = []
    for i in time_data:
        year,month,day =  i.split('-')
        d,t = day.split('T')
        year_w.append(year)
        day_w.append(d)
        time_w.append(t)
        month_w.append(month_list[int(month)-1])
    df = pd.DataFrame({'Year':year_w,'Month':month_w,'Day':day_w,"Time":time_w,f'{select_weath}':rain})
    df['YMDT']= df['Year']+' '+df['Month']+' '+df['Day']+' '+df['Time']
    button_rain = st.button(label='SHOW Data')    
    st.markdown(f'# 🌧️{select_weath} Detail')
    if button_rain:
        st.dataframe(df)
    cbox = st.checkbox('chart?')
    if cbox:
        x_rainy = st.selectbox(label='select for X',options=df.columns)
        y_rainy = select_weath
        if x_rainy and y_rainy:
            st.markdown('#### scatterchart')
            st.scatter_chart(data=df,x=x_rainy,y=y_rainy)
            st.markdown('#### areachart')
            st.area_chart(df,x='YMDT',y=y_rainy)
            st.markdown('#### Barchart')
            st.bar_chart(data=df,x=x_rainy,y=y_rainy)
            st.markdown('#### linechart')
            st.line_chart(data=df,x=x_rainy,y=y_rainy)

# prediction
def maximumm(long,lat):
    st.markdown('---')
    st.markdown('# 🌞The max')
    select_weath = st.selectbox('select what you want:',key='anticipate_selcetbox',options=['rain','showers','snowfall','snow_depth','apparent_temperature','temperature_2m','relative_humidity_2m','dew_point_2m','pressure_msl','surface_pressure','cloud_cover','cloud_cover_low','cloud_cover_mid','cloud_cover_high,visibility','evapotranspiration','vapour_pressure_deficit','wind_speed_10m','temperature_80m','soil_temperature_0cm'])
    req =requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&hourly={select_weath}')
    data = req.json()
    rain = data['hourly'][f'{select_weath}']
    time_data = data['hourly']['time']
    month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    month_w = []
    day_w = []
    time_w = []
    year_w = []
    for i in time_data:
        year,month,day =  i.split('-')
        d,t = day.split('T')
        year_w.append(year)
        day_w.append(int(d))
        time_w.append(int(t.split(':')[0]))
        month_w.append(month_list[int(month)-1])
    df = pd.DataFrame({'Year':year_w,'Month':month_w,'Day':day_w,"Time":time_w,f'{select_weath}':rain})
    button_rain = st.button(label='Max',key='anticipate_button')    
    if button_rain:
        maximu = df.loc[df[f'{select_weath}'] == df[f'{select_weath}'].max(),['Year','Month','Day','Time',f'{select_weath}']]
        st.dataframe(maximu)
def maximumm_2(g):
    st.markdown('---')
    st.markdown('# 🌞The max')
    select_weath = st.selectbox('select what you want:',key='anticipate_selcetbox',options=['rain','showers','snowfall','snow_depth','apparent_temperature','temperature_2m','relative_humidity_2m','dew_point_2m','pressure_msl','surface_pressure','cloud_cover','cloud_cover_low','cloud_cover_mid','cloud_cover_high,visibility','evapotranspiration','vapour_pressure_deficit','wind_speed_10m','temperature_80m','soil_temperature_0cm'])
    req =requests.get(g).json()
    lat = req["results"][0]["latitude"]
    long = req["results"][0]["longitude"]
    st.write(f"📍 coordination {city}: lat=> {lat}, lon=> {long}")
    req = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&hourly={select_weath}')
    data = req.json()
    rain = data['hourly'][f'{select_weath}']
    time_data = data['hourly']['time']
    month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    month_w = []
    day_w = []
    time_w = []
    year_w = []
    for i in time_data:
        year,month,day =  i.split('-')
        d,t = day.split('T')
        year_w.append(year)
        day_w.append(int(d))
        time_w.append(int(t.split(':')[0]))
        month_w.append(month_list[int(month)-1])
    df = pd.DataFrame({'Year':year_w,'Month':month_w,'Day':day_w,"Time":time_w,f'{select_weath}':rain})
    button_rain = st.button(label='Max',key='anticipate_button')    
    if button_rain:
        maximu = df.loc[df[f'{select_weath}'] == df[f'{select_weath}'].max(),['Year','Month','Day','Time',f'{select_weath}']]
        st.dataframe(maximu)

 

#longlat
st.markdown('# long&lat or Name')
lat = st.text_input('Latitude:')
long = st.text_input('Longitude:')
by_city_name = st.text_input("Enter the name of the city:")
#input the city
st.markdown('# 🌪️Weather')
city = st.text_input('### Name of the city:')
if city:
    weather(city)
else:
    st.error("❌404")

if long and lat:
    weathermeto(long,lat)
    
    maximumm(long,lat)


if by_city_name:
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={by_city_name}&count=1&format=json"
    weathermeto_2(geo_url)
    maximumm_2(geo_url)



