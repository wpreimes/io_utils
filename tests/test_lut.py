import pytest

from io_utils.luts import lookup_lc, lookup_ismn_sensor
import numpy as np

def test_lookup():
    assert lookup_ismn_sensor(['Flower-Power']) == np.array(['Flower-Power'])
    assert np.all(lookup_lc([110, 120]) == np.array(['TreeCover', 'Grassland']))
    assert np.all(lookup_lc([110, 120, 999], ignore_missing=True) == np.array(['TreeCover', 'Grassland', np.nan]))
    with pytest.raises(ValueError):
        lookup_lc([110, 120, 999], ignore_missing=False)
    assert len(lookup_ismn_sensor(['Capacitance', 'TDR'])) > 0
    assert len(lookup_lc(['Grassland', 'TreeCover'])) > 0
