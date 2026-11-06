"""Regression checks for nonfinite components outside the axial comparison.

Run from the documentation repository: python -m unittest discover -s tests
Requires the tutorial's NumPy and Matplotlib dependencies, but no DES binary.
"""

from pathlib import Path
import runpy
import tempfile
from types import SimpleNamespace
import unittest

import numpy as np


SCRIPT = Path(__file__).resolve().parents[1] / "static/tutorial/pt/analyze_pt.py"
ANALYSIS = SimpleNamespace(**runpy.run_path(str(SCRIPT)))


class ElasticOutput:
    """Small homogeneous output fixture exposing the DES reader interface."""

    def __init__(self, ndims):
        self.ndims = ndims
        self.frames = self.steps = list(range(4))
        self.time = np.arange(4) * 0.01
        self.fields = {}
        axial_strain = -1e5 / (1e7 + 4e7 / 3)
        for frame in self.frames:
            coordinate = np.zeros((2, ndims))
            coordinate[0, -1] = -1
            velocity = np.zeros_like(coordinate)
            strain = np.zeros((1, 3 if ndims == 2 else 6))
            stress = np.zeros_like(strain)
            if frame:
                strain[0, ndims - 1] = axial_strain
                stress[0, :ndims] = -1e5 / 7
                stress[0, ndims - 1] = -1e5
            if frame == 1:
                velocity[1, -1] = axial_strain / 0.01
            for name, field in (("coordinate", coordinate), ("velocity", velocity),
                                ("strain", strain), ("stress", stress)):
                self.fields[frame, name] = field

    def read_field(self, frame, name):
        return self.fields[frame, name].copy()


class AnalysisTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.prefix = Path(self.directory.name) / "elastic"
        self.prefix.with_suffix(".log").write_text("".join(
            f"PT step={step} status=converged iterations=1 residual=0 initial=0 "
            "threshold=1 warm_initial=0 evaluations=1 stage=before_physical_updates\n"
            for step in range(1, 4)))

    def test_finite_elastic_output_passes_in_both_dimensions(self):
        for ndims in (2, 3):
            with self.subTest(ndims=ndims):
                model = ElasticOutput(ndims)
                ANALYSIS.read_model(lambda _: model, self.prefix, "elastic")
                self.assertTrue(self.prefix.with_suffix(".csv").is_file())

    def test_nonfinite_nonaxial_components_are_rejected(self):
        for ndims in (2, 3):
            for name in ("stress", "strain", "velocity", "coordinate"):
                for value in (np.nan, np.inf):
                    with self.subTest(ndims=ndims, field=name, value=value):
                        model = ElasticOutput(ndims)
                        model.fields[1, name][0, 0] = value
                        with self.assertRaisesRegex(ValueError, f"nonfinite {name} at frame 1"):
                            ANALYSIS.read_model(lambda _: model, self.prefix, "elastic")


if __name__ == "__main__":
    unittest.main()
