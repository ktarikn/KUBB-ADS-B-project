import folium
m = folium.Map(location=[41, -71], zoom_start=4)

kw = {"prefix": "fa", "color": "green", "icon": "plane"}

angle = 180
icon = folium.Icon(angle=angle, **kw)
folium.Marker(location=[41, -72], icon=icon, tooltip="Plane going to 'Merica").add_to(m)

angle = 45
icon = folium.Icon(angle=angle, **kw)
folium.Marker(location=[41, -75], icon=icon, tooltip=str(angle)).add_to(m)

angle = 90
icon = folium.Icon(angle=angle, **kw)
folium.Marker([41, -78], icon=icon, tooltip=str(angle)).add_to(m)

initialPlanes = [] # store all plane's starting location.

currentPlanes = [] # planes that are on the move





m.save("mapimiz.html")
