# -*- coding: utf-8 -*-
"""
Benchmark NNPDF pdf family
"""
import numpy as np
from banana import register

from ekomark.benchmark.runner import Runner

register(__file__)


class BenchmarkNNPDF(Runner):
    """
    Globally set the external program to LHAPDF
    """

    external = "LHAPDF"

    # Rotate to evolution basis
    rotate_to_evolution_basis = True

    def skip_pdfs(self, _theory):
        return [
            -6,
            6,
            22,
            "ph",
            "T35",
            "V35",
        ]


base_operator = {"ev_op_iterations": 1, "backward_inversion": "exact"}

base_theory = {
    "Qref": 91.2,
    "mc": 1.51,
    "mb": 4.92,
    "mt": 172.5,
    "kcThr": 1.0,
    "kbThr": 1.0,
    "ktThr": 1.0,
    "alphas": 0.118000,
    "alphaqed": 0.007496,
    "FNS": "ZM-VFNS",
    "ModEv": "TRN",
}


class BenchmarkNNPDF31(BenchmarkNNPDF):
    """Benchmark NNPDF3.1"""

    def benchmark_nlo(self, Q0=1.65, Q2grid=(100,)):
        theory_card = {
            **base_theory,
            "PTO": 1,
            "QED": 0,
            "Q0": Q0,
        }

        operator_card = {**base_operator, "Q2grid": list(Q2grid)}
        self.run([theory_card], [operator_card], ["NNPDF31_nlo_as_0118"])


class BenchmarkNNPDF40(BenchmarkNNPDF):
    """Benchmark NNPDF4.0"""

    def benchmark_nlo(self, Q0=1.65, Q2grid=(100,)):
        theory_card = {
            **base_theory,
            "PTO": 1,
            "QED": 0,
            "Q0": Q0,
        }

        operator_card = {**base_operator, "Q2grid": list(Q2grid)}
        self.run([theory_card], [operator_card], ["NNPDF40_nlo_as_01180"])

    def benchmark_nnlo(self, Q0=1.65, Q2grid=(100,)):
        theory_card = {
            **base_theory,
            "PTO": 2,
            "QED": 0,
            "IC": 1,
            "IB": 1,
            "Q0": Q0,
        }

        operator_card = {**base_operator, "Q2grid": list(Q2grid)}
        self.run([theory_card], [operator_card], ["NNPDF40_nnlo_as_01180"])


if __name__ == "__main__":
    low2 = 4**2
    high2 = 30**2
    # nn31 = BenchmarkNNPDF31()
    # # test forward
    # nn31.benchmark_nlo(Q0=np.sqrt(low2), Q2grid=[10])
    # # test backward
    # #nn31.benchmark_nlo(Q0=np.sqrt(high2), Q2grid=[low2])
    nn40 = BenchmarkNNPDF40()
    # nn40.benchmark_nnlo(Q2grid=[100])
    nn40.benchmark_nnlo(Q0=np.sqrt(high2), Q2grid=[low2])
