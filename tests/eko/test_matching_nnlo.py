# -*- coding: utf-8 -*-
# Test NNLO OME

import numpy as np

from eko.harmonics import compute_cache, constants
from eko.matching_conditions.as2 import A_ns, A_qq_ns, A_singlet


def test_A_2():
    logs = [0, 100]

    for L in logs:
        N = 1
        sx = compute_cache(N, 3, False)
        aNSqq2 = A_qq_ns(N, sx, L)
        # quark number conservation
        np.testing.assert_allclose(aNSqq2, 0.0, atol=2e-11)

        N = 2
        sx = compute_cache(N, 3, True)
        aS2 = A_singlet(N, sx, L)

        # gluon momentum conservation
        np.testing.assert_allclose(aS2[0, 0] + aS2[1, 0] + aS2[2, 0], 0.0, atol=2e-6)
        # quark momentum conservation
        np.testing.assert_allclose(aS2[0, 1] + aS2[1, 1] + aS2[2, 1], 0.0, atol=1e-11)

    aNS2 = A_ns(N, sx, L)
    assert aNS2.shape == (2, 2)
    assert aS2.shape == (3, 3)

    np.testing.assert_allclose(aS2[1, 0], 0)
    np.testing.assert_allclose(aS2[:, 2], np.zeros(3))
    np.testing.assert_allclose(aNS2[1, 1], 0)


def test_A_2_shape():
    N = np.random.rand()
    L = 3
    sx = compute_cache(N, 3, (-1) ** N == 1)
    aNS2 = A_ns(N, sx, L)
    aS2 = A_singlet(N, sx, L)

    assert aNS2.shape == (2, 2)
    assert aS2.shape == (3, 3)

    # check q line equal to the h line for non intrinsic
    assert aS2[1].all() == aS2[2].all()
    assert aNS2[0].all() == aNS2[1].all()


def test_pegasus_sign():
    # reference value come from Pegasus code transalted Mathematica
    ref_val = -21133.9
    N = 2
    sx = compute_cache(N, 3, True)
    L = 100.0
    aS2 = A_singlet(N, sx, L)

    np.testing.assert_allclose(aS2[0, 0], ref_val, rtol=4e-5)


def test_Blumlein_2():
    # Test against Blumlein OME implementation :cite:`Bierenbaum:2009zt`.
    # For singlet OME only even moments are available in that code.
    # Note there is a minus sign in the definition of L.
    ref_val_gg = {
        0: [-9.96091, -30.0093, -36.5914, -40.6765, -43.6823],
        10: [-289.097, -617.811, -739.687, -820.771, -882.573],
    }
    ref_val_gq = {
        0: [
            5.82716,
            1.34435,
            0.739088,
            0.522278,
            0.413771,
        ],
        10: [
            191.506,
            60.3468,
            37.0993,
            27.3308,
            21.8749,
        ],
    }
    ref_val_Hg = {
        0: [9.96091, 10.6616, 9.27572, 8.25694, 7.49076],
        10: [289.097, 278.051, 223.261, 186.256, 160.027],
    }
    ref_val_Hq = {
        0: [-2.66667, -0.365962, -0.15071, -0.084247, -0.0543195],
        10: [-101.432, -17.2316, -7.25937, -4.04249, -2.58706],
    }
    ref_val_qq = {
        0: [
            -3.16049,
            -5.0571,
            -6.43014,
            -7.51258,
            -8.409,
            -9.17546,
            -9.84569,
            -10.4416,
            -10.9783,
        ],
        10: [
            -90.0741,
            -139.008,
            -173.487,
            -200.273,
            -222.222,
            -240.833,
            -256.994,
            -271.28,
            -284.083,
        ],
    }
    for N in range(2, 11):
        for L, ref_Hg in ref_val_Hg.items():
            sx = compute_cache(N, 3, True)
            aS2 = A_singlet(N, sx, L)
            if N % 2 == 0:
                idx = int(N / 2 - 1)
                np.testing.assert_allclose(aS2[0, 0], ref_val_gg[L][idx], rtol=2e-6)
                np.testing.assert_allclose(aS2[0, 1], ref_val_gq[L][idx], rtol=4e-6)
                np.testing.assert_allclose(aS2[2, 0], ref_Hg[idx], rtol=3e-6)
                np.testing.assert_allclose(aS2[2, 1], ref_val_Hq[L][idx], rtol=3e-6)
            np.testing.assert_allclose(aS2[1, 1], ref_val_qq[L][N - 2], rtol=4e-6)


def test_Hg2_pegasus():
    # Test against the parametrized expression for A_Hg
    # coming from Pegasus code
    # This parametrization is less accurate.
    L = 0

    for N in range(3, 20):
        sx = compute_cache(N, 3, True)
        S1 = sx[0][0]
        S2 = sx[1][0]
        S3 = sx[2][0]
        aS2 = A_singlet(N, sx, L)

        E2 = (
            2.0 / N * (constants.zeta3 - S3 + 1.0 / N * (constants.zeta2 - S2 - S1 / N))
        )

        a_hg_param = (
            -0.006
            + 1.111 * (S1**3 + 3.0 * S1 * S2 + 2.0 * S3) / N
            - 0.400 * (S1**2 + S2) / N
            + 2.770 * S1 / N
            - 24.89 / (N - 1.0)
            - 187.8 / N
            + 249.6 / (N + 1.0)
            + 1.556 * 6.0 / N**4
            - 3.292 * 2.0 / N**3
            + 93.68 * 1.0 / N**2
            - 146.8 * E2
        )

        np.testing.assert_allclose(aS2[2, 0], a_hg_param, rtol=7e-4)


def test_msbar_matching():
    logs = [0, 100]

    for L in logs:
        N = 2
        sx = compute_cache(N, 3, True)
        aS2 = A_singlet(N, sx, L, True)
        # gluon momentum conservation
        np.testing.assert_allclose(aS2[0, 0] + aS2[1, 0] + aS2[2, 0], 0.0, atol=2e-6)
