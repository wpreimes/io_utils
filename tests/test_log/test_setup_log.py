from tempfile import mkdtemp
from io_utils.logging import logger
import os

def test_create_logfile():
    path = mkdtemp()
    msg = "Test running"
    fpath, mylogger = logger.create(path, 'mylog')
    mylogger.info(msg)

    print(fpath)
    print(os.path.isfile(fpath))
    with open(fpath) as f:
        f = f.readlines()

    assert msg in f[0]

if __name__ == '__main__':
    test_create_logfile()