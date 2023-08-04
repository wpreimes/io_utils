# -*- coding: utf-8 -*-
from io_utils.data.grid.grid_functions import read_cells_for_continent

def test_read_cells_for_continent():
    try:
        read_cells_for_continent('notexistingname')
    except ValueError:
        assert True
    else:
        assert False

    cells = read_cells_for_continent('Oceania')
    assert 2244 in cells

if __name__ == '__main__':
    test_read_cells_for_continent()

