from os import listdir
from os.path import dirname, basename


# Import all the game managers

__all__ = list()
for f in listdir(dirname(__file__)):
    if f[-8:] == "_role.py" and not f.endswith("__init__.py"):
        __all__.append(basename(f)[:-3])
