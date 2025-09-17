
import dataclasses as dc
import functools

import folium.plugins
import pandas as pd

import df2map.part_s.p00_save as p00
import df2map.part_s.p01_tiles as p01
import df2map.part_s.p02_row_to_html as p02
import df2map.part_s.p03_groups_logic as p03
import df2map.part_s.p04_same_geopnt_resolver as p04


@dc.dataclass(slots=True)
class StartPoint:
    lat:        float = 51.532          # London
    lon:        float = -0.1887
    zoom:       int = 12


@dc.dataclass(slots=True)
class Columns4Map:
    latitude:       str = 'lat'
    longitude:      str = 'lon'
    color:          str = 'color'
    group:          str = 'group'
    group_order:    str = 'group_order'

    def __iter__(self):
        for val in dc.asdict(self).values():
            yield val


@dc.dataclass(slots=True)
class Df2Map:
    df:                     pd.DataFrame
    tile_list:              list[folium.raster_layers.TileLayer] | None = None

    start_pnt:              StartPoint = dc.field(default_factory=StartPoint)
    map_col:                Columns4Map = dc.field(default_factory=Columns4Map)
    same_pnt_resolver:      p04.SameGeoPntResolver | None = None

    default_group:          str = 'df'
    show_groups:            bool = True

    drop_map_col:           bool = True
    popup_drop:             list[str] | None = None
    tip_drop:               list[str] | None = None

    popup_styles:  list[functools.partial] | None = None       # use pandas.io.formats.style.Style methods
    tip_styles:    list[functools.partial] | None = None       # use pandas.io.formats.style.Style methods

    _map:       folium.Map = dc.field(init=False)

    # TODO required columns exception

    def __post_init__(self):
        self._map = folium.Map(
            location=(self.start_pnt.lat, self.start_pnt.lon),
            zoom_start=self.start_pnt.zoom,
            control_scale=True,
            tiles=None if self.tile_list else folium.raster_layers.TileLayer(),
        )

        if self.tile_list:
            [tile.add_to(self._map) for tile in self.tile_list]

        group_s = dict()                    # [group_key: folium.FeatureGroup]
        for a_group in p03.groups_name_inorder(self.df, self.map_col.group, self.map_col.group_order, self.default_group):
            group_s[a_group] = folium.FeatureGroup(name=a_group, show=self.show_groups)
            group_s[a_group].add_to(self._map)

        if self.drop_map_col:
            self.popup_drop = [*self.popup_drop, *self.map_col] if self.popup_drop else list(self.map_col)
            self.tip_drop = [*self.tip_drop, *self.map_col] if self.tip_drop else list(self.map_col)

        for idx in range(self.df.shape[0]):
            row: pd.Series = self.df.iloc[idx]
            g_folium = group_s[row.get(self.map_col.group, self.default_group)]

            pnt_lat, pnt_lon = row[self.map_col.latitude], row[self.map_col.longitude]
            if self.same_pnt_resolver is not None:
                pnt_lat, pnt_lon = self.same_pnt_resolver.get_coordinate_for(pnt_lat, pnt_lon)

            folium.CircleMarker(            # https://leafletjs.com/reference.html#circlemarker-option
                location=(pnt_lat, pnt_lon),
                fill=True,
                radius=1.5,
                fill_opacity=1.2,
                color=row.get(self.map_col.color, 'magenta'),
                popup=p02.row2html(row, self.popup_drop, self.popup_styles),
                tooltip=p02.row2html(row, self.tip_drop, self.tip_styles),
            ).add_to(g_folium)

        folium.LayerControl().add_to(self._map)
        folium.plugins.MousePosition().add_to(self._map)

    def save(self):
        return p00.save(self._map)


# sample and/or test code below #################################################################################
if __name__ == '__main__':  # ###################################################################################

    import functools

    import pandas as pd
    import numpy as np
    import pandas.io.formats.style

    import df2map

    the_df: pd.DataFrame = pd.read_csv('input/df.csv').drop(columns=['link_part'])
    the_df.index = np.arange(1, len(the_df) + 1)

    the_df['first_dt'] = the_df['first_dt'].str.split(' ').str[0]
    the_df['last_dt'] = the_df['last_dt'].str.split(' ').str[0]

    month_s = ('jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec')

    label2clr = {
        'top_100':  'grey',
        'top_050':   'magenta',
        'top_010':  'cyan',
        'top_003':  'yellow',
    }

    the_df['group'] = pd.cut(
        x=the_df['ascents'],
        bins=[0, 1550, 2500, 4080, 9999],
        labels=label2clr.keys()
    )
    the_df['color'] = the_df['group'].map(label2clr)

    popup_n_tip_styles = [
        functools.partial(
            pandas.io.formats.style.Styler.format,
            precision=1,
        ),
        functools.partial(
            pandas.io.formats.style.Styler.bar,
            subset=pd.IndexSlice[['ascents_per_day'], :],
            height=75,
            color='magenta',
            vmax=15.1,
        ),
    ]

    popup_styles = [
        *popup_n_tip_styles,

        functools.partial(
            pandas.io.formats.style.Styler.bar,
            color='lightgreen',
            vmin=1.,
            vmax=100.,
            subset=pd.IndexSlice[[*month_s], :],
            height=75,
        ),
    ]

    path2map = df2map.Df2Map(
        df=the_df,
        tile_list=[df2map.CartoTile.dark(), df2map.CartoTile.light()],

        start_pnt=df2map.StartPoint(lat=46.58, lon=9.0, zoom=4),
        map_col=df2map.Columns4Map(),
        same_pnt_resolver=df2map.SameGeoPntResolver(shift=0.0001),

        drop_map_col=True,
        tip_drop=[*month_s, 'last_dt', 'first_dt'],
        popup_drop=[],

        tip_styles=popup_n_tip_styles,
        popup_styles=popup_styles,
    ).save()

    print(path2map)
