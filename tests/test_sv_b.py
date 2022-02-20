# -*- coding: utf-8 -*-

import numpy as np

from eko.anomalous_dimensions import gamma_ns, gamma_singlet
from eko.beta import beta_0
from eko.kernels import non_singlet, singlet
from eko.scale_variations import a, b


def test_ns_sv_dispacher():
    """Test to identity"""
    order = 2
    gamma_ns = np.random.rand(order + 1)
    L = 0
    nf = 5
    a_s = 0.35
    np.testing.assert_allclose(
        b.non_singlet_variation(gamma_ns, a_s, order, nf, L), 1.0
    )


def test_singlet_sv_dispacher():
    """Test to identity"""
    order = 2
    gamma_singlet = np.random.rand(order + 1, 2, 2)
    L = 0
    nf = 5
    a_s = 0.35
    np.testing.assert_allclose(
        b.singlet_variation(gamma_singlet, a_s, order, nf, L), np.eye(2)
    )


def test_scale_variation_a_vs_b():
    r"""
    Test sv_scheme A kernel vs sv_scheme B.
    We test that the quantity :math:`(ker_A - ker_B)/ker_{unv}` depends
    only on the accuracy in the :math:`\alpha_s` expansion
    and not in the size of the `fact_to_ren` itself.
    However in our implementation the sv_scheme A depends on
    the actual value of a0 and a1, since the evolution integral in :math:`\alpha_s`
    is evaluated. Thus this test ratio :math:`(ker_A - ker_B)/ker_{unv}`
    still contains a dependency on `fact_to_ren`.
    """
    nf = 5
    n = 10
    a1 = 0.118 / (4 * np.pi)
    a0 = 0.2 / (4 * np.pi)
    method = "truncated"

    def scheme_diff(g, k, pto, is_singlet):
        """
        :math:`(ker_A - ker_B)/ker_{unv}` for truncated expansion
        Effects due to non commutativity are neglected thus,
        he accuracy of singlet quantities is slightly worst.
        """
        if pto >= 1:
            diff = g[0] * k * a0
        if pto >= 2:
            b0 = beta_0(nf)
            g02 = g[0] @ g[0] if is_singlet else g[0] ** 2
            diff += a0**2 * g[1] * k - k**2 * (
                1 / 2 * a0**2 * b0 * g[0] + a1 * a0 * g02 - 1 / 2 * a0**2 * g02
            )
        return diff

    for L in [np.log(0.5), np.log(2)]:
        for order in [1, 2]:
            # Non singlet kernels
            gns = gamma_ns(order, 4, n, nf)
            ker = non_singlet.dispatcher(
                order, method, gns, a1, a0, nf, ev_op_iterations=1
            )
            gns_a = a.gamma_variation(gns.copy(), order, nf, L)
            ker_a = non_singlet.dispatcher(
                order, method, gns_a, a1, a0, nf, ev_op_iterations=1
            )
            ker_b = ker * b.non_singlet_variation(gns, a1, order, nf, L)
            ns_diff = scheme_diff(gns, L, order, False)
            np.testing.assert_allclose((ker_a - ker_b) / ker, ns_diff, atol=1e-3)

            # Singlet kernels
            gs = gamma_singlet(order, n, nf)
            ker = singlet.dispatcher(
                order, method, gs, a1, a0, nf, ev_op_iterations=1, ev_op_max_order=1
            )
            gs_a = a.gamma_variation(gs.copy(), order, nf, L)
            ker_a = singlet.dispatcher(
                order, method, gs_a, a1, a0, nf, ev_op_iterations=1, ev_op_max_order=1
            )
            ker_b = ker @ b.singlet_variation(gs, a1, order, nf, L)
            s_diff = scheme_diff(gs, L, order, True)
            np.testing.assert_allclose(
                (ker_a - ker_b) @ np.linalg.inv(ker), s_diff, atol=5e-3
            )
