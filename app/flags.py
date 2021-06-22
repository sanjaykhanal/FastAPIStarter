from easydict import EasyDict



flags = EasyDict()


# Set the required flags.
flags.needs_setup = False
flags.enable_authentication = True
flags.allow_cors = True             # Further rules for cors are defined in config/config.py

flags.include_modules = [
    'authentication'
]
flags.enable_test_console = False


def get_flags():
    return flags
