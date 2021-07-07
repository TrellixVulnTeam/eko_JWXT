# -*- coding: utf-8 -*-
# Test NLO OME
import numpy as np

from eko.matching_conditions.nlo import A_ns_1, A_singlet_1

from .test_matching_nnlo import get_sx


def test_A_1_intrinsic():

    L = 100.0
    N = 2
    sx = get_sx(N)
    aS1 = A_singlet_1(N, sx, L)
    # heavy quark momentum conservation
    np.testing.assert_allclose(aS1[0, 2] + aS1[1, 2] + aS1[2, 2], 0.0, atol=1e-10)

    # gluon momentum conservation
    np.testing.assert_allclose(aS1[0, 0] + aS1[1, 0] + aS1[2, 0], 0.0)


def test_A_1_shape():

    N = 2
    L = 3.0
    sx = get_sx(N)
    aNS1i = A_ns_1(N, sx, L)
    aS1i = A_singlet_1(N, sx, L)

    assert aNS1i.shape == (2, 2)
    assert aS1i.shape == (3, 3)

    # check intrisic hh is the same
    assert aNS1i[1, 1] == aS1i[2, 2]


def test_Bluemlein_1():
    # Test against Blumlein OME implementation :cite:`Bierenbaum_2009`.
    # Only even moments are available in that code.
    # Note there is a minus sign in the definition of L.

    N_vals = 5
    ref_val_gg = {10: np.full(N_vals, -6.66667)}
    ref_val_Hg = {
        10: [6.66667, 3.66667, 2.61905, 2.05556, 1.69697],
    }

    for n in range(N_vals):
        N = 2 * n + 2
        sx = get_sx(N)
        for L in ref_val_gg:
            aS1 = A_singlet_1(N, sx, L)
            np.testing.assert_allclose(aS1[0, 0], ref_val_gg[L][n], rtol=1e-6)
            np.testing.assert_allclose(aS1[2, 0], ref_val_Hg[L][n], rtol=3e-6)
