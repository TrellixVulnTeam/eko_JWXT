# -*- coding: utf-8 -*-
import warnings

import numpy as np
import pytest

from eko import anomalous_dimensions as ad
from eko import beta
from eko.kernels import non_singlet as ns

methods = [
    "iterate-expanded",
    "decompose-expanded",
    "perturbative-expanded",
    "truncated",
    "ordered-truncated",
    "iterate-exact",
    "decompose-exact",
    "perturbative-exact",
]


def test_zero():
    """No evolution results in exp(0)"""
    nf = 3
    ev_op_iterations = 2
    gamma_ns = np.array([1 + 0.0j, 1 + 0j, 1 + 0j, 1 + 0j])
    for order in [1, 2, 3, 4]:
        for method in methods:
            np.testing.assert_allclose(
                ns.dispatcher(
                    (order, 0), method, gamma_ns, 1.0, 1.0, nf, ev_op_iterations
                ),
                1.0,
            )
            np.testing.assert_allclose(
                ns.dispatcher(
                    (order, 0),
                    method,
                    np.zeros(order + 1, dtype=complex),
                    2.0,
                    1.0,
                    nf,
                    ev_op_iterations,
                ),
                1.0,
            )


def test_ode_lo():
    nf = 3
    ev_op_iterations = 10
    gamma_ns = np.random.rand(1) + 0j
    delta_a = -1e-6
    a0 = 0.3
    for a1 in [0.1, 0.2]:
        r = a1 * gamma_ns / (beta.beta_qcd((2, 0), nf) * a1**2)
        for method in methods:
            rhs = r * ns.dispatcher(
                (1, 0), method, gamma_ns, a1, a0, nf, ev_op_iterations
            )
            lhs = (
                ns.dispatcher(
                    (1, 0),
                    method,
                    gamma_ns,
                    a1 + 0.5 * delta_a,
                    a0,
                    nf,
                    ev_op_iterations,
                )
                - ns.dispatcher(
                    (1, 0),
                    method,
                    gamma_ns,
                    a1 - 0.5 * delta_a,
                    a0,
                    nf,
                    ev_op_iterations,
                )
            ) / delta_a
            np.testing.assert_allclose(lhs, rhs, atol=np.abs(delta_a))


def test_ode_nlo():
    nf = 3
    ev_op_iterations = 10
    gamma_ns = np.random.rand(2) + 0j
    delta_a = -1e-6
    a0 = 0.3
    for a1 in [0.1, 0.2]:
        r = (a1 * gamma_ns[0] + a1**2 * gamma_ns[1]) / (
            beta.beta_qcd((2, 0), nf) * a1**2 + beta.beta_qcd((3, 0), nf) * a1**3
        )
        for method in ["iterate-exact"]:
            rhs = r * ns.dispatcher(
                (2, 0), method, gamma_ns, a1, a0, nf, ev_op_iterations
            )
            lhs = (
                ns.dispatcher(
                    (2, 0),
                    method,
                    gamma_ns,
                    a1 + 0.5 * delta_a,
                    a0,
                    nf,
                    ev_op_iterations,
                )
                - ns.dispatcher(
                    (2, 0),
                    method,
                    gamma_ns,
                    a1 - 0.5 * delta_a,
                    a0,
                    nf,
                    ev_op_iterations,
                )
            ) / delta_a
            np.testing.assert_allclose(lhs, rhs, atol=np.abs(delta_a))


def test_ode_nnlo():
    nf = 3
    ev_op_iterations = 10
    gamma_ns = np.random.rand(3) + 0j
    delta_a = -1e-6
    a0 = 0.3
    for a1 in [0.1, 0.2]:
        r = (gamma_ns[0] + a1 * gamma_ns[1] + a1**2 * gamma_ns[2]) / (
            beta.beta_qcd((2, 0), nf) * a1
            + beta.beta_qcd((3, 0), nf) * a1**2
            + beta.beta_qcd((4, 0), nf) * a1**3
        )
        for method in ["iterate-exact"]:
            rhs = r * ns.dispatcher(
                (3, 0), method, gamma_ns, a1, a0, nf, ev_op_iterations
            )
            lhs = (
                ns.dispatcher(
                    (3, 0),
                    method,
                    gamma_ns,
                    a1 + 0.5 * delta_a,
                    a0,
                    nf,
                    ev_op_iterations,
                )
                - ns.dispatcher(
                    (3, 0),
                    method,
                    gamma_ns,
                    a1 - 0.5 * delta_a,
                    a0,
                    nf,
                    ev_op_iterations,
                )
            ) / delta_a
            np.testing.assert_allclose(lhs, rhs)


def test_ode_n3lo():
    nf = 3
    ev_op_iterations = 10
    gamma_ns = np.random.rand(4) + 0j
    delta_a = -1e-6
    a0 = 0.3
    for a1 in [0.1, 0.2]:
        r = (
            gamma_ns[0]
            + a1 * gamma_ns[1]
            + a1**2 * gamma_ns[2]
            + a1**3 * gamma_ns[3]
        ) / (
            beta.beta_qcd((2, 0), nf) * a1
            + beta.beta_qcd((3, 0), nf) * a1**2
            + beta.beta_qcd((4, 0), nf) * a1**3
            + beta.beta_qcd((5, 0), nf) * a1**4
        )
        for method in ["iterate-exact"]:
            rhs = r * ns.dispatcher(
                (4, 0), method, gamma_ns, a1, a0, nf, ev_op_iterations
            )
            lhs = (
                ns.dispatcher(
                    (4, 0),
                    method,
                    gamma_ns,
                    a1 + 0.5 * delta_a,
                    a0,
                    nf,
                    ev_op_iterations,
                )
                - ns.dispatcher(
                    (4, 0),
                    method,
                    gamma_ns,
                    a1 - 0.5 * delta_a,
                    a0,
                    nf,
                    ev_op_iterations,
                )
            ) / delta_a
            np.testing.assert_allclose(lhs, rhs)


def test_error():
    with pytest.raises(NotImplementedError):
        ns.dispatcher((5, 0), "iterate-exact", np.random.rand(3) + 0j, 0.2, 0.1, 3, 10)
    with pytest.raises(NotImplementedError):
        ad.gamma_ns((2, 0), 10202, 1, 3)


def test_gamma_usage():
    a1 = 0.1
    a0 = 0.3
    nf = 3
    ev_op_iterations = 10
    # first check that at order=n only uses the matrices up n
    gamma_ns = np.full(4, np.nan)
    for order in range(1, 5):
        gamma_ns[order - 1] = np.random.rand()
        for method in methods:
            r = ns.dispatcher(
                (order, 0), method, gamma_ns, a1, a0, nf, ev_op_iterations
            )
            assert not np.isnan(r)
    # second check that at order=n the actual matrix n is used
    for order in range(1, 5):
        gamma_ns = np.random.rand(order)
        gamma_ns[order - 1] = np.nan
        for method in methods:
            if method == "ordered-truncated":
                # we are actually dividing by a np.nan,
                # since the sum of U vec is nan
                warnings.simplefilter("ignore", RuntimeWarning)
            r = ns.dispatcher(
                (order, 0), method, gamma_ns, a1, a0, nf, ev_op_iterations
            )
            assert np.isnan(r)
