# -*- coding: utf-8 -*-

'''
Contains a plotter for variables from a netcdf file directly
Contains a combinatory plotter for e.g. creating difference plots.
'''
# TODO # (+) 

# NOTES # -

from src.io_utils.plot.plot_maps import cp_map, cp_scatter_map
import pandas as pd
import os
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
from src.io_utils.write.reg_nc_image import ReadNcImg


class NcVarPlotter(ReadNcImg):
    """
    Class to plot variables from a netcdf file.

    Parameters
    ----------
    filepath : str
        Path to a file that contains the data to plot
    time : datetime.datetime
        Time to read the variable for or None if there is only 1 time.
    resxy : tuple or None
        X and Y resolution of the netcdf image
        If None is passed we assume that the data is on an irregular grid and
        make scatter plot maps instead of regular gridded maps (as for ISMN stations).
    lat_var : str, optional (default: 'lat')
        The name of the variable in the netcdf file that refers to the latitude
        of the observation.
    lon_var : str, optional (default: 'lon')
        The name of the variable in the netcdf file that refers to the longitude
        of the observation.
    z_var : str, optional (default: 'time')
        Name of the z dimension variable name in the netcdf file.
    cell_center_origin : bool, optional (default: True)
        Set True of the loc_var refers to the center of each pixel, otherwise False.
        This has no effect if resxy is False or if loc_var is not lat/lon.
    out_dir : str, optional (default: None)
        Out path where the plots are store to, if None is passed than we use
        the parent directory of the input.
    dpi : int, optional (default: 300)
        Resolution (dots per inch) of the map (also affects rasterised parts of
        vector plots!!)
    """

    def __init__(self, filepath, resxy=(0.25, 0.25), lat_var='lat', lon_var='lon',
                 z_var='time', cell_center_origin=True, subgrid=None,
                 out_dir=None, dpi=300):

        super(NcVarPlotter, self).__init__(filepath=filepath, resxy=resxy,
                                           lat_var=lat_var, lon_var=lon_var,
                                           z_var=z_var, subgrid=subgrid,
                                           cell_center_origin=cell_center_origin)

        self.out_dir = out_dir if out_dir else self.parent_dir
        self.dpi = dpi
        self.time, self.df, self.title_template = None, None, None


    def plot_variable(self, variable, time=None, interface=True, transparent=True,
                      plotfile_name=None, file_format='png', **plot_kwargs):
        """Plot a single variable from a certain time"""
        self.read(time)

        df = self.df.copy()

        if not interface:
            plot_kwargs['show_cbar'] = False
            plot_kwargs['title'] = None

        if self.irregular:
            lons = df[self.index_name[1]].values if self.index_name[1] in df.columns \
                else df.index.get_level_values(self.index_name[1])
            lats = df[self.index_name[0]].values if self.index_name[0] in df.columns \
                else df.index.get_level_values(self.index_name[0])
            f, imax, im = cp_scatter_map(lons, lats, df[variable].values, **plot_kwargs)
        else:
            f, imax, im = cp_map(df, variable,  resxy=self.resxy, **plot_kwargs)

        if not plotfile_name:
            if self.time not in [None, datetime(1900,1,1)]:
                plotfile_name = '{var}_at_{time}_from_{file}'.format(
                    var=variable,
                    time=str(self.time.date()) if not isinstance(self.time, str) else self.time,
                    file=self.filename)
            else:
                plotfile_name = '{var}_from_{file}'.format(
                    var=variable, file=self.filename)

        if not interface:
            plt.tight_layout(pad=3)

        if not os.path.exists(self.out_dir):
            os.makedirs(self.out_dir)

        plt.savefig(os.path.join(self.out_dir, plotfile_name + '.{}'.format(file_format)),
                    dpi=self.dpi, transparent=transparent, bbox_inches='tight')
        plt.close('all')

class NcVarCombPlotter(object):
    def __init__(self, filepath1, filepath2, lat_var='lat', lon_var='lon',
                 z_var='time', cell_center_origin=True, resxy=(0.25, 0.25),
                 out_dir=None, dpi=300):
        """
        Class to combine data from (one or multiple) files to a map.
        We always calculate !!File1*metric*File2!!

        Parameters
        ----------
        filepath1 : str
            Path to a file that contains data to combine
            We always calculate File1*metric*File2
        filepath1 : str
            Other path to a file that contains data to combine
            We always calculate File1*metric*File2
            To combine variables from one file, pass the same path as for file1
            here.
        lat_var : str, optional (default: 'lat')
            The name of the variable in the netcdf file that refers to the latitude
            of the observation.
        lon_var : str, optional (default: 'lon')
            The name of the variable in the netcdf file that refers to the longitude
            of the observation.
        resxy : tuple or None
            X and Y resolution of the netcdf images to combine (must have same shape)
            If None is passed we assume that the data is on an irregular grid and
            make scatter plot maps instead of regular gridded maps (as for ISMN stations).
        out_dir : str, optional (default: None)
            Out path where the plots are store to, if None is passed than we use
            the parent directory of file1.
        dpi : int, optional (default: 300)
            Resolution (dots per inch) of the map (also affects rasterised parts of
            vector plots!!)
        """

        self.ds1 = NcVarPlotter(filepath=filepath1, resxy=resxy,
                                out_dir=out_dir, lat_var=lat_var, lon_var=lon_var,
                                z_var=z_var, cell_center_origin=cell_center_origin)
        self.ds2 = NcVarPlotter(filepath=filepath2, resxy=resxy,
                                out_dir=out_dir, lat_var=lat_var, lon_var=lon_var,
                                z_var=z_var, cell_center_origin=cell_center_origin)

        # ds1 parent if out_dir is None, otherwise the correct one was passed to ds1
        self.out_dir = self.ds1.out_dir
        self.dpi = dpi

    def _load_times(self, time1, time2, var1, var2):
        self.ds1.read(time1, var1)
        self.ds2.read(time2, var2)

        times = [None, None]
        if self.ds1.time is not None:
            times[0] = self.ds1.time
        if self.ds2.time is not None:
            times[1] = self.ds2.time
        return times

    @staticmethod
    def _usemetric(s1, s2, metric):
        """
        We calculate 'variable1 *metric* variable2'
        """
        if metric in ['-', 'Difference']:
            return s1 - s2, 'Difference'
        elif metric == 'AbsDiff':
            return (s1 - s2).abs(), 'AbsDiff'
        elif metric in ['+', 'Sum']:
            return s1 + s2, 'Sum'
        elif metric in ['/', 'Ratio']:
            return s1 / s2, 'Ratio'
        elif metric in ['*', 'Product']:
            return s1 * s2, 'Product'
        elif metric == 'Mask1': # remove all were s2 is NOT 1
            cs1 = s1.copy(True)
            cs1.loc[s2.loc[s2 != 1.].index] = np.nan
            return cs1
        else:
            raise ValueError('Metric {} is not implemented'.format(metric))

    def plot_comb_variable(self, vards1, vards2, time1=None, time2=None,
                           metric='-', interface=True, transparent=False,
                           plotfile_name=None, file_format='png',
                           **plot_kwargs):
        """
        Plot a single variable from a certain time

        Parameters
        ---------
        vards1 : str
            Name of the variable to use in the first file
        vards2 : str
            Name of the variable to use in the second file
        time1 : datetime or str, optional (default: None)
            Date of the variable in the first file to use. If there are no
            dates, pass None.
        time2 : datetime or str, optional (default: None)
            Date of the variable in the second file to use. If there are no
            dates, pass None
        metric : str, optional (default: -)
            Metric to combine the 2 variables
            Difference, AbsDiff, Ratio, Product, Sum, or Mask1
        interface: bool, optional (default: True)
            Plot elements such as colorbar and title
        transparent: bool, optional (default: True)
            Make the background of the plot transparent.
        plotfile_name : str, optional (default: None)
            File name to store the plot, if this is None, we create a file name.
        file_format : str, optional (default: 'png')
            Format in which the plot is stored (e.g. pdf or svg for vector format)

        Returns
        ---------
        ds : pd.Series
            The created comb data frame, e.g. for calculating stats according to
            the plotted data.
        f : plt.figure
            The Figure that is created.
        imax : plt.Axes
            The axes of the map plot.
        """
        plt.close('all')

        self.times = self._load_times(time1, time2, vards1, vards2)
        # calc variable1 *metric* variable2
        s1 = self.ds1.df[vards1]
        s2 = self.ds2.df[vards2]
        # make sure the two have the same index names
        if self.ds1.index_name != self.ds2.index_name:
            s2.rename_axis(index=dict(zip(self.ds2.index_name, self.ds1.index_name)))
        cds, smetric = self._usemetric(s1, s2, metric)
        name = '{}_between_{}_and_{}'.format(smetric, vards1, vards2)

        df = cds.to_frame(name)
        if not interface:
            plot_kwargs['show_cbar'] = False

        if not self.ds1.irregular and not self.ds2.irregular:
            f, imax, im = cp_map(df, name, **plot_kwargs)
        else:
            f, imax, im = cp_scatter_map(lats=df.index.get_level_values(self.ds1.index_name[0]),
                                         lons=df.index.get_level_values(self.ds1.index_name[1]),
                                         values=df[name].values, **plot_kwargs)

        if not plotfile_name:
            plotfile_name = name

            if self.times in [[None, None], [datetime(1900, 1, 1), datetime(1900, 1, 1)]]:
                pass
            else:
                plotfile_name += 'at_{t1}_and_{t2}'.format(t1=str(self.times[0]),
                                                    t2=str(self.times[1]))

        if not os.path.exists(self.out_dir):
            os.makedirs(self.out_dir)

        plt.savefig(os.path.join(self.out_dir, plotfile_name + '.{}'.format(file_format)),
                    dpi=self.dpi, transparent=transparent, bbox_inches='tight')

        return df[name], f, imax


if __name__ == '__main__':
    irreg_file = r"C:\Temp\nc_compress\test1_with_test2.nc"
    reg_file = r"\\?\D:\data-write\paper_results\iter3\hsp_model_frames\CCI_45_COMBINED\intercomparison\ERA5\intercomparison\GLOBAL_basic_validation_1978-10-26_to_2018-12-31.nc"
    plotter = NcVarPlotter(filepath=reg_file,
                           lat_var='lat', lon_var='lon', resxy=(0.25,0.25),
                           cell_center_origin=True)
    plotter.plot_variable('n_obs', veg_mask=False, cbrange=(0,10000), ext_label_min='TEST',
                          ext_label_max='TEST2', extend='both', cblabel='testtest', file_format='pdf')