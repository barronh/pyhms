def test_url():
    from .. import hmsapi
    hms = hmsapi()
    url = hms.get_url('2023-06-14')
    chkurl = 'https://satepsanone.nesdis.noaa.gov/pub/FIRE/web/HMS'
    chkurl += '/Smoke_Polygons/Shapefile/2023/06/hms_smoke20230614.zip'
    assert url == chkurl


def test_local():
    from .. import hmsapi
    hms = hmsapi()
    url = hms.get_local('2023-06-14')
    chkurl = './2023/06/hms_smoke20230614.zip'
    assert url == chkurl


def test_download():
    import tempfile
    from .. import hmsapi
    with tempfile.TemporaryDirectory() as td:
        hms = hmsapi(cache=td)
        outpaths = hms.download('2023-06-14')
    assert len(outpaths) == 1


def test_open():
    import tempfile
    from .. import hmsapi
    with tempfile.TemporaryDirectory() as td:
        hms = hmsapi(cache=td)
        hmsf = hms.open('2023-06-14')
    assert 'Density' in hmsf.columns


def test_plot_smoke():
    import tempfile
    from .. import hmsapi, plot_smoke
    with tempfile.TemporaryDirectory() as td:
        hms = hmsapi(cache=td)
        hmsf = hms.open('2023-06-14')
        ax = plot_smoke(hmsf, statepath=f'{td}/states.zip')
    assert len(ax.collections) == 2
