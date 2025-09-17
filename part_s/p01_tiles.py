
import folium


class CartoTile:

    @classmethod
    def light(cls) -> folium.raster_layers.TileLayer:
        return folium.raster_layers.TileLayer(     # /dark_all/ OR
            tiles='https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png',   # /light_nolabels/
            name='light',
            attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> '
                 'contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
        )

    @classmethod
    def dark(cls) -> folium.raster_layers.TileLayer:
        return folium.raster_layers.TileLayer(  # /dark_all/ OR
            tiles='https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png',  # /dark_nolabels/
            name='dark',
            attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> '
                 'contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
        )
