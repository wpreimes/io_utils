from tempfile import mkdtemp
from io_utils.logging import logger
import logging
import os

def test_create_logfile():
    path = mkdtemp()
    msg = "Test running"
    fpath = logger.create(path, 'mylog')
    logging.info(msg)

    print(fpath)
    print(os.path.isfile(fpath))
    with open(fpath) as f:
        f = f.readlines()

    assert msg in f[0]