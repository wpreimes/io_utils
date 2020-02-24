
from datetime import datetime
import os
import logging
import sys

def setup(fname, level=logging.DEBUG, verbose=False):
	logging.basicConfig(filename=fname, level=level,
                        format='%(levelname)s %(asctime)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
	if verbose:
		logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
	logging.captureWarnings(True)

def create(log_file_path, log_fname='create', **kwargs):
	"""
	sets up the log file name based on the input configuration file and the cell
	or gpi being processed
	"""
	tnow = "_{:%Y%m%d%H%M%S.%f}".format(datetime.now())
	fname = log_fname + tnow + ".log"
	fname = os.path.join(log_file_path, fname) #t
	# imestamp used as unique identifier
	setup(fname, **kwargs) #sets up logging file

	return fname