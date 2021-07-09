from pytesmo.validation_framework.adapters import *

class ColumnCombineAdapter(BasicAdapter):
    """
    Takes the pandas DataFrame that the read_ts or read method of the instance
    returns and applies a function to merge multiple columns into one.
    E.g. when there are 2 Soil Moisture parameters in a dataset that should be
    averaged on reading. Will add one additional column to the input data frame.
    """

    def __init__(self, cls, func, func_kwargs=None, columns=None, new_name='merged'):
        """
        Parameters
        ----------
        cls : class instance
            Must have a read_ts or read method returning a pandas.DataFrame
        func: Callable
            Will be applied to dataframe columns using pd.DataFrame.apply(..., axis=1)
            additional kwargs for this must be given in func_kwargs,
            e.g. pd.DataFrame.mean
        func_kwargs : dict, optional (default: None)
            kwargs that are passed to method
        columns: list, optional (default: None)
            Columns in the dataset that are combined. If None are selected
            all columns are used.
        new_name: str, optional (default: merged)
            Name that the merged column will have in the returned data frame.
        """

        super(ColumnCombineAdapter, self).__init__(cls)
        self.func = func
        self.func_kwargs = func_kwargs if func_kwargs is not None else {}
        self.func_kwargs['axis'] = 1
        self.columns = columns
        self.new_name = new_name

    def apply(self, data: DataFrame) -> DataFrame:
        columns = data.columns if self.columns is None else self.columns
        new_col = data[columns].apply(self.func, **self.func_kwargs)
        data[self.new_name] = new_col
        return data

    def read_ts(self, *args, **kwargs) -> DataFrame:
        data = super(ColumnCombineAdapter, self).read_ts(*args, **kwargs)
        return self.apply(data)

    def read(self, *args, **kwargs) -> DataFrame:
        return self.read_ts(*args, **kwargs)