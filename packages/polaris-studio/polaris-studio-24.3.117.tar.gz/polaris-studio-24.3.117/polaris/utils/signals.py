# Copyright © 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
import importlib.util as iutil

qgis = iutil.find_spec("qgis") is not None


def noop(_):
    pass


if iutil.find_spec("qgis"):
    from PyQt5.QtCore import pyqtSignal as SIGNAL  # type: ignore

    noop(SIGNAL.__class__)  # This should be no-op but it stops PyCharm from "optimising" the above import
else:
    from polaris.utils.python_signal import PythonSignal as SIGNAL  # type: ignore

    noop(SIGNAL.__class__)  # This should be no-op but it stops PyCharm from "optimising" the above import
