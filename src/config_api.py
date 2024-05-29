"""
This file has all the default configs and the necessary getters and setters for the same

USAGE:

1. importing cfg

from src.config_api import get_config_api
cfg = get_config_api()


2. using it

to read -> cfg.DEFAULT_READ_ENCODING
to update -> cfg.DEFAULT_READ_ENCODING = 'latin1'

"""

# Importing Dependencies

from src.error_types import (
    ConfigNotFoundError
)


from typing import (
    Any
)


# Singleton cfg
cfg = None


class ConfigAPI:

    """
    A simple config class that has getter and setter
    examples in the file docstring
    """

    ##################################################
    #           Available Global Variables           #
    ##################################################

    CONFIG_VARS = {
        "DEFAULT_READ_ENCODING": 'utf-8'
    }


    ##################################################
    #                    Getters                     #
    ##################################################

    def __getattribute__(self, __name: str) -> Any:
        try:
            return self.CONFIG_VARS[__name]
        except:
            raise ConfigNotFoundError

    def __setattr__(self, __name: str, __value: Any) -> None:
        try:
            if __name in self.CONFIG_VARS and isinstance(__value, type(self.CONFIG_VARS[__name])):
                self.CONFIG_VARS[__name] = __value
                return
            raise
        except:
            raise ConfigNotFoundError

def get_config_api():
    global cfg
    if cfg is None:
        cfg = ConfigAPI()
    return cfg