# espn_nfl_api/__init__.py

from .api import ESPNAPI
from .exceptions import APIError

__all__ = ["ESPNAPI", "APIError"]