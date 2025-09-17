
import pathlib as pl

import folium


def save(map: folium.Map) -> str:
    path = pl.Path("map.html").resolve()
    map.save(str(path))
    return f'file://{str(path)}'


# sample and/or test code below #################################################################################
if __name__ == '__main__':  # ###################################################################################

    the_map = folium.Map(location=(51.532, -0.1887), zoom_start=8, control_scale=True,)
    print(save(the_map))
