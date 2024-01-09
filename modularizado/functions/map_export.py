import folium

def create_map(list):
    mapa = folium.Map(location=[-5.812757, -35.255127], zoom_start=6)  

    for pin in list:
        folium.Marker([pin['lat'], pin['long']], popup=pin['name']).add_to(mapa) 

    return mapa