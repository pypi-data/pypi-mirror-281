import logging


def get_logger(name: str = None, verbosity: int = 0) -> logging.Logger:
    log = logging.getLogger(name)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    log.addHandler(ch)
    if verbosity < 0:
        log.setLevel(logging.WARNING)
    elif verbosity > 0:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)
    return log
