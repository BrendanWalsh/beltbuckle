from importlib import resources

try:
    import tomllib
except ModuleNotFoundError:
    # Third party imports
    import tomli as tomllib

__version__ = "0.0.0"
_cfg = tomllib.loads(resources.read_text("beltbuckle", "config.toml"))
