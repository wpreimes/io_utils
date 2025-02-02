import os

# Note: Must be set BEFORE the first numpy import!!
os.environ['MKL_NUM_THREADS'] = '1'
os.environ['NUMEXPR_NUM_THREADS'] = '1'
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['MKL_DYNAMIC'] = 'FALSE'
os.environ['OPENBLAS_NUM_THREADS'] = '1'

import numpy as np
from tqdm import tqdm
import logging
from multiprocessing import Pool
from datetime import datetime
import sys
from warnings import warn

# Note: Might not work under windows... Maybe with py 3.10?

def apply_to_elements(
        FUNC, ITER_KWARGS, STATIC_KWARGS=None, n_proc=1,
        show_progress_bars=True, ignore_errors=False, log_path=None,
        debug_mode=False,
):
    """
    Applies the passed function to all elements of the passed iterables.
    Usually the iterable is a list of cells, but it can also be a list of
    e.g. images etc.

    Parameters
    ----------
    FUNC: Callable
        Function to call.
    ITER_KWARGS: dict
        Container that holds iterables to split up and call in parallel with
        FUNC:
        Usually something like 'cell': [cells, ... ]
        If multiple, iterables MUST HAVE THE SAME LENGTH.
        We iterate through all iterables and pass them to FUNC as individual
        kwargs. i.e. FUNC is called N times, where N is the length of
        iterables passed in this dict. Can not be empty!
    STATIC_KWARGS: dict, optional (default: None)
        Kwargs that are passed to FUNC in addition to each element in
        ITER_KWARGS. Are the same for each call of FUNC!
    n_proc: int, optional (default: 1)
        Number of parallel workers
    show_progress_bars: bool, optional (default: True)
        Show how many iterables were processed already.
    log_path: str, optional (default: None)
        If provided, a log file is created in the passed directory.
    debug_mode: float, optional (default: False)
        Print logging messages to stdout, useful for debugging.

    Returns
    -------
    results: list
        List of return values from each function call
    """
    warn("This function is deprecated and will be removed in the future. "
         "Use the new function version from repurpose.proc instead.",
         DeprecationWarning)
    logger = logging.getLogger()
    streamHandler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    streamHandler.setFormatter(formatter)

    if STATIC_KWARGS is None:
        STATIC_KWARGS = dict()

    if debug_mode:
        logger.setLevel('DEBUG')
        logger.addHandler(streamHandler)

    if log_path is not None:
        log_file = os.path.join(log_path,
            f"{FUNC.__name__}_{datetime.now().strftime('%Y%m%d%H%M')}.log")
    else:
        log_file = None

    if log_file:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format="%(levelname)s %(asctime)s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    n = np.array([len(v) for k, v in ITER_KWARGS.items()])
    if len(n) == 0:
        raise ValueError("No ITER_KWARGS passed")
    if len(n) > 1:
        if not np.all(np.diff(n) == 0):
            raise ValueError(
                "Different number of elements found in ITER_KWARGS."
                f"All passed Iterable must have the same length."
                f"Got: {n}")
    n = n[0]

    i1d = np.intersect1d(np.array(list(ITER_KWARGS.keys())),
                         np.array(list(STATIC_KWARGS.keys())))
    if len(i1d) > 0:
        raise ValueError(
            "Got duplicate(s) in ITER_KWARGS and STATIC_KWARGS. "
            f"Must be unique. Duplicates: {i1d}")

    process_kwargs = []
    for i in range(n):
        kws = {k: v[i] for k, v in ITER_KWARGS.items()}
        kws.update(STATIC_KWARGS)
        process_kwargs.append(kws)

    if show_progress_bars:
        pbar = tqdm(total=len(process_kwargs), desc=f"Processed")
    else:
        pbar = None

    results = []

    def update(r) -> None:
        if r is not None:
            results.append(r)
        if pbar is not None:
            pbar.update()

    def error(e) -> None:
        logging.error(e)
        if not ignore_errors:
            raise e
        if pbar is not None:
            pbar.update()

    if n_proc == 1:
        for kwargs in process_kwargs:
            try:
                r = FUNC(**kwargs)
                update(r)
            except Exception as e:
                error(e)
    else:

        with Pool(n_proc) as pool:
            for kwds in process_kwargs:
                pool.apply_async(
                    FUNC,
                    kwds=kwds,
                    callback=update,
                    error_callback=error,
                )
            pool.close()
            pool.join()

    if pbar is not None:
        pbar.close()

    if debug_mode:
        logger.handlers.clear()

    handlers = logger.handlers[:]
    for handler in handlers:
        logger.removeHandler(handler)
        handler.close()

    return results
