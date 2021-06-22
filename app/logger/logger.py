import time
import os
import zlib
import logging
import logging.handlers
from logging import Formatter

from config.config import LOGGER_MAX_SIZE, LOGGER_MAX_FILES, LOGGER_PATH, LOGGER_FILENAME


# name the compressed file
def namer(name):
    return name + ".gz"


# read the data from source, compress it, write it to dest and delete source
def rotator(source, dest):
    with open(source, "rb") as sf:
        data = sf.read()
        compressed = zlib.compress(data, 9)
        with open(dest, "wb") as df:
            df.write(compressed)
    os.remove(source)


def set_size_based_rotating_log(log_path=LOGGER_PATH, log_name=LOGGER_FILENAME):
    """creates a logger object that logs messages in the log_path with log_name"""

    # Checks if the path exists otherwise tries to create it
    if not os.path.exists(log_path):
        try:
            os.makedirs(log_path)
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print(exc_type, exc_value, exc_traceback)

    # Sets the format and level of logging records
    format = '%(asctime)s - %(levelname)s - [%(pathname)s:%(lineno)s - %(funcName)10s() ] - %(message)s'
    formatter = Formatter(format)
    level=logging.DEBUG

    # Does basic configuration for the logging system
    logging.basicConfig(format=format, level=level)

    # Instantiates a logger object
    logger = logging.getLogger("")

    handler = logging.handlers.RotatingFileHandler(filename=log_path+'/'+log_name,
                                       maxBytes=LOGGER_MAX_SIZE,
                                       backupCount=LOGGER_MAX_FILES)
    handler.setFormatter(formatter)
    handler.rotator = rotator
    handler.namer = namer
    logger.addHandler(handler)
    return logger
