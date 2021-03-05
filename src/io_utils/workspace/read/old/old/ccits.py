
from old.ESA_CCI_interface import ESA_CCI_SM_cfg
import numpy as np

class CCITs_old(object):
    """
    Read CCI SM (flagged) data
    """
    def __init__(self, version, product, dropna=True, cfg_file=None, read_flags=None,
                 grid=None, resample='D', scale_factors=None, **kwargs):
        """
        Read a CCI time series

        Parameters
        ----------
        version : str
            Version string of the CCI product to read
        product : str
            product to read from the file
        dropna : bool
            Replace 9999 with nans
        cfg_file : str, optional (default: None)
            path to the config file for reading the cci data
            If None is passed we search one a default directory
                (../data-read-write/cci_cfg_local/<os>)
        read_flags : list, optional (default: [0])
            List of flags for which we read observations, others are not read
            and not in the returned data frame!
            If None is passed, all vales are returned.
        grid : pygeogrids.CellGrid, optional (default: None)
            Grid to use for reading, if None is passed the one from the cfg file is
            used.
        resample : str, optional (default: D)
            How the data frame is resampled after reading
        scale_factors : dict, optional (default: None)
            Multiplicative scale factor (item) for the columns (key)
        kwargs : dict, optional
            Other kwargs to use (e.g ioclass_kws or parameters)
        """
        self.resample = resample
        self.dropna = dropna
        self.product = product
        self.scale_factors = scale_factors
        self.reader = ESA_CCI_SM_cfg(version='ESA_CCI_SM_v0%s' % version,
                                     product=product, cfg_file=cfg_file, grid=grid,
                                     **kwargs)
        self.read_flags = read_flags
        if self.read_flags is not None:
            self.read_flags = list([read_flags]) if not isinstance(read_flags, list) else read_flags
            self.flag_name = 'flag'
            if ('parameter' in kwargs.keys()) and (self.flag_name not in kwargs['parameter']):
                kwargs.parameters.append(self.flag_name)

        self.grid = self.reader.grid  # type: pygeogrids.CellGrid

    def read_ts(self, *args):
        try:
            df_cci = pd.DataFrame(self.reader.read(*args))
        except IOError:
            df_cci = pd.DataFrame()

        if 'sm_noise' in df_cci.columns:
            df_cci = df_cci.rename(columns={'sm_noise': 'sm_uncertainty'})

        if df_cci.empty:
            if 'ADJUSTED' in self.product:
                return pd.DataFrame(columns=['adjusted'])
            else:
                return pd.DataFrame(columns=['sm', 'sm_uncertainty', 'flag'])

        if self.scale_factors is None:
            raise ValueError(self.scale_factors,
                             "Need to pass scale factors to define the SM col")

        sm_col = list(self.scale_factors.keys())[0]

        if self.read_flags is not None:
                df_cci = df_cci.loc[df_cci[self.flag_name].isin(self.read_flags), :]
                df_cci = df_cci.drop(columns=[self.flag_name])

        if not df_cci.empty:
            if 'ADJUSTED' in self.product:
                if self.dropna:
                    df_cci = df_cci.dropna(subset=[sm_col])
            else:
                placeholder = np.nanmin(df_cci[sm_col])

                # just so we never delete any actual data:
                if placeholder not in [-9999., -999999., -999900.]:
                    placeholder = -9999.

                for col in df_cci.columns:
                    df_cci.loc[df_cci[col] == placeholder, col] = np.nan

                if self.dropna:
                    df_cci = df_cci.dropna(subset=[sm_col])

        if not df_cci[sm_col].empty:
            for col, sf in self.scale_factors.items():
                if col in df_cci.columns:
                    df_cci[col] *= sf

        if self.resample:
            df_cci = df_cci.resample(self.resample).mean()

        return df_cci
