import folium
m = folium.Map((0, 0), zoom_start=7)

group_1 = folium.FeatureGroup("first group").add_to(m)
folium.Marker((0, 0), icon=folium.Icon("red")).add_to(group_1)
folium.Marker((1, 0), icon=folium.Icon("red")).add_to(group_1)

group_2 = folium.FeatureGroup("second group").add_to(m)
folium.Marker((0, 1), icon=folium.Icon("green")).add_to(group_2)

folium.LayerControl().add_to(m)
m.save("index.html")