coordinate = (0, 0)
        m = folium.Map(
        	
        	zoom_start=8,
        	location=coordinate
        )
        group_1 = folium.FeatureGroup("first group").add_to(m)
        folium.Marker((0, 0), icon=folium.Icon("red") ,popup="Flight no XYZ Altitude:32794, Latitude:412387").add_to(group_1)
        folium.Marker((1, 0), icon=folium.Icon("red")).add_to(group_1)
        # save map data to data object
        data = io.BytesIO()
        m.save(data, close_file=False)

        self.webView = QWebEngineView()
        self.webView.setHtml(data.getvalue().decode())
        layout.addWidget(self.webView)