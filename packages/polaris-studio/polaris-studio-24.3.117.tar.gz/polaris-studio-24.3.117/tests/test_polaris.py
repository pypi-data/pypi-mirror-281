import os
import uuid
from os.path import join, isfile
from pathlib import Path
from tempfile import gettempdir
from unittest import TestCase

from polaris import Polaris
from polaris.analyze.analyze import Analyze
from polaris.analyze.result_kpis import ResultKPIs
from polaris.demand.demand import Demand
from polaris.network.network import Network
from polaris.runs.convergence.convergence_iteration import ConvergenceIteration
from polaris.runs.wtf_runner import run_baseline_analysis
from polaris.utils.testing.temp_model import TempModel


class TestPolaris(TestCase):
    # The structure may not be necessary for now, but adds no run time and will be handy as we add more tests
    @classmethod
    def setUpClass(cls) -> None:
        cls.fldr = TempModel("Grid")

    def test_open_model(self):
        model = Polaris().from_dir(self.fldr)

        self.assertEqual(str(model.model_path), str(self.fldr))
        self.assertEqual(model.demand_file, Path(join(self.fldr, "Grid-Demand.sqlite")))
        self.assertEqual(model.supply_file, Path(join(self.fldr, "Grid-Supply.sqlite")))
        self.assertEqual(model.result_file, Path(join(self.fldr, "Grid-Result.sqlite")))

        model.load_config(join(self.fldr, "convergence_control.yaml"))

        # Now we call all methods just to make sure they work
        model.upgrade()

        self.assertIsInstance(model.network, Network)
        self.assertIsInstance(model.analyze, Analyze)
        self.assertIsInstance(model.analyze, Analyze)

        hwy_skim = model.skims.highway
        pt_skim = model.skims.transit
        self.assertEqual(hwy_skim.num_zones, pt_skim.num_zones)

        model.close()

    def test_create_from_git(self):
        direc = join(gettempdir(), f"polaris_{uuid.uuid4().hex}")
        _ = Polaris().build_from_git(direc, "Grid")

        print(list(os.walk(join(direc, "Grid", "built"))))
        self.assertTrue(isfile(join(direc, "Grid", "built", "Grid-Supply.sqlite")))
        self.assertTrue(isfile(join(direc, "Grid", "built", "Grid-Demand.sqlite")))

    def test_running(self):
        # This model is stored fully run
        model = Polaris().from_dir(self.fldr)
        model.upgrade()

        iteration = ConvergenceIteration.from_dir(Path(self.fldr) / "Grid_iteration_1")
        Demand.from_file(iteration.files.demand_db).upgrade()
        run_baseline_analysis(iteration, model.run_config.population_scale_factor)

        # Just run through the available metrics and re-calculate them to flush out gremlins
        kpis = ResultKPIs.from_iteration(iteration, clear_cache=True)
        kpis.cache_all_available_metrics()
