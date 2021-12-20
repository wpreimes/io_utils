
from datetime import datetime
import os
import logging
import sys
from functools import wraps

def setup(fname, level=logging.DEBUG, verbose=False):

    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    logging.basicConfig(filename=fname, level=level,
                        format='%(levelname)s %(asctime)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger()
    if verbose:
        logger.addHandler(logging.StreamHandler(sys.stdout))
    logging.captureWarnings(True)

    if not os.path.exists(fname):
        raise ValueError(f"Path does not exist: {fname}")

    return logger

def create(log_file_path, prefix='logfile', **kwargs):
    """
    sets up the log file name based on the input configuration file and the cell
    or gpi being processed
    """
    if not os.path.exists(log_file_path):
        os.makedirs(log_file_path)

    tnow = "_{:%Y%m%d%H%M%S.%f}".format(datetime.now())
    fname = prefix + tnow + ".log"
    fname = os.path.join(log_file_path, fname) #timestamp used as unique identifier
    logger = setup(fname, **kwargs) #sets up logging file

    return fname, logger