# -*- coding: utf-8 -*-
import numpy as np
import pytest

from eko.anomalous_dimensions import harmonics

# until https://github.com/numba/numba/pull/5660 is confirmed
# we need to deactivate numba prior running


def test_cern_polygamma():
    zs = [1.0, 2.0, 3.0, 0 + 1j, -1 + 1j, -2 + 1j, -1 + 2j, -2 + 2j, -3 + 2j]
    ks = range(5)
    fortran_ref = [
        [
            (-0.5772156649015332 + 0j),
            (0.42278433509846636 + 0j),
            (0.9227843350984672 + 0j),
            (0.09465032062247669 + 2.0766740474685816j),
            (0.5946503206224767 + 2.5766740474685816j),
            (0.9946503206224772 + 2.7766740474685814j),
            (0.9145915153739776 + 2.2208072826422303j),
            (1.1645915153739772 + 2.47080728264223j),
            (1.395360746143208 + 2.624653436488384j),
        ],
        [
            (1.6449340668482264 + 0j),
            (0.6449340668482264 + 0j),
            (0.3949340668482264 + 0j),
            (-0.5369999033772361 - 0.7942335427593189j),
            (-0.5369999033772362 - 0.2942335427593189j),
            (-0.4169999033772362 - 0.13423354275931887j),
            (-0.24506883785905695 - 0.3178255501472297j),
            (-0.24506883785905695 - 0.19282555014722969j),
            (-0.21548303904248892 - 0.12181963298746643j),
        ],
        [
            (-2.404113806319188 + 0j),
            (-0.40411380631918853 + 0j),
            (-0.15411380631918858 + 0j),
            (0.3685529315879351 - 1.233347149654934j),
            (-0.13144706841206477 - 0.7333471496549337j),
            (-0.09944706841206462 - 0.5573471496549336j),
            (0.03902435405364951 - 0.15743252404131272j),
            (-0.02347564594635048 - 0.09493252404131272j),
            (-0.031668636387861625 - 0.053057239562477945j),
        ],
        [
            (6.49393940226683 + 0j),
            (0.49393940226682925 + 0j),
            (0.11893940226682913 + 0j),
            (4.4771255510465044 - 0.31728657866196064j),
            (2.9771255510464925 - 0.3172865786619599j),
            (2.909925551046492 - 0.08688657866195917j),
            (0.12301766661068443 - 0.05523068481179527j),
            (0.02926766661068438 - 0.055230684811795216j),
            (0.004268541930176011 - 0.03002148345329936j),
        ],
        [
            (-24.88626612344089 + 0j),
            (-0.8862661234408784 + 0j),
            (-0.13626612344087824 + 0j),
            (3.2795081690440493 + 21.41938794863803j),
            (0.2795081690440445 + 18.419387948637894j),
            (-0.012331830955960252 + 18.734267948637896j),
            (0.14223316576854003 + 0.10023607930398608j),
            (0.04848316576854002 + 0.006486079303986134j),
            (0.009893695996688708 + 0.014372034600746361j),
        ],
    ]
    for nk, k in enumerate(ks):
        for nz, z in enumerate(zs):
            me = harmonics.cern_polygamma(z, k)
            ref = fortran_ref[nk][nz]
            np.testing.assert_almost_equal(me, ref)
    # errors
    with pytest.raises(NotImplementedError):
        _ = harmonics.cern_polygamma(1, 5)
    with pytest.raises(ValueError):
        _ = harmonics.cern_polygamma(0, 0)


def test_harmonic_Sx():
    """test harmonic sums S_x on real axis"""
    # test on real axis
    def sx(n, m):
        return np.sum([1 / k ** m for k in range(1, n + 1)])

    ls = [harmonics.harmonic_S1, harmonics.harmonic_S2, harmonics.harmonic_S3]
    for k in range(1, 3 + 1):
        for n in range(1, 4 + 1):
            np.testing.assert_almost_equal(ls[k - 1](n), sx(n, k))


def test_melling_g3():
    ns = [1.0, 2.0, 1 + 1j]
    # NIntegrate[x^({1, 2, 1 + I} - 1) PolyLog[2, x]/(1 + x), {x, 0, 1}]
    mma_ref_values = [0.3888958462, 0.2560382207, 0.3049381491 - 0.1589060625j]
    for n, r in zip(ns, mma_ref_values):
        np.testing.assert_almost_equal(harmonics.mellin_g3(n), r, decimal=6)


def test_melling_g3_pegasus():
    # Test against pegasus implementation
    for N in [1, 2, 3, 4]:
        S1 = harmonics.harmonic_S1(N)
        N1 = N + 1.0
        N2 = N + 2.0
        N3 = N + 3.0
        N4 = N + 4.0
        N5 = N + 5.0
        N6 = N + 6.0
        S11 = S1 + 1.0 / N1
        S12 = S11 + 1.0 / N2
        S13 = S12 + 1.0 / N3
        S14 = S13 + 1.0 / N4
        S15 = S14 + 1.0 / N5
        S16 = S15 + 1.0 / N6
        zeta2 = harmonics.zeta2

        SPMOM = (
            1.0000 * (zeta2 - S1 / N) / N
            - 0.9992 * (zeta2 - S11 / N1) / N1
            + 0.9851 * (zeta2 - S12 / N2) / N2
            - 0.9005 * (zeta2 - S13 / N3) / N3
            + 0.6621 * (zeta2 - S14 / N4) / N4
            - 0.3174 * (zeta2 - S15 / N5) / N5
            + 0.0699 * (zeta2 - S16 / N6) / N6
        )

        np.testing.assert_allclose(harmonics.mellin_g3(N), SPMOM)
