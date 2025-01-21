""" Some quick readers for specific tasks, we dont have to keep"""
from io_utils.data.read.geo_ts_readers import GeoCCISMv6Ts
import pandas as pd

class GapfilledWithStatsReader:
    def __init__(self, path1, path2):
        self.reader1 = GeoCCISMv6Ts(path1, ioclass_kws={'read_bulk': True})
        self.reader2 = GeoCCISMv6Ts(path2, ioclass_kws={'read_bulk': True})

        self.grid = self.reader1.grid

    def read(self, *args, **kwargs):
        ts1 = self.reader1.read(*args, **kwargs)
        ts2 = self.reader2.read(*args, **kwargs)
        return pd.concat([ts1, ts2], axis=1)

if __name__ == '__main__':
    paths = [
        '/home/wpreimes/shares/climers/Projects/CCIplus_Soil_Moisture/07_data/ESA_CCI_SM_v09.1_GAPFILLED/COMBINED/gapfill_abs/08_gapfilled_timeseries',
        '/home/wpreimes/shares/climers/Projects/CCIplus_Soil_Moisture/07_data/ESA_CCI_SM_v09.1_GAPFILLED/COMBINED/02_gapstats_gapmasks/cciv9Final/CCIv9Final_1991_2023/ts_gapstats_CCIv91Final'
    ]
    reader = GapfilledWithStatsReader(*paths)
    ts = reader.read(-73.125, -40.875)
    ts = ts[(ts['euclidean_distance'] >= 2)]

    print(ts)