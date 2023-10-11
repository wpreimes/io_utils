from pytesmo.validation_framework.adapters import *

def lprm_bt2surft(bt, smooth=14):
    """
    Convert brightness temperature to surface temperature folling the LPRM
    approach.

    Parameters
    ----------
    bt: pd.Series
        Brightness temperature input time series (usually K band, V pol. and
        daily).
    smooth: int, optional (default: 14)
        Number of values to use for smoothing the time series (backward
        window). If None or 0, then no smoothing is performed.

    Returns
    -------
    tsurf: pd.Series
        Surface temperature time series derived from the brightness
        temperature input time series.
    """
    if smooth:
        tsurf = 0.893 * bt.rolling(smooth, min_periods=1, center=False).apply(
        np.nanmean) + 44.8
    else:
        tsurf = 0.893 * bt + 44.8

    return tsurf


class PreprocessingAdapter(BasicAdapter):
    """
    Takes the pandas DataFrame that reader returns and applies a preprocessing
    function to it.

    Parameters
    ----------
    cls: object
        Reader object, has to have a `read_ts` or `read` method or a method
        name must be specified in the `read_name` kwarg. The same method will
        be available for the adapted version of the reader.
    func: Callable
        Preprocessing function that takes a pandas Series as input and
        returns a pandas Series as output.
    column: str, optional (default: None)
        Name of the Column where the preprocessing function should be applied.
        The original values will be replaced by the values that the function
        returns.
    read_name: str, optional (default: None)
        To enable the adapter for a method other than `read` or `read_ts`
        give the function name here (a function of that name must exist in
        cls). A method of the same name will be added to the adapted
        Reader, which takes the same arguments as the base method.
        The output of this method will be changed by the adapter.
        If None is passed, only data from `read` and `read_ts` of cls
        will be adapted.
    kwargs:
        Any remaining keyword arguments will be passed to the preprocessing
        function `func`.
    """

    def __init__(self, cls, func, column=None, **kwargs):

        cls_kwargs = dict()
        if "data_property_name" in kwargs:
            cls_kwargs["data_property_name"] = kwargs.pop("data_property_name")
        if "read_name" in kwargs:
            cls_kwargs["read_name"] = kwargs.pop("read_name")

        super().__init__(cls, **cls_kwargs)

        self.column = column
        self.func = func
        self.kwargs = kwargs

    def _adapt(self, data):
        """
        Apply the preprocessing function to the data.

        Parameters
        ----------
        data: pd.DataFrame
            DataFrame containing the time series. As returned by the read
            function of the original reader.

        Returns
        -------
        data: pd.DataFrame
            DataFrame containing the adapted column time series.
        """
        data = super()._adapt(data)
        data[self.column] = self.func(data[self.column], **self.kwargs)
        return data


class AnomalyClimAdapter(BasicAdapter):
    """
    Takes the pandas DataFrame that reader returns and calculates the
    anomaly of the time series based on the (long-term) average of the series.

    Parameters
    ----------
    cls: object
        Reader object, has to have a `read_ts` or `read` method or a method
        name must be specified in the `read_name` kwarg. The same method will
        be available for the adapted version of the reader.
    columns: list, optional (default: None)
        Columns in the dataset for which to calculate anomalies. If None is
        passed, the anomaly is calculated for all columns.
    data_property_name: str, optional (default: "data")
        Attribute name under which the pandas DataFrame containing the time
        series is found in the object returned by the read function of the
        original reader. Ignored if no attribute of this name is found.
        Then it is required that the DataFrame is already the return value
        of the read function.
    read_name: str, optional (default: None)
        To enable the adapter for a method other than `read` or `read_ts`
        give the function name here (a function of that name must exist in
        cls). A method of the same name will be added to the adapted
        Reader, which takes the same arguments as the base method.
        The output of this method will be changed by the adapter.
        If None is passed, only data from `read` and `read_ts` of cls
        will be adapted.
    return_clim: bool, optional (default: False)
        If True, then a column for the climatology is added to the DataFrame
        returned by the read function.
    kwargs:
        Any remaining keyword arguments will be given to
        :func:`pytesmo.time_series.anomaly.calc_climatology`
    """

    def __init__(self, cls, columns=None, return_clim=False, **kwargs):

        cls_kwargs = dict()
        if "data_property_name" in kwargs:
            cls_kwargs["data_property_name"] = kwargs.pop("data_property_name")
        if "read_name" in kwargs:
            cls_kwargs["read_name"] = kwargs.pop("read_name")

        super().__init__(cls, **cls_kwargs)

        self.return_clim = return_clim
        self.kwargs = kwargs
        self.columns = columns

    def _adapt(self, data):
        data = super()._adapt(data)
        if self.columns is None:
            ite = data
        else:
            ite = self.columns
        for column in ite:
            clim = calc_climatology(data[column], **self.kwargs)
            anom = calc_anomaly(data[column], climatology=clim,
                                return_clim=self.return_clim)
            if self.return_clim:
                data[column] = anom['anomaly']
                data[f"{column}_climatology"] = anom['climatology']
            else:
                data[column] = anom

        return data
