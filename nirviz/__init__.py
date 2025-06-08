from importlib.metadata import version as metadata_version, PackageNotFoundError

# Exposing imports
from .nirviz import visualize

try:
    # For pyproject.toml dynamic versioning
    __version__ = version = metadata_version("nirviz")
    del metadata_version
except PackageNotFoundError:
    print('nirviz: package not found')
    pass
