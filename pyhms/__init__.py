__all__ = ['get_hms']
__version__ = '0.1.0'
__doc__ = """
"""


def plot_smoke(hmsf, ax=None, statepath='cb_2022_us_state_500k.zip'):
    """
    Arguments
    ---------
    hmsf : geopandas.GeoDataFrame
        data from HMS product
    ax : matplotlib.axes.Axes
        Axes to plot on. If None is given, one will be created.
    statepath : str
        Path to state boundaries for plotting. If None, states will not be added.
        If provided and not present, the US Census 2022 500k will be downloaded.

    Returns
    -------
    ax : matplotlib.axes.Axes
        Axes with plot
    """
    import matplotlib.colors as mc
    import matplotlib.pyplot as plt
    import requests
    from os.path import exists
    # ideally, you download this once and then change the path to the downloaded copy.
    
    cmap, norm = mc.from_levels_and_colors([0.5, 1.5, 2.5, 3.5], ['green', 'yellow', 'red'])
    hmsf['DensityNum'] = hmsf['Density'].replace({'Light': 1, 'Medium': 2, 'Heavy': 3})

    ax = hmsf.plot('DensityNum', cmap=cmap, norm=norm, alpha=0.75, ax=ax)
    figure = ax.figure
    cb = fig.colorbar(ax.collections[0], ticks=[1, 2, 3])
    cb.ax.set_yticklabels(['Light', 'Medium', 'Heavy'], rotation=90, verticalalignment='center')
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    plotstates = statepath is not None
    if plotstates:
        if not exists(statepath):
            r = requests.get('https://www2.census.gov/geo/tiger/GENZ2022/shp/cb_2022_us_state_500k.zip')
            r.raise_for_status()
            with open(statepath, 'wb') as outf:
                outf.write(r.content)

        stf = gpd.read_file(statepath)
        stf.plot(facecolor='none', edgecolor='grey', ax=ax)

    ax.set(xlim=xlim, ylim=ylim)
    return ax


class hmsapi():
    def __init__(self, root='https://satepsanone.nesdis.noaa.gov/pub/FIRE/web/HMS', cache='.')
        """
        Arguments
        ---------
        Returns
        -------
        None
        """
        self._root = root
        self._cache = cache

    def open(self, date, prod='smoke'):
        """
        Arguments
        ---------
        date : pandas.Datetime
            A date or dates to process.
        prod : str
            smoke, fire

        Returns
        -------
        hmsf : geopands.GeoDataFrame
            File opened from local download.
        """
        import geopandas as gpd
        import pandas as pd

        localpaths = self.download(date, prod=prod)
        hmsfs = []
        for localpath in localpaths:
            hmsf = gpd.read_file(localpath)
            hmsfs.append(hmsf)
        hmsf = pd.concat(hmsfs)
        return hmsf

    def download(self, date, prod='smoke'):
        """
        Arguments
        ---------
        date : pandas.Datetime
            A date or dates to process.
        prod : str
            smoke, fire

        Returns
        -------
        outpaths : list
            List of outpaths
        """
        from collections.abc import Iterable
        import requests
        from os.path import dirname
        import os
        cache = self._cache

        if not isinstance(date, Iterable):
            date = [date]

        outpaths = []
        for dt in date:
            if exists(dest):
                outpaths.append(dest)
                continue
            destdir = dirname(dest)
            os.makedirs(destdir, exist_ok=True)
            r = requests.get(url)
            r.raise_for_status()
            with open(dest, 'wb') as outf:
                outf.write(r.content)
            outpaths.append(dest)

        return outpaths

    def get_local(date, prod='smoke'):
        """
        Arguments
        ---------
        date : pandas.Datetime
            A date to process.
        prod : str
            smoke, fire

        Returns
        -------
        localpath : str
            Local file path
        """
        from os.path import basename, join, exists
        url = self.get_url(date, prod=prod)
        destdir = date.strftime(f'{self._cache}/%Y/%m')
        dest = join(destdir, basename(url))
        return dest

    def get_url(date, prod='smoke'):
        """
        Arguments
        ---------
        date : pandas.Datetime
            A date to process.
        prod : str
            smoke, fire

        Returns
        -------
        url : str
            Url to download 
        """
        root = self._root
        if prod == 'smoke':
            tmpl = f'{root}/Smoke_Polygons/Shapefile/%Y/%m/hms_smoke%Y%m%d.zip'
        elif prod == 'fire'
            tmpl = f'{root}/Fire_Points/Shapefile/%Y/%m/hms_fire%Y%m%d.zip'
    
        return date.strftime(tmpl)
