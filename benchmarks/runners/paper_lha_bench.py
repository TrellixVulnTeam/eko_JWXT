# -*- coding: utf-8 -*-
"""
Benchmark to :cite:`Giele:2002hx` and  :cite:`Dittmar:2005ed` (NNLO)
"""
import numpy as np

from ekomark.benchmark.runner import Runner

base_theory = {
    "ModEv": "EXA",
    "Q0": np.sqrt(2.0),  # Eq. (30), Eq. (4.53) NNLO
    "mc": np.sqrt(2.0),  # Eq. (34), Eq. (4.56) NNLO
    "mb": 4.5,
    "mt": 175,
    "Qref": np.sqrt(2.0),  # Eq. (32),Eq. (4.53) NNLO
    "alphas": 0.35,  # Eq. (4.55) NNLO
}
"""Global theory settings"""


class LHABenchmark(Runner):
    """
    Globally set the external program to LHA
    """

    external = "LHA"

    theory = {}

    rotate_to_evolution_basis = True

    skip_pdfs = [22, -6, 6, "ph", "V35", "V24", "V15", "V8", "T35"]

    is_FFNS = False

    def plain_theory(self, pto):
        """
        Plain theories at given PTO.

        Parameters
        ----------
            pto : int
                perturbation order

        Returns
        -------
            list(dict)
                theory updates
        """
        th = self.theory.copy()
        th.update({"PTO": pto})
        return [th]

    def sv_theories(self, pto):
        """
        Scale variation theories.

        Parameters
        ----------
            pto : int
                perturbation order

        Returns
        -------
            list(dict)
                theory updates
        """
        low = self.theory.copy()
        low["PTO"] = pto
        low["XIR"] = np.sqrt(1.0 / 2.0)
        high = self.theory.copy()
        high["PTO"] = pto
        high["XIR"] = np.sqrt(2.0)
        return [low, high]

    def run_lha(self, theory_updates):
        """
        Enforce operators and PDF

        Parameters
        ----------
            theory_updates : list(dict)
                theory updates
        """
        self.run(theory_updates, [{"Q2grid": [1e4],}], ["ToyLH"])

    def benchmark_plain(self, pto):
        """Plain configuration"""
        if pto == 2 and self.is_FFNS:
            self.ffns_nnlo_pdfs()
        self.run_lha(self.plain_theory(pto))

    def benchmark_sv(self):
        """Scale variations"""
        for pto in [1,2]:
            if pto == 2 and self.is_FFNS:
                self.ffns_nnlo_pdfs()
            self.run_lha(self.sv_theories(pto))


class BenchmarkVFNS(LHABenchmark):
    """Variable Flavor Number Scheme"""

    theory = base_theory.copy()
    theory.update(
        {
            "FNS": "ZM-VFNS",  # ignored by eko, but needed by LHA_utils
            "kcThr": 1.0,
            "kbThr": 1.0,
            "ktThr": 1.0,
        }
    )


class BenchmarkFFNS(LHABenchmark):
    """Fixed Flavor Number Scheme"""

    theory = base_theory.copy()
    theory.update(
        {
            "FNS": "FFNS",  # ignored by eko, but needed by LHA_utils
            "NfFF": 4,
            "kcThr": 0.0,
            "kbThr": np.inf,
            "ktThr": np.inf,
        }
    )
    is_FFNS = True

    def ffns_nnlo_pdfs(self):
        """
        Set different pdfs set for NNLO FFNS
        """
        self.skip_pdfs.extend([-5, 5, "T24"])
        if "V8" in self.skip_pdfs:
            self.skip_pdfs.remove("V8")


if __name__ == "__main__":

    vfns = BenchmarkVFNS()
    vfns.benchmark_plain(2)
    vfns.benchmark_sv()

    ffns = BenchmarkFFNS()
    ffns.benchmark_plain(2)
    ffns = BenchmarkFFNS()
    ffns.benchmark_sv()
