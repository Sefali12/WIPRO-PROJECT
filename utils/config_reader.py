"""
config_reader.py
-----------------
Loads config/config.yaml once and exposes it as a dict-like singleton so
every layer of the framework (driver factory, pages, tests) reads settings
from ONE place instead of scattering hardcoded values.
"""

import os
import yaml

_CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "config",
    "config.yaml",
)

_config_cache = None


def get_config():
    """Return the parsed config.yaml as a dict (cached after first read)."""
    global _config_cache
    if _config_cache is None:
        with open(_CONFIG_PATH, "r", encoding="utf-8") as f:
            _config_cache = yaml.safe_load(f)
    return _config_cache
