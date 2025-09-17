
import functools

import pandas as pd


def row2html(
        row: pd.Series,
        drop: list[str] | None = None,
        add_styles: list[functools.partial] | None = None      # use methods of pandas.io.formats.style.Style
) -> str:
    # modification ################################################################################
    part_of_row = row.drop(drop, errors='ignore') if drop else row

    # general #####################################################################################
    style = part_of_row.to_frame().style

    style.set_table_attributes(
        'border="1" class="table table-striped table-hover table-condensed table-responsive"'
    )
    style.set_table_styles([
        {'selector': 'td', 'props': 'text-align: right;'},
        {'selector': 'th', 'props': 'text-align: right;'},
    ])

    # style.format(hyperlinks='html')

    # specific ####################################################################################
    if add_styles:
        [to_apply_style(style) for to_apply_style in add_styles]

    return style.to_html()


# sample and/or test code below #################################################################################
if __name__ == '__main__':  # ###################################################################################

    import pathlib as pl

    import folium
    import pandas.io.formats.style

    the_row = pd.Series({
        'url': 'https://www.wikipedia.org',
        'dtime': '2025-Jan-21',
        'price': 925,
        'z_score_price': -3.7220047562221863,
        'sq_m': 9.3,
        'z_score_ppm': 2.2761118417629063,
        'epc': '-',
        'tax': '-',
        'lat': 51.48361,
        'lon': -0.11484,
    })

    the_point = (51.48361, -0.11484)    # lat, lon
    the_map = folium.Map(the_point, zoom_start=16, control_scale=True)

    styles_for_popup = [
        functools.partial(
            pandas.io.formats.style.Styler.format,
            subset=pd.IndexSlice[['sq_m', 'z_score_price', 'z_score_ppm'], :],
            precision=1
        ),
        functools.partial(
            pandas.io.formats.style.Styler.bar,
            subset=pd.IndexSlice[['z_score_price', 'z_score_ppm'], :],
            align=0, vmin=-3, vmax=3, color=['green', 'red'], height=50
        ),
    ]

    folium.Marker(
        location=the_point,
        popup=row2html(
            row=the_row,
            add_styles=styles_for_popup,
        ),
        tooltip=row2html(
            row=the_row,
            drop=['lat', 'lon', 'url', 'z_score_price', 'z_score_ppm', 'epc', 'tax'],
            add_styles=[functools.partial(pandas.io.formats.style.Styler.format, precision=1)],
        )
    ).add_to(the_map)

    the_path = pl.Path(__file__).with_suffix('.html')
    the_map.save(str(the_path))
    print(f'file://{str(the_path)}')
