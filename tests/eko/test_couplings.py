# -*- coding: utf-8 -*-
"""
    This module tests the implemented beta functions and the value
    of alpha_s for different orders.
"""
import numpy as np
import pytest

from eko import compatibility, thresholds
from eko.couplings import Couplings


class TestCouplings:
    def test_from_dict(self):
        theory_dict = {
            "alphas": 0.118,
            "alphaem": 0.00781,
            "Qref": 91.0,
            "nfref": None,
            "Q0": 1,
            "order": (1, 0),
            "ModEv": "EXA",
            "fact_to_ren_scale_ratio": 1.0,
            "mc": 2.0,
            "mb": 4.0,
            "mt": 175.0,
            "kcThr": 1.0,
            "kbThr": 1.0,
            "ktThr": 1.0,
            "MaxNfAs": 6,
            "HQ": "POLE",
            "ModSV": None,
        }
        sc = Couplings.from_dict(theory_dict)
        assert sc.a(theory_dict["Qref"] ** 2)[0] == theory_dict["alphas"] / (
            4.0 * np.pi
        )
        assert sc.a(theory_dict["Qref"] ** 2)[1] == theory_dict["alphaem"] / (
            4.0 * np.pi
        )

    def test_init(self):
        # prepare
        alphas_ref = 0.118
        alphaem_ref = 0.00781
        couplings_ref = np.array([alphas_ref, alphaem_ref])
        scale_ref = 91.0**2
        nf = 4
        threshold_holder = thresholds.ThresholdsAtlas.ffns(nf)
        # create
        sc = Couplings(
            couplings_ref, scale_ref, threshold_holder.area_walls[1:-1], (1.0, 1.0, 1.0)
        )
        assert sc.q2_ref == scale_ref
        assert sc.a_ref[0] == couplings_ref[0] / 4.0 / np.pi
        assert sc.a_ref[1] == couplings_ref[1] / 4.0 / np.pi
        # from theory dict
        for ModEv in ["EXP", "EXA"]:
            for PTOs in range(3 + 1):
                for PTOem in range(2 + 1):
                    setup = dict(
                        alphas=alphas_ref,
                        alphaem=alphaem_ref,
                        Qref=np.sqrt(scale_ref),
                        nfref=None,
                        order=(PTOs, PTOem),
                        ModEv=ModEv,
                        FNS="FFNS",
                        NfFF=nf,
                        Q0=2,
                        fact_to_ren_scale_ratio=1,
                        mc=2.0,
                        mb=4.0,
                        mt=175.0,
                        kcThr=1.0,
                        kbThr=1.0,
                        ktThr=1.0,
                        MaxNfAs=6,
                        HQ="POLE",
                        ModSV=None,
                    )
                    sc2 = Couplings.from_dict(setup)
                    assert sc2.q2_ref == scale_ref
                    assert sc2.a_ref[0] == couplings_ref[0] / 4.0 / np.pi
                    assert sc2.a_ref[1] == couplings_ref[1] / 4.0 / np.pi

        # errors
        with pytest.raises(ValueError):
            Couplings(
                [0, couplings_ref[1]],
                scale_ref,
                threshold_holder.area_walls[1:-1],
                (1.0, 1.0, 1.0),
            )
        with pytest.raises(ValueError):
            Couplings(
                [couplings_ref[0], 0],
                scale_ref,
                threshold_holder.area_walls[1:-1],
                (1.0, 1.0, 1.0),
            )
        with pytest.raises(ValueError):
            Couplings(
                couplings_ref, 0, threshold_holder.area_walls[1:-1], (1.0, 1.0, 1.0)
            )
        with pytest.raises(NotImplementedError):
            Couplings(
                couplings_ref,
                scale_ref,
                threshold_holder.area_walls[1:-1],
                (1.0, 1.0, 1.0),
                (6, 0),
            )
        with pytest.raises(NotImplementedError):
            Couplings(
                couplings_ref,
                scale_ref,
                threshold_holder.area_walls[1:-1],
                (1.0, 1.0, 1.0),
                (1, 3),
            )
        with pytest.raises(ValueError):
            Couplings(
                couplings_ref,
                scale_ref,
                threshold_holder.area_walls[1:-1],
                (1.0, 1.0, 1.0),
                method="ODE",
            )
        with pytest.raises(ValueError):
            Couplings.from_dict(
                dict(
                    alphas=alphas_ref,
                    alphaem=alphaem_ref,
                    Qref=np.sqrt(scale_ref),
                    nfref=None,
                    order=(1, 0),
                    ModEv="FAIL",
                ),
            )
        with pytest.raises(ValueError):
            Couplings.from_dict(
                dict(
                    alphas=alphas_ref,
                    alphaem=alphaem_ref,
                    Qref=np.sqrt(scale_ref),
                    nfref=None,
                    order=(1, 0),
                    ModEv="EXA",
                    HQ="FAIL",
                ),
            )

    def test_ref(self):
        # prepare
        thresh_setups = [
            (np.inf, np.inf, np.inf),
            (0, np.inf, np.inf),
            (2, 4, 175),
        ]
        alphas_ref = 0.118
        alphaem_ref = 0.00781
        scale_ref = 91.0**2
        for thresh_setup in thresh_setups:
            for order_s in [0, 1, 2, 3, 4]:
                for order_em in [0, 1, 2]:
                    for method in ["exact", "expanded"]:
                        # if order_em == 1 and method == "expanded" and order_s != 0:
                        #    continue
                        # create
                        sc = Couplings(
                            np.array([alphas_ref, alphaem_ref]),
                            scale_ref,
                            thresh_setup,
                            (1.0, 1.0, 1.0),
                            (order_s, order_em),
                            method,
                        )
                        np.testing.assert_approx_equal(
                            sc.a(scale_ref)[0], alphas_ref / 4.0 / np.pi
                        )
                        np.testing.assert_approx_equal(
                            sc.a(scale_ref)[1], alphaem_ref / 4.0 / np.pi
                        )

    def test_exact_LO(self):
        # prepare
        thresh_setups = [
            (np.inf, np.inf, np.inf),
            (0, np.inf, np.inf),
            (2, 4, 175),
        ]
        alphas_ref = 0.118
        alphaem_ref = 0.00781
        scale_ref = 91.0**2
        for thresh_setup in thresh_setups:
            # in LO expanded  = exact
            sc_expanded = Couplings(
                np.array([alphas_ref, alphaem_ref]),
                scale_ref,
                thresh_setup,
                (1.0, 1.0, 1.0),
                (1, 0),
                "expanded",
            )
            sc_exact = Couplings(
                np.array([alphas_ref, alphaem_ref]),
                scale_ref,
                thresh_setup,
                (1.0, 1.0, 1.0),
                (1, 0),
                "exact",
            )
            for q2 in [1, 1e1, 1e2, 1e3, 1e4]:
                np.testing.assert_allclose(
                    sc_expanded.a(q2)[0], sc_exact.a(q2)[0], rtol=5e-4
                )
                np.testing.assert_allclose(
                    sc_expanded.a(q2)[1], sc_exact.a(q2)[1], rtol=5e-4
                )

    def test_exact_LO_QED(self):
        # prepare
        thresh_setups = [
            (np.inf, np.inf, np.inf),
            (0, np.inf, np.inf),
            (2, 4, 175),
        ]
        alphas_ref = 0.118
        alphaem_ref = 0.00781
        scale_ref = 91.0**2
        for PTOs in range(1, 4 + 1):
            for thresh_setup in thresh_setups:
                # in LO expanded  = exact
                sc_expanded = Couplings(
                    np.array([alphas_ref, alphaem_ref]),
                    scale_ref,
                    thresh_setup,
                    (1.0, 1.0, 1.0),
                    (PTOs, 1),
                    "expanded",
                )
                sc_exact = Couplings(
                    np.array([alphas_ref, alphaem_ref]),
                    scale_ref,
                    thresh_setup,
                    (1.0, 1.0, 1.0),
                    (PTOs, 1),
                    "exact",
                )
                for q2 in [1e2, 1e3, 1e4]:
                    np.testing.assert_allclose(
                        sc_expanded.a(q2)[0], sc_exact.a(q2)[0], atol=1e-4
                    )
                    np.testing.assert_allclose(
                        sc_expanded.a(q2)[1], sc_exact.a(q2)[1], atol=5e-4
                    )

    def test_exact_NLO_QED(self):
        # prepare
        thresh_setups = [
            (np.inf, np.inf, np.inf),
            (0, np.inf, np.inf),
            (2, 4, 175),
        ]
        alphas_ref = 0.118
        alphaem_ref = 0.00781
        scale_ref = 91.0**2
        for thresh_setup in thresh_setups:
            # in LO expanded  = exact
            sc_expanded = Couplings(
                np.array([alphas_ref, alphaem_ref]),
                scale_ref,
                thresh_setup,
                (1.0, 1.0, 1.0),
                (0, 2),
                "expanded",
            )
            sc_exact = Couplings(
                np.array([alphas_ref, alphaem_ref]),
                scale_ref,
                thresh_setup,
                (1.0, 1.0, 1.0),
                (0, 2),
                "exact",
            )
            for q2 in [1, 1e1, 1e2, 1e3, 1e4]:
                np.testing.assert_allclose(
                    sc_expanded.a(q2)[0], sc_exact.a(q2)[0], rtol=5e-4
                )
                np.testing.assert_allclose(
                    sc_expanded.a(q2)[1], sc_exact.a(q2)[1], rtol=5e-4
                )

    def test_exact_NLO_mix(self):
        # prepare
        thresh_setups = [
            (np.inf, np.inf, np.inf),
            (0, np.inf, np.inf),
            (2, 4, 175),
        ]
        alphas_ref = 0.118
        alphaem_ref = 0.00781
        scale_ref = 91.0**2
        for thresh_setup in thresh_setups:
            # in LO expanded  = exact
            sc_expanded = Couplings(
                np.array([alphas_ref, alphaem_ref]),
                scale_ref,
                thresh_setup,
                (1.0, 1.0, 1.0),
                (2, 2),
                "expanded",
            )
            sc_exact = Couplings(
                np.array([alphas_ref, alphaem_ref]),
                scale_ref,
                thresh_setup,
                (1.0, 1.0, 1.0),
                (2, 2),
                "exact",
            )
            for q2 in [1e2, 1e3, 1e4]:
                np.testing.assert_allclose(
                    sc_expanded.a(q2)[0], sc_exact.a(q2)[0], atol=5e-4
                )
                np.testing.assert_allclose(
                    sc_expanded.a(q2)[1], sc_exact.a(q2)[1], atol=5e-4
                )

    def test_exact_N2LO_mix(self):
        # prepare
        thresh_setups = [
            (np.inf, np.inf, np.inf),
            (0, np.inf, np.inf),
            (2, 4, 175),
        ]
        alphas_ref = 0.118
        alphaem_ref = 0.00781
        scale_ref = 91.0**2
        for thresh_setup in thresh_setups:
            # in LO expanded  = exact
            sc_expanded = Couplings(
                np.array([alphas_ref, alphaem_ref]),
                scale_ref,
                thresh_setup,
                (1.0, 1.0, 1.0),
                (3, 2),
                "expanded",
            )
            sc_exact = Couplings(
                np.array([alphas_ref, alphaem_ref]),
                scale_ref,
                thresh_setup,
                (1.0, 1.0, 1.0),
                (3, 2),
                "exact",
            )
            for q2 in [1e1, 1e2, 1e3, 1e4]:
                np.testing.assert_allclose(
                    sc_expanded.a(q2)[0], sc_exact.a(q2)[0], atol=5e-4
                )
                np.testing.assert_allclose(
                    sc_expanded.a(q2)[1], sc_exact.a(q2)[1], atol=5e-4
                )

    def test_exact_N3LO_mix(self):
        # prepare
        thresh_setups = [
            (np.inf, np.inf, np.inf),
            (0, np.inf, np.inf),
            (2, 4, 175),
        ]
        alphas_ref = 0.118
        alphaem_ref = 0.00781
        scale_ref = 91.0**2
        for thresh_setup in thresh_setups:
            # in LO expanded  = exact
            sc_expanded = Couplings(
                np.array([alphas_ref, alphaem_ref]),
                scale_ref,
                thresh_setup,
                (1.0, 1.0, 1.0),
                (4, 2),
                "expanded",
            )
            sc_exact = Couplings(
                np.array([alphas_ref, alphaem_ref]),
                scale_ref,
                thresh_setup,
                (1.0, 1.0, 1.0),
                (4, 2),
                "exact",
            )
            for q2 in [1e1, 1e2, 1e3, 1e4]:
                np.testing.assert_allclose(
                    sc_expanded.a(q2)[0], sc_exact.a(q2)[0], atol=5e-3
                )
                np.testing.assert_allclose(
                    sc_expanded.a(q2)[1], sc_exact.a(q2)[1], atol=5e-4
                )

    def benchmark_expanded_n3lo(self):
        """test N3LO - NNLO expansion with some reference value from Mathematica"""
        Q2 = 100**2
        # use a big alpha_s to enlarge the difference
        alphas_ref = 0.9
        alphaem_ref = 0.00781
        scale_ref = 90**2
        m2c = 2
        m2b = 25
        m2t = 30625
        threshold_list = [m2c, m2b, m2t]
        mathematica_val = -0.000169117
        # collect my values
        as_NNLO = Couplings(
            np.array([alphas_ref, alphaem_ref]),
            scale_ref,
            threshold_list,
            (1.0, 1.0, 1.0),
            order=(3, 0),
            method="expanded",
        )
        as_N3LO = Couplings(
            np.array([alphas_ref, alphaem_ref]),
            scale_ref,
            threshold_list,
            (1.0, 1.0, 1.0),
            order=(4, 0),
            method="expanded",
        )
        np.testing.assert_allclose(
            mathematica_val, as_N3LO.a(Q2)[0] - as_NNLO.a(Q2)[0], rtol=3e-6
        )
