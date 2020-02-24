from tempfile import mkdtemp
import io_utils.logging.logger as logger
import logging

def test_create_logfile():
    path = mkdtemp()
    msg = "Test running"
    fpath = logger.create(path, 'create')
    logging.info(msg)

    with open(fpath) as f:
        f = f.readlines()

    assert msg in f[0]

if __name__ == '__main__':
    test_create_logfile()