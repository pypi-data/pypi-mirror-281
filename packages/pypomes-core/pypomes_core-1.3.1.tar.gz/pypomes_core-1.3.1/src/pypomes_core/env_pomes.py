import os
from pathlib import Path
from typing import Final

# the prefix for the names of the environment variables
APP_PREFIX: Final[str] = os.getenv("PYPOMES_APP_PREFIX", "")


def env_get_str(key: str,
                def_value: str = None) -> str:
    """
    Retrieve and return the string value defined for *key* in the current operating environment.

    :param key: The key the value is associated with
    :param def_value: The default value to return, if the key has not been defined
    :return: The str value associated with the key
    """
    result: str = os.getenv(key)
    if result is None:
        result = def_value

    return result


def env_get_bool(key: str,
                 def_value: bool = None) -> bool:
    """
    Retrieve and return the boolean value defined for *key* in the current operating environment.

    :param key: The key the value is associated with
    :param def_value: The default value to return, if the key has not been defined
    :return: The bool value associated with the key
    """
    result: bool
    try:
        result = os.environ[key].lower() in ["1", "t", "true"]
    except (AttributeError, KeyError, TypeError):
        result = def_value

    return result


def env_get_int(key: str,
                def_value: int = None) -> int:
    """
    Retrieve and return the int value defined for *key* in the current operating environment.

    :param key: The key the value is associated with
    :param def_value: The default value to return, if the key has not been defined
    :return: The int value associated with the key
    """
    result: int
    try:
        result = int(os.environ[key])
    except (AttributeError, KeyError, TypeError):
        result = def_value

    return result


def env_get_float(key: str,
                  def_value: float = None) -> float:
    """
    Retrieve and return the float value defined for *key* in the current operating environment.

    :param key: The key the value is associated with
    :param def_value: The default value to return, if the key has not been defined
    :return: The float value associated with the key
    """
    result: float
    try:
        result = float(os.environ[key])
    except (AttributeError, KeyError, TypeError):
        result = def_value

    return result


def env_get_path(key: str,
                 def_value: Path = None) -> Path:
    """
    Retrieve and return the path value defined for *key* in the current operating environment.

    :param key: The key the value is associated with
    :param def_value: The default value to return, if the key has not been defined
    :return: The path value associated with the key
    """
    result: Path
    try:
        result = Path(os.environ[key])
    except (AttributeError, KeyError, TypeError):
        result = def_value

    return result
