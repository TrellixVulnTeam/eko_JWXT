# -*- coding: utf-8 -*-
"""This module benchmarks MSbar mass evolution against APFEL."""
import copy

import numpy as np
import pytest

from eko import compatibility, msbar_masses
from eko.basis_rotation import quark_names
from eko.couplings import Couplings

# try to load APFEL - if not available, we'll use the cached values
try:
    import apfel

    use_APFEL = True
except ImportError:
    use_APFEL = False

theory_dict = {
    "alphas": 0.1180,
    "alphaqed": 0.007496,
    "Qref": 91,
    "nfref": 5,
    "MaxNfPdf": 6,
    "MaxNfAs": 6,
    "Q0": 1,
    "fact_to_ren_scale_ratio": 1.0,
    "mc": 1.5,
    "mb": 4.1,
    "mt": 175.0,
    "kcThr": 1.0,
    "kbThr": 1.0,
    "ktThr": 1.0,
    "HQ": "MSBAR",
    "Qmc": 18,
    "Qmb": 20,
    "Qmt": 175.0,
    "PTO": 2,
    "QED": 0,
    "ModEv": "EXA",
}


@pytest.mark.isolated
class BenchmarkMSbar:
    def benchmark_APFEL_msbar_evolution(self):
        theory = compatibility.update_theory(theory_dict)
        bench_values = dict(zip(np.power([1, 96, 150], 2), [3, 5, 5]))
        theory.update(
            {
                "mc": 1.4,
                "mb": 4.5,
                "mt": 175.0,
                "Qmc": 2.0,
                "Qmb": 4.5,
                "Qmt": 175.0,
            }
        )
        apfel_vals_dict = {
            "exact": {
                1: np.array(
                    [
                        [1.6046128320144937, 5.82462147889985, 319.1659462836651],
                        [0.9184216270407894, 3.3338000474743867, 182.67890037277968],
                        [0.8892735505271812, 3.2279947658871553, 176.88119438599423],
                    ]
                ),
                2: np.array(
                    [
                        [1.7606365126844892, 6.707425163030458, 392.9890591164956],
                        [0.8227578662769597, 3.134427109507681, 183.6465604399247],
                        [0.7934449726444709, 3.0227549733595973, 177.10367302092334],
                    ]
                ),
                3: np.array(
                    [
                        [1.8315619347807859, 7.058348563796064, 416.630860855048],
                        [0.8078493428925942, 3.113242546931765, 183.76436225206226],
                        [0.7788276351007536, 3.0014003869088755, 177.16269119698978],
                    ]
                ),
            },
            "expanded": {
                1: np.array(
                    [
                        [1.6046128320144941, 5.824621478899853, 319.1659462836651],
                        [0.9184216270407891, 3.3338000474743863, 182.67890037277968],
                        [0.8892735505271808, 3.227994765887154, 176.88119438599423],
                    ]
                ),
                2: np.array(
                    [
                        [1.7533055503995305, 6.672122790503439, 390.2255025944903],
                        [0.8251533585949282, 3.1400827586994855, 183.65075271254497],
                        [0.7957427000040153, 3.028161864236207, 177.104951823859],
                    ]
                ),
                3: np.array(
                    [
                        [1.8268480938423455, 7.037891257825139, 415.2638988980831],
                        [0.8084237419306857, 3.1144420987483485, 183.76461377981423],
                        [0.7793806824526442, 3.002554084550691, 177.16277079680097],
                    ]
                ),
            },
        }
        # collect my values
        for method in ["exact", "expanded"]:
            theory["ModEv"] = "EXP" if method == "expanded" else "EXA"
            for order in [1, 2, 3]:
                theory["order"] = (order, 0)
                as_VFNS = Couplings(
                    np.array([theory["alphas"], theory["alphaem"]]),
                    theory["Qref"] ** 2,
                    msbar_masses.compute(theory),
                    np.power([theory["kcThr"], theory["kbThr"], theory["ktThr"]], 2),
                    order=theory["order"],
                    method=method,
                    nf_ref=theory["nfref"],
                    hqm_scheme=theory["HQ"],
                )
                my_vals = []
                for Q2, nf_to in bench_values.items():
                    my_masses = []
                    for n in [3, 4, 5]:
                        my_masses.append(
                            msbar_masses.evolve(
                                theory[f"m{quark_names[n]}"] ** 2,
                                theory[f"Qm{quark_names[n]}"] ** 2,
                                strong_coupling=as_VFNS,
                                fact_to_ren=1.0,
                                q2_to=Q2,
                                nf_ref=n,
                                nf_to=nf_to,
                            )
                        )
                    my_vals.append(my_masses)
                # get APFEL numbers - if available else use cache
                apfel_vals = apfel_vals_dict[method][order]
                if use_APFEL:
                    # run apfel
                    apfel.CleanUp()
                    apfel.SetTheory("QCD")
                    apfel.SetPerturbativeOrder(order - 1)
                    apfel.SetAlphaEvolution(method)
                    apfel.SetAlphaQCDRef(theory["alphas"], theory["Qref"])
                    apfel.SetVFNS()
                    apfel.SetMSbarMasses(theory["mc"], theory["mb"], theory["mt"])
                    apfel.SetMassScaleReference(
                        theory["Qmc"], theory["Qmb"], theory["Qmt"]
                    )
                    apfel.SetRenFacRatio(1.0)
                    apfel.InitializeAPFEL()
                    # collect apfel masses
                    apfel_vals_cur = []
                    for Q2 in bench_values:
                        masses = []
                        for n in [4, 5, 6]:
                            masses.append(apfel.HeavyQuarkMass(n, np.sqrt(Q2)))
                        apfel_vals_cur.append(masses)
                    print(apfel_vals_cur)
                    np.testing.assert_allclose(
                        apfel_vals,
                        np.array(apfel_vals_cur),
                        err_msg=f"order={order - 1}",
                    )
                # check myself to APFEL
                np.testing.assert_allclose(
                    apfel_vals, np.sqrt(np.array(my_vals)), rtol=2.3e-3
                )

    def benchmark_APFEL_msbar_solution(self):
        apfel_vals_dict = {
            "EXA": {
                1: np.array(
                    [1.9855, 4.8062, 175.0000],
                ),
                2: np.array(
                    [2.1308, 4.9656, 175.0000],
                ),
                3: np.array([2.1566, 4.9841, 175.0000]),
            },
        }
        # collect my values
        theory = compatibility.update_theory(theory_dict)
        for order in [1, 2, 3]:
            theory["order"] = (order, 0)
            my_masses = msbar_masses.compute(theory)
            # get APFEL numbers - if available else use cache
            apfel_vals = apfel_vals_dict[theory_dict["ModEv"]][order]
            if use_APFEL:
                # run apfel
                apfel.CleanUp()
                apfel.SetTheory("QCD")
                apfel.SetPerturbativeOrder(order - 1)
                apfel.SetAlphaEvolution("exact")
                apfel.SetAlphaQCDRef(theory_dict["alphas"], theory_dict["Qref"])
                apfel.SetVFNS()
                apfel.SetMSbarMasses(
                    theory_dict["mc"], theory_dict["mb"], theory_dict["mt"]
                )
                apfel.SetMassScaleReference(
                    theory_dict["Qmc"], theory_dict["Qmb"], theory_dict["Qmt"]
                )
                apfel.SetRenFacRatio(theory_dict["fact_to_ren_scale_ratio"])
                apfel.InitializeAPFEL()
            # check myself to APFEL
            np.testing.assert_allclose(
                apfel_vals, np.sqrt(np.array(my_masses)), rtol=4e-4
            )

    def benchmark_msbar_solution_kthr(self):
        """
        With this test you can see that in EKO
        the solution value of mb is not affected by "kbThr",
        since mb is searched with an Nf=5 larger range.
        While in Apfel this doesn't happen.
        """
        theory_dict.update(
            {
                "mc": 1.5,
                "mb": 4.1,
                "mt": 175.0,
                "kcThr": 1.2,
                "kbThr": 1.8,
                "ktThr": 1.0,
                "Qmc": 18,
                "Qmb": 20,
                "Qmt": 175.0,
                "PTO": 0,
            }
        )
        theory = compatibility.update_theory(theory_dict)
        my_masses_thr = msbar_masses.compute(theory)
        apfel_masses_thr = [1.9891, 4.5102, 175.0000]
        theory.update(
            {
                "kcThr": 1.0,
                "kbThr": 1.0,
            }
        )
        my_masses_plain = msbar_masses.compute(theory)
        apfel_masses_plain = ([1.9855, 4.8062, 175.0000],)

        # Eko bottom mass is the same
        np.testing.assert_allclose(my_masses_thr[1], my_masses_plain[1])
        # Eko charm mass is not the same
        np.testing.assert_raises(
            AssertionError,
            np.testing.assert_allclose,
            my_masses_thr[0],
            my_masses_plain[0],
        )

        # Apfel bottom masses are not the same
        np.testing.assert_raises(
            AssertionError,
            np.testing.assert_allclose,
            apfel_masses_thr[0],
            apfel_masses_plain[0],
        )
        np.testing.assert_raises(
            AssertionError,
            np.testing.assert_allclose,
            apfel_masses_thr[0],
            apfel_masses_plain[0],
        )
