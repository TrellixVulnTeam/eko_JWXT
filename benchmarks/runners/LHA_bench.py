# -*- coding: utf-8 -*-
"""
    Benchmark EKO to :cite:`Giele:2002hx`
"""
import numpy as np

from banana.data import power_set

from ekomark.benchmark.runner import Runner
from ekomark.data import operators


class LHABenchmark(Runner):

    """
    Globally set the external program to LHA
    """

    external = "LHA"

    rotate_to_evolution_basis = True

    # pdf to skip
    skip_pdfs = [22, -6, 6, "ph", "V35", "V24", "V15", "V8", "T35"]


class BenchmarkZm(LHABenchmark):
    """Benckmark ZM-VFNS """

    zm_theory = {
        "FNS": "ZM-VFNS",
        "ModEv": "EXA",
        "Q0": np.sqrt(2),
        "kcThr": 1.0,
        "kbThr": 1.0,
        "ktThr": 1.0,
        "mc": np.sqrt(2.0),
        "mb": 4.5,
        "mt": 175,
        "Qref": np.sqrt(2.0),
        "alphas": 0.35,
    }

    def benchmark_zm(self, pto):

        th = self.zm_theory.copy()
        th.update({"PTO": pto})
        self.run([th], operators.build(operators.lha_config), ["ToyLH"])


class BenchmarkFfns(LHABenchmark):
    """Benckmark FFNS """

    ffns_theory = {
        "FNS": "FFNS",
        "NfFF": 4,
        "ModEv": "EXA",
        "Q0": np.sqrt(2),
        "kcThr": 0.0,
        "kbThr": np.inf,
        "ktThr": np.inf,
        "Qref": np.sqrt(2.0),
        "alphas": 0.35,
    }

    def benchmark_ffns(self, pto):

        th = self.ffns_theory.copy()
        th.update({"PTO": pto})
        self.run([th], operators.build(operators.lha_config), ["ToyLH"])

    def benchmark_sv(self):
        """Benckmark Scale Variation"""

        th = self.ffns_theory.copy()
        for key, item in th.items():
            th[key] = [item]
        th.update({"PTO": [1], "XIR": [0.7071067811865475, 1.4142135623730951]})
        self.run(power_set(th), operators.build(operators.lha_config), ["ToyLH"])


if __name__ == "__main__":

    zm = BenchmarkZm()
    ffns = BenchmarkFfns()
    for o in [0, 1]:
        zm.benchmark_zm(o)
        ffns.benchmark_ffns(o)

    ffns.benchmark_sv()
