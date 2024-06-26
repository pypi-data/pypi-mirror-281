# Copyright © 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
import importlib.util as iutil

inside_qgis = iutil.find_spec("qgis") is not None
