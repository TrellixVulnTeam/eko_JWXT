# -*- coding: utf-8 -*-

import numpy as np
import scipy.integrate

from eko.operator import Operator, gamma_ns_fact, gamma_singlet_fact, quad_ker
from eko.operator.grid import OperatorGrid
from eko.thresholds import ThresholdsAtlas
from eko.strong_coupling import StrongCoupling
from eko.interpolation import InterpolatorDispatcher
from eko import anomalous_dimensions as ad
from eko.kernels import non_singlet as ns
from eko.kernels import singlet as s
from eko import mellin
from eko import interpolation


def test_gamma_ns_fact(monkeypatch):
    gamma_ns = np.array([1.0, 0.5, 0.25])
    monkeypatch.setattr(ad, "gamma_ns", lambda *args: gamma_ns.copy())
    gamma_ns_LO_0 = gamma_ns_fact(0, "NS_p", 1, 3, 0)
    np.testing.assert_allclose(gamma_ns_LO_0, gamma_ns)
    gamma_ns_LO_1 = gamma_ns_fact(0, "NS_p", 1, 3, 1)
    np.testing.assert_allclose(gamma_ns_LO_1, gamma_ns)
    gamma_ns_NLO_1 = gamma_ns_fact(1, "NS_p", 1, 3, 1)
    assert gamma_ns_NLO_1[1] < gamma_ns[1]
    gamma_ns_NNLO_1 = gamma_ns_fact(2, "NS_p", 1, 3, 1)
    assert gamma_ns_NNLO_1[2] - gamma_ns[2] == 8.0


def test_gamma_singlet_fact(monkeypatch):
    gamma_s = np.array([1.0, 0.5, 0.25])
    monkeypatch.setattr(ad, "gamma_singlet", lambda *args: gamma_s.copy())
    gamma_s_LO_0 = gamma_singlet_fact(0, 1, 3, 0)
    np.testing.assert_allclose(gamma_s_LO_0, gamma_s)
    gamma_s_LO_1 = gamma_singlet_fact(0, 1, 3, 1)
    np.testing.assert_allclose(gamma_s_LO_1, gamma_s)
    gamma_s_NLO_1 = gamma_singlet_fact(1, 1, 3, 1)
    assert gamma_s_NLO_1[1] < gamma_s[1]
    gamma_s_NNLO_1 = gamma_singlet_fact(2, 1, 3, 1)
    assert gamma_s_NNLO_1[2] - gamma_s[2] == 8.0


def test_quad_ker(monkeypatch):
    monkeypatch.setattr(
        mellin, "Talbot_path", lambda *args: 2
    )  # N=2 is a safe evaluation point
    monkeypatch.setattr(
        mellin, "Talbot_jac", lambda *args: complex(0, np.pi)
    )  # negate mellin prefactor
    monkeypatch.setattr(interpolation, "log_evaluate_Nx", lambda *args: 1)
    monkeypatch.setattr(interpolation, "evaluate_Nx", lambda *args: 1)
    monkeypatch.setattr(ns, "dispatcher", lambda *args: 1.0)
    monkeypatch.setattr(s, "dispatcher", lambda *args: np.identity(2))
    for is_log in [True, False]:
        res_ns = quad_ker(
            u=0,
            order=0,
            mode="NS_p",
            method="",
            is_log=is_log,
            logx=0.0,
            areas=np.zeros(3),
            a1=1,
            a0=2,
            nf=3,
            L=0,
            ev_op_iterations=0,
            ev_op_max_order=0,
        )
        np.testing.assert_allclose(res_ns, 1.0)
        res_s = quad_ker(
            u=0,
            order=0,
            mode="S_qq",
            method="",
            is_log=is_log,
            logx=0.0,
            areas=np.zeros(3),
            a1=1,
            a0=2,
            nf=3,
            L=0,
            ev_op_iterations=0,
            ev_op_max_order=0,
        )
        np.testing.assert_allclose(res_s, 1.0)
        res_s = quad_ker(
            u=0,
            order=0,
            mode="S_qg",
            method="",
            is_log=is_log,
            logx=0.0,
            areas=np.zeros(3),
            a1=1,
            a0=2,
            nf=3,
            L=0,
            ev_op_iterations=0,
            ev_op_max_order=0,
        )
        np.testing.assert_allclose(res_s, 0.0)
    monkeypatch.setattr(interpolation, "log_evaluate_Nx", lambda *args: 0)
    res_ns = quad_ker(
        u=0,
        order=0,
        mode="NS_p",
        method="",
        is_log=True,
        logx=0.0,
        areas=np.zeros(3),
        a1=1,
        a0=2,
        nf=3,
        L=0,
        ev_op_iterations=0,
        ev_op_max_order=0,
    )
    np.testing.assert_allclose(res_ns, 0.0)


class TestOperator:
    def test_labels(self):
        o = Operator(
            dict(order=2, debug_skip_non_singlet=False, debug_skip_singlet=False),
            {},
            3,
            1,
            2,
        )
        assert sorted(o.labels()) == sorted(
            ["NS_p", "NS_m", "NS_v", "S_qq", "S_qg", "S_gq", "S_gg"]
        )
        o = Operator(
            dict(order=1, debug_skip_non_singlet=True, debug_skip_singlet=True),
            {},
            3,
            1,
            2,
        )
        assert sorted(o.labels()) == []

    def test_compute(self, monkeypatch):
        # setup objs
        theory_card = {
            "alphas": 0.35,
            "PTO": 0,
            "ModEv": "TRN",
            "fact_to_ren_scale_ratio": 1.0,
            "Qref": np.sqrt(2),
            "Q0": np.sqrt(2),
            "FNS": "FFNS",
            "NfFF": 3,
            "IC": 0,
            "mc": 1.0,
            "mb": 4.75,
            "mt": 173.0,
            "kcThr": np.inf,
            "kbThr": np.inf,
            "ktThr": np.inf,
            "MaxNfPdf": 6,
            "MaxNfAs": 6,
        }
        operators_card = {
            "Q2grid": [1, 10],
            "interpolation_xgrid": [0.1, 1.0],
            "interpolation_polynomial_degree": 1,
            "interpolation_is_log": True,
            "debug_skip_singlet": True,
            "debug_skip_non_singlet": False,
            "ev_op_max_order": 1,
            "ev_op_iterations": 1,
            "backward_inversion": "exact",
        }
        g = OperatorGrid.from_dict(
            theory_card,
            operators_card,
            ThresholdsAtlas.from_dict(theory_card),
            StrongCoupling.from_dict(theory_card),
            InterpolatorDispatcher.from_dict(operators_card),
        )
        o = Operator(g.config, g.managers, 3, 2, 10)
        # fake quad
        monkeypatch.setattr(
            scipy.integrate, "quad", lambda *args, **kwargs: np.random.rand(2)
        )
        # LO
        o.compute()
        assert "NS_m" in o.op_members
        np.testing.assert_allclose(
            o.op_members["NS_m"].value, o.op_members["NS_p"].value
        )
        np.testing.assert_allclose(
            o.op_members["NS_v"].value, o.op_members["NS_p"].value
        )
        # NLO
        o.config["order"] = 1
        o.compute()
        assert not np.allclose(o.op_members["NS_p"].value, o.op_members["NS_m"].value)
        np.testing.assert_allclose(
            o.op_members["NS_v"].value, o.op_members["NS_m"].value
        )


def test_pegasus_path():
    def quad_ker_pegasus(
        u, order, mode, method, logx, areas, a1, a0, nf, L, ev_op_iterations
    ):
        # compute the mellin inversion as done in pegasus
        phi = 3 / 4 * np.pi
        c = 1.9
        n = complex(c + u * np.exp(1j * phi))
        gamma_ns = gamma_ns_fact(order, mode, n, nf, L)
        ker = ns.dispatcher(
            order,
            method,
            gamma_ns,
            a1,
            a0,
            nf,
            ev_op_iterations,
        )
        pj = interpolation.log_evaluate_Nx(n, logx, areas)
        return np.imag(np.exp(1j * phi) / np.pi * pj * ker)

    # It might be useful to test with a different fuction
    # monkeypatch.setattr(ns, "dispatcher", lambda x, *args: np.exp( - x ** 2 ) )
    xgrid = np.geomspace(1e-7, 1, 10)
    int_disp = InterpolatorDispatcher(xgrid, 1, True)
    order = 1
    mode = "NS_p"
    method = ""
    logxs = np.log(int_disp.xgrid_raw)
    a1 = 1
    a0 = 2
    nf = 3
    L = 0
    ev_op_iterations = 10
    for logx in logxs:
        for bf in int_disp:
            res_ns, _ = scipy.integrate.quad(
                quad_ker,
                0.5,
                1.0,
                args=(
                    order,
                    mode,
                    method,
                    int_disp.log,
                    logx,
                    bf.areas_representation,
                    a1,
                    a0,
                    nf,
                    L,
                    ev_op_iterations,
                    10,
                ),
                epsabs=1e-12,
                epsrel=1e-5,
                limit=100,
                full_output=1,
            )[:2]

            res_test, _ = scipy.integrate.quad(
                quad_ker_pegasus,
                0,
                np.inf,
                args=(
                    order,
                    mode,
                    method,
                    logx,
                    bf.areas_representation,
                    a1,
                    a0,
                    nf,
                    L,
                    ev_op_iterations,
                ),
                epsabs=1e-12,
                epsrel=1e-5,
                limit=100,
                full_output=1,
            )[:2]

            np.testing.assert_allclose(res_ns, res_test, rtol=2e-6)
