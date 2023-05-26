import inspect
import io_utils.plot.colormaps as mycmaps

def test_all_colormaps():
    functions = inspect.getmembers(mycmaps, inspect.isfunction)
    function_names = [name for name, _ in functions]
    for name in function_names:
        getattr(mycmaps, name)()

if __name__ == '__main__':
    test_all_colormaps()
