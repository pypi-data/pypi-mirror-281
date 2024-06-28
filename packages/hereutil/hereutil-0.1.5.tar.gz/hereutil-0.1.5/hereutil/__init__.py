from __future__ import annotations
import os
import sys
import warnings
from os import PathLike
from pathlib import Path
from typing import Any, Optional
from importlib import reload
from pyprojroot.here import here


def source(file: str, globals: Optional[dict[str, Any]] = None, locals: Optional[dict[str, Any]] = None) -> None:
    """Source a python file

    Source a given python file in the current (or given) context

    Parameters
    ----------
    file: str
        The file to source
    globals: dict[str, Any], optional
        A globals object, if not the one of the caller
    locals: dict[str, Any], optional
        A locals object, if not the one of the caller
    """
    if globals is None:
        globals = sys._getframe(1).f_globals
    if locals is None:
        locals = sys._getframe(1).f_locals
    with open(file, "rb") as f:
        code = compile(f.read(), file, 'exec')
        exec(code, globals, locals)


def add_to_sys_path(location: str | PathLike[str] = here(), warn: bool = True) -> None:
    """Add a location to the system path for importing

    Parameters
    ----------
    location: str | PathLike[str]
        The path to add to sys.path
    warn: bool, optional
        Warn if the path to be added does not exist. Defaults to True.
    """
    if warn and not os.path.exists(location):
        warnings.warn("Path doesn't exist: {}".format(location))
    if isinstance(location, PathLike):
        location = str(location)
    if location not in sys.path:
        sys.path.insert(0, location)


def remove_from_sys_path(location: str | PathLike[str] = here()) -> None:
    """Remove a location from the system path

    Parameters
    ----------
    location: str | PathLike[str]
        The path to remove from sys.path
    """
    if isinstance(location, PathLike):
        location = str(location)
    sys.path.remove(location)


__all__ = ["here", "source", "add_to_sys_path", "remove_from_sys_path", "reload"]
