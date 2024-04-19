__all__ = ['hmsapi', 'plot_smoke']
__version__ = '0.1.0'
__doc__ = """
Overview
========
pyhms helps to download and create plots of NOAA's HMS products in python.
"""
from importlib.metadata import version, PackageNotFoundError


try:
    __version__ = version('pyhms')
except PackageNotFoundError:
    __version__ = '0.0.0'

_stateroot = 'https://www2.census.gov/geo/tiger/GENZ2022/shp'
_stateurl = f'{_stateroot}/cb_2022_us_state_500k.zip'


def plot_smoke(hmsf, ax=None, statepath='cb_2022_us_state_500k.zip', **kwds):
    """
    Arguments
    ---------
    hmsf : geopandas.GeoDataFrame or str
        If dataframe, should be data from HMS product.
        If str, should be a path to a HMS file.
    ax : matplotlib.axes.Axes
        Axes to plot on. If None is given, one will be created.
    statepath : str
        Path to state boundaries for plotting. If None, states will not be
        added. If provided and not on disk, US Census 2022 states 500k will
        be downloaded.
    kwds : mappable
        Additional kwds will be passed to hmsf.plot and affect polygons.

    Returns
    -------
    ax : matplotlib.axes.Axes
        Axes with plot

    Example
    -------

    .. code-block::python

        import pyhms
        hms = pyhms.hmsapi()
        hmsf = hms.open('2023-06-14')
        ax = pyhms.plot_smoke(hmsf)
        ax.figure.savefig('hms_smoke.png')
    """
    import geopandas as gpd
    import matplotlib.colors as mc
    import requests
    from os.path import exists

    levels = [0.5, 1.5, 2.5, 3.5]
    colors = ['green', 'yellow', 'red']
    cmap, norm = mc.from_levels_and_colors(levels, colors)
    cats = {'Light': 1, 'Medium': 2, 'Heavy': 3}
    if isinstance(hmsf, str):
        hmsf = gpd.read_file(hmsf)

    DensityNum = hmsf['Density'].apply(cats.get)
    ax = hmsf.plot(DensityNum, cmap=cmap, norm=norm, ax=ax, **kwds)
    fig = ax.figure
    cb = fig.colorbar(ax.collections[0], ticks=[1, 2, 3])
    cb.ax.set_yticklabels(
        ['Light', 'Medium', 'Heavy'], rotation=90, verticalalignment='center'
    )
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    plotstates = statepath is not None
    if plotstates:
        if not exists(statepath):
            r = requests.get(_stateurl)
            r.raise_for_status()
            with open(statepath, 'wb') as outf:
                outf.write(r.content)

        stf = gpd.read_file(statepath)
        stf.plot(facecolor='none', edgecolor='grey', ax=ax)

    ax.set(xlim=xlim, ylim=ylim)
    return ax


class hmsapi():
    def __init__(self, root=None, cache='.'):
        """
        Arguments
        ---------
        root : str
            Optional, specify the url where NOAA hosts HMS files.
            Default https://satepsanone.nesdis.noaa.gov/pub/FIRE/web/HMS
        cache : str
            Place to cache HMS files.

        Returns
        -------
        None
        """
        if root is None:
            root = 'https://satepsanone.nesdis.noaa.gov/pub/FIRE/web/HMS'

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

        Example
        -------

        .. code-block::python

            import pyhms
            hms = pyhms.hmsapi()
            hmsf = hms.open('2023-06-14')
            print(hmsf.shape)
            # (69, 5)
            print(hmsf.columns)
            # Index(['Satellite', 'Start', 'End', 'Density', 'geometry'],
            #       dtype='object')
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

        Example
        -------

        .. code-block::python

            import pyhms
            import pandas as pd
            hms = pyhms.hmsapi()
            dates = pd.date_range('2023-06-14', '2023-06-16')
            outpaths = hms.download(dates)
            print(len(outpaths), outpaths[0])
            # 3 ./2023/06/hms_smoke20230614.zip
        """
        from collections.abc import Iterable
        import requests
        from os.path import dirname, exists
        import os

        if isinstance(date, str) or not isinstance(date, Iterable):
            date = [date]

        outpaths = []
        for dt in date:
            url = self.get_url(dt, prod=prod)
            dest = self.get_local(dt, prod=prod)
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

    def get_local(self, date, prod='smoke'):
        """
        Returns the local path even if it does not exist.

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

        Example
        -------

        .. code-block::python

            import pyhms
            hms = pyhms.hmsapi()
            localpath = hms.get_local('2023-06-14')
            print(localpath)
            # ./2023/06/hms_smoke20230614.zip
        """
        from os.path import basename, join
        import pandas as pd
        date = pd.to_datetime(date)
        url = self.get_url(date, prod=prod)
        destdir = date.strftime(f'{self._cache}/%Y/%m')
        dest = join(destdir, basename(url))
        return dest

    def get_url(self, date, prod='smoke'):
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

        Example
        -------

        .. code-block::python

            import pyhms
            hms = pyhms.hmsapi()
            url = hms.get_url('2023-06-14')
            print(url)
            # https://satepsanone.nesdis.noaa.gov/pub/FIRE/web/HMS/
            #         Smoke_Polygons/Shapefile/2023/06/hms_smoke20230614.zip
        """
        import pandas as pd
        date = pd.to_datetime(date)
        root = self._root
        if prod == 'smoke':
            tmpl = f'{root}/Smoke_Polygons/Shapefile/%Y/%m/hms_smoke%Y%m%d.zip'
        elif prod == 'fire':
            tmpl = f'{root}/Fire_Points/Shapefile/%Y/%m/hms_fire%Y%m%d.zip'

        return date.strftime(tmpl)
