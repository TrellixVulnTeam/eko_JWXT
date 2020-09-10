# -*- coding: utf-8 -*-
"""
    Benchmark EKO to APFEL
"""
import pickle
import yaml
import numpy as np
import pandas as pd

import eko

from .toyLH import mkPDF
from .apfel_utils import load_apfel
from .df_dict import DFdict


class ApfelBenchmark:
    """
    Benchmark EKO to APFEL

    Parameters
    ----------
        path : str
            input card
    """
    def __init__(self, path):
        with open(path, "r") as o:
            self.cfg = yaml.safe_load(o)

    def run(self):
        """
        Run APFEL
        """
        output_grid = [0.1, 0.5]
        # # compute our result
        # eko_res = eko.run_dglap(self.cfg)
        # eko_res.dump_yaml_to_file("assets/apf-fast-ops.yaml")
        eko_res = eko.output.Output.load_yaml_from_file("assets/apf-fast-ops.yaml")
        eko_pdf = eko_res.apply_pdf(mkPDF("", ""), output_grid)
        # compute APFEL reference
        apfel = load_apfel(self.cfg)
        apfel.EvolveAPFEL(self.cfg["Q0"], np.sqrt(self.cfg["Q2grid"][0]))
        apf_tabs = {}
        for q2, pdfs in eko_pdf.items():
            out = DFdict()
            for pid, eko_res in pdfs["pdfs"].items():
                # collect APFEL
                apf = []
                for x in output_grid:
                    apf.append(apfel.xPDF(pid if pid < 21 else 0, x) / x)
                apf = np.array(apf)
                # collect our data
                eko_res = np.array(eko_res)
                eko_error = np.array(pdfs["errors"][pid])
                rel_err = (apf - eko_res) / apf * 100
                out[pid] = pd.DataFrame(dict(
                    x=output_grid,
                    APFEL=apf,
                    eko=eko_res,
                    eko_error=eko_error,
                    rel_err=rel_err,
                ))
            apf_tabs[q2] = out
        # output
        self.print(apf_tabs)

    def print(self, apf_tabs):
        """
        Print all result

        Parameters
        ----------
            apf_tabs : dict
                comparison result
        """
        # iterate all values
        for q2, dfdict in apf_tabs.items():
            print("-"*20)
            print(f"Q2 = {q2} GeV^2 ")
            print("-"*20)
            print(dfdict)
            print("-"*20)
