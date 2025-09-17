
import dataclasses as dc

import geohash


@dc.dataclass(slots=True)
class SameGeoPntResolver:
    shift:      float = 0.0005
    precision:  int = 9

    _seen:      set = dc.field(init=False, default_factory=set)

    def get_coordinate_for(self, lat: float, lon: float) -> tuple[float, float]:

        while (tmp := geohash.encode(lat, lon, precision=self.precision)) in self._seen:
            lat += self.shift
        self._seen.add(tmp)

        return lat, lon


# sample and/or test code below #################################################################################
if __name__ == '__main__':  # ###################################################################################

    import folium
    import pandas as pd

    import pathlib as pl

    df_test = pd.DataFrame([
        {
            'url': 'https://www.wikipedia.org',
            'dtime': '2025-Jan-21',
            'price': 1925,
            'lat': 51.48361,
            'lon': -0.11484,
        },
        {
            'url': 'https://www.wikipedia.org',
            'dtime': '2025-Feb-02',
            'price': 925,
            'lat': 51.48361,
            'lon': -0.11484,
        }
    ])

    the_point = (51.48361, -0.11484)    # lat, lon
    the_map = folium.Map(the_point, zoom_start=16, control_scale=True)

    same_geopnt_resolving = SameGeoPntResolver()

    for idx in range(df_test.shape[0]):
        row: pd.Series = df_test.iloc[idx]

        pnt_lat, pnt_lon = same_geopnt_resolving.get_coordinate_for(row['lat'], row['lon'])

        folium.Marker(
            location=(pnt_lat, pnt_lon),
            tooltip=row.to_frame().style.format(precision=1, hyperlinks='html').to_html(),
        ).add_to(the_map)

    the_path = pl.Path(__file__).with_suffix('.html')
    the_map.save(str(the_path))
    print(f'file://{str(the_path)}')