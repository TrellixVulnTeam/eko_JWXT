# -*- coding: utf-8 -*-
"""
This module contains the anomalous dimension :math:`\\gamma_{qg}^{(3)}`
"""
import numba as nb
import numpy as np

from ...harmonics.log_functions import lm13, lm13m1, lm14, lm15


@nb.njit(cache=True)
def gamma_qg_nf3(n, sx):
    """Implements the part proportional to :math:`nf^3` of :math:`\\gamma_{qg}^{(3)}`
    The expression is copied exact from Eq. 3.12 of :cite:`Davies:2016jie`.

    Parameters
    ----------
    n : complex
        Mellin moment
    sx : list
        harmonic sums cache

    Returns
    -------
    complex
        |N3LO| non-singlet anomalous dimension :math:`\\gamma_{qg}^{(3)}|_{nf^3}`

    """
    S1 = sx[0][0]
    S2, Sm2 = sx[1]
    S3, S21, _, _, _, Sm3 = sx[2]
    S4, S31, S211, _, _, _, Sm4 = sx[3]
    return 1.3333333333333333 * (
        44.56685134331718 / (-1.0 + n)
        - 82.37037037037037 / np.power(n, 5)
        + 95.30864197530865 / np.power(n, 4)
        - 298.6951686088834 / np.power(n, 3)
        + 334.4519003852186 / np.power(n, 2)
        - 576.1641081960868 / n
        - 156.44444444444446 / np.power(1.0 + n, 6)
        + 271.4074074074074 / np.power(1.0 + n, 5)
        - 142.6172839506173 / np.power(1.0 + n, 4)
        + 49.20926725891911 / np.power(1.0 + n, 3)
        + 242.3162373306182 / np.power(1.0 + n, 2)
        + 383.95514040473176 / (1.0 + n)
        + 75.85185185185185 / np.power(2.0 + n, 5)
        - 18.962962962962962 / np.power(2.0 + n, 4)
        - 28.97119341563786 / np.power(2.0 + n, 3)
        + 57.904384241653375 / np.power(2.0 + n, 2)
        + 153.56036440484917 / (2.0 + n)
        - (7.725651577503429 * S1) / (-1.0 + n)
        + (35.55555555555556 * S1) / np.power(n, 5)
        - (53.333333333333336 * S1) / np.power(n, 4)
        + (149.7283950617284 * S1) / np.power(n, 3)
        - (189.49794238683128 * S1) / np.power(n, 2)
        + (219.77429764880566 * S1) / n
        - (71.11111111111111 * S1) / np.power(1.0 + n, 5)
        + (75.85185185185185 * S1) / np.power(1.0 + n, 4)
        + (45.4320987654321 * S1) / np.power(1.0 + n, 3)
        - (24.691358024691358 * S1) / np.power(1.0 + n, 2)
        - (242.01773110008048 * S1) / (1.0 + n)
        + (37.925925925925924 * S1) / np.power(2.0 + n, 4)
        + (53.72839506172839 * S1) / np.power(2.0 + n, 3)
        + (39.76954732510288 * S1) / np.power(2.0 + n, 2)
        + (33.84214810968268 * S1) / (2.0 + n)
        - (8.954732510288066 * S2) / (-1.0 + n)
        + (28.444444444444443 * S2) / np.power(n, 4)
        - (47.407407407407405 * S2) / np.power(n, 3)
        + (117.33333333333333 * S2) / np.power(n, 2)
        - (128.52674897119343 * S2) / n
        - (71.11111111111111 * S2) / np.power(1.0 + n, 4)
        + (9.481481481481481 * S2) / np.power(1.0 + n, 3)
        + (60.44444444444444 * S2) / np.power(1.0 + n, 2)
        - (11.588477366255145 * S2) / (1.0 + n)
        + (56.888888888888886 * S2) / np.power(2.0 + n, 3)
        + (112.19753086419753 * S2) / np.power(2.0 + n, 2)
        + (144.98765432098764 * S2) / (2.0 + n)
        - (2.3703703703703702 * (np.power(S1, 2) + S2)) / (-1.0 + n)
        + (2.3703703703703702 * (np.power(S1, 2) + S2)) / np.power(n, 3)
        + (3.3580246913580245 * (np.power(S1, 2) + S2)) / np.power(n, 2)
        - (13.695473251028806 * (np.power(S1, 2) + S2)) / n
        + (7.111111111111111 * (np.power(S1, 2) + S2)) / np.power(1.0 + n, 4)
        + (9.481481481481481 * (np.power(S1, 2) + S2)) / np.power(1.0 + n, 3)
        - (2.962962962962963 * (np.power(S1, 2) + S2)) / np.power(1.0 + n, 2)
        + (53.76131687242798 * (np.power(S1, 2) + S2)) / (1.0 + n)
        - (9.481481481481481 * (np.power(S1, 2) + S2)) / np.power(2.0 + n, 3)
        - (21.333333333333332 * (np.power(S1, 2) + S2)) / np.power(2.0 + n, 2)
        - (38.650205761316876 * (np.power(S1, 2) + S2)) / (2.0 + n)
        - (3.1604938271604937 * S21) / (-1.0 + n)
        + (7.111111111111111 * S21) / np.power(n, 3)
        - (10.666666666666666 * S21) / np.power(n, 2)
        + (32.0 * S21) / n
        - (14.222222222222221 * S21) / np.power(1.0 + n, 3)
        - (53.333333333333336 * S21) / (1.0 + n)
        + (9.481481481481481 * S21) / np.power(2.0 + n, 2)
        + (24.493827160493826 * S21) / (2.0 + n)
        - (3.1604938271604937 * S3) / (-1.0 + n)
        + (7.111111111111111 * S3) / np.power(n, 3)
        - (10.666666666666666 * S3) / np.power(n, 2)
        + (28.049382716049383 * S3) / n
        - (14.222222222222221 * S3) / np.power(1.0 + n, 3)
        - (43.06172839506173 * S3) / (1.0 + n)
        + (9.481481481481481 * S3) / np.power(2.0 + n, 2)
        + (14.222222222222221 * S3) / (2.0 + n)
        - (3.1604938271604937 * (S1 * S2 - 1.0 * S21 + S3)) / (-1.0 + n)
        + (7.111111111111111 * (S1 * S2 - 1.0 * S21 + S3)) / np.power(n, 3)
        - (10.666666666666666 * (S1 * S2 - 1.0 * S21 + S3)) / np.power(n, 2)
        + (32.0 * (S1 * S2 - 1.0 * S21 + S3)) / n
        - (14.222222222222221 * (S1 * S2 - 1.0 * S21 + S3)) / np.power(1.0 + n, 3)
        - (53.333333333333336 * (S1 * S2 - 1.0 * S21 + S3)) / (1.0 + n)
        + (9.481481481481481 * (S1 * S2 - 1.0 * S21 + S3)) / np.power(2.0 + n, 2)
        + (24.493827160493826 * (S1 * S2 - 1.0 * S21 + S3)) / (2.0 + n)
        + (0.5267489711934157 * (np.power(S1, 3) + 3.0 * S1 * S2 + 2.0 * S3))
        / (-1.0 + n)
        - (1.1851851851851851 * (np.power(S1, 3) + 3.0 * S1 * S2 + 2.0 * S3))
        / np.power(n, 3)
        + (1.9753086419753085 * (np.power(S1, 3) + 3.0 * S1 * S2 + 2.0 * S3))
        / np.power(n, 2)
        - (4.674897119341564 * (np.power(S1, 3) + 3.0 * S1 * S2 + 2.0 * S3)) / n
        + (2.3703703703703702 * (np.power(S1, 3) + 3.0 * S1 * S2 + 2.0 * S3))
        / np.power(1.0 + n, 3)
        + (7.57201646090535 * (np.power(S1, 3) + 3.0 * S1 * S2 + 2.0 * S3)) / (1.0 + n)
        - (1.5802469135802468 * (np.power(S1, 3) + 3.0 * S1 * S2 + 2.0 * S3))
        / np.power(2.0 + n, 2)
        - (2.765432098765432 * (np.power(S1, 3) + 3.0 * S1 * S2 + 2.0 * S3)) / (2.0 + n)
        - (
            1.1851851851851851
            * (
                0.041666666666666664 * np.power(S1, 4)
                + 0.25 * np.power(S1, 2) * S2
                + 0.125 * np.power(S2, 2)
                + 0.3333333333333333 * S1 * S3
                + 0.25 * S4
            )
        )
        / n
        + (
            2.3703703703703702
            * (
                0.041666666666666664 * np.power(S1, 4)
                + 0.25 * np.power(S1, 2) * S2
                + 0.125 * np.power(S2, 2)
                + 0.3333333333333333 * S1 * S3
                + 0.25 * S4
            )
        )
        / (1.0 + n)
        - (
            2.3703703703703702
            * (
                0.041666666666666664 * np.power(S1, 4)
                + 0.25 * np.power(S1, 2) * S2
                + 0.125 * np.power(S2, 2)
                + 0.3333333333333333 * S1 * S3
                + 0.25 * S4
            )
        )
        / (2.0 + n)
        + (3.5555555555555554 * S4) / n
        - (7.111111111111111 * S4) / (1.0 + n)
        + (7.111111111111111 * S4) / (2.0 + n)
    ) + 3.0 * (
        2.5381463063368415 / (-1.0 + n)
        + 3.5555555555555554 / np.power(n, 5)
        + 5.728395061728395 / np.power(n, 4)
        + 4.559670781893004 / np.power(n, 3)
        + 2.036401939671693 / np.power(n, 2)
        - 1.1169664019346115 / n
        + 26.074074074074073 / np.power(1.0 + n, 5)
        - 56.098765432098766 / np.power(1.0 + n, 4)
        + 70.0246913580247 / np.power(1.0 + n, 3)
        - 56.58563233464838 / np.power(1.0 + n, 2)
        + 23.268759906664844 / (1.0 + n)
        + 18.962962962962962 / np.power(2.0 + n, 5)
        - 37.925925925925924 / np.power(2.0 + n, 4)
        + 22.386831275720166 / np.power(2.0 + n, 3)
        + 25.899964373170548 / np.power(2.0 + n, 2)
        - 33.71051594275432 / (2.0 + n)
        + (0.3511659807956104 * S1) / (-1.0 + n)
        - (9.481481481481481 * S1) / np.power(n, 4)
        + (8.938271604938272 * S1) / np.power(n, 3)
        - (17.432098765432098 * S1) / np.power(n, 2)
        + (15.015825807984449 * S1) / n
        + (14.222222222222221 * S1) / np.power(1.0 + n, 4)
        - (1.7777777777777777 * S1) / np.power(1.0 + n, 3)
        - (14.534979423868313 * S1) / np.power(1.0 + n, 2)
        + (48.28933603835209 * S1) / (1.0 + n)
        + (9.481481481481481 * S1) / np.power(2.0 + n, 4)
        - (46.617283950617285 * S1) / np.power(2.0 + n, 3)
        - (42.27160493827161 * S1) / np.power(2.0 + n, 2)
        - (64.96148967346869 * S1) / (2.0 + n)
        + (1.7119341563786008 * S2) / (-1.0 + n)
        - (2.3703703703703702 * S2) / np.power(n, 3)
        + (0.7407407407407407 * S2) / np.power(n, 2)
        - (7.703703703703703 * S2) / n
        + (9.481481481481481 * S2) / np.power(1.0 + n, 3)
        - (15.012345679012345 * S2) / np.power(1.0 + n, 2)
        + (27.308641975308642 * S2) / (1.0 + n)
        - (4.7407407407407405 * S2) / np.power(2.0 + n, 3)
        + (2.765432098765432 * S2) / np.power(2.0 + n, 2)
        - (21.020576131687243 * S2) / (2.0 + n)
        + (0.8559670781893004 * (np.power(S1, 2) + S2)) / (-1.0 + n)
        - (1.1851851851851851 * (np.power(S1, 2) + S2)) / np.power(n, 3)
        + (0.37037037037037035 * (np.power(S1, 2) + S2)) / np.power(n, 2)
        - (2.60082304526749 * (np.power(S1, 2) + S2)) / n
        + (2.9135802469135803 * (np.power(S1, 2) + S2)) / np.power(1.0 + n, 2)
        + (5.275720164609053 * (np.power(S1, 2) + S2)) / (1.0 + n)
        + (2.3703703703703702 * (np.power(S1, 2) + S2)) / np.power(2.0 + n, 3)
        - (6.518518518518518 * (np.power(S1, 2) + S2)) / np.power(2.0 + n, 2)
        - (2.8724279835390947 * (np.power(S1, 2) + S2)) / (2.0 + n)
        - (3.950617283950617 * S21) / n
        - (2.3703703703703702 * S21) / np.power(1.0 + n, 2)
        + (7.901234567901234 * S21) / (1.0 + n)
        + (2.3703703703703702 * S21) / np.power(2.0 + n, 2)
        - (7.901234567901234 * S21) / (2.0 + n)
        + (1.1851851851851851 * S211) / n
        - (2.3703703703703702 * S211) / (1.0 + n)
        + (2.3703703703703702 * S211) / (2.0 + n)
        - (3.950617283950617 * S3) / n
        + (2.3703703703703702 * S3) / np.power(1.0 + n, 2)
        + (3.1604938271604937 * S3) / (1.0 + n)
        - (2.3703703703703702 * S3) / np.power(2.0 + n, 2)
        - (3.1604938271604937 * S3) / (2.0 + n)
        + (3.950617283950617 * (S1 * S2 - 1.0 * S21 + S3)) / n
        + (2.3703703703703702 * (S1 * S2 - 1.0 * S21 + S3)) / np.power(1.0 + n, 2)
        - (7.901234567901234 * (S1 * S2 - 1.0 * S21 + S3)) / (1.0 + n)
        - (2.3703703703703702 * (S1 * S2 - 1.0 * S21 + S3)) / np.power(2.0 + n, 2)
        + (7.901234567901234 * (S1 * S2 - 1.0 * S21 + S3)) / (2.0 + n)
        - (0.6584362139917695 * (np.power(S1, 3) + 3.0 * S1 * S2 + 2.0 * S3)) / n
        - (0.3950617283950617 * (np.power(S1, 3) + 3.0 * S1 * S2 + 2.0 * S3))
        / np.power(1.0 + n, 2)
        + (1.316872427983539 * (np.power(S1, 3) + 3.0 * S1 * S2 + 2.0 * S3)) / (1.0 + n)
        + (0.3950617283950617 * (np.power(S1, 3) + 3.0 * S1 * S2 + 2.0 * S3))
        / np.power(2.0 + n, 2)
        - (1.316872427983539 * (np.power(S1, 3) + 3.0 * S1 * S2 + 2.0 * S3)) / (2.0 + n)
        + (1.1851851851851851 * S31) / n
        - (2.3703703703703702 * S31) / (1.0 + n)
        + (2.3703703703703702 * S31) / (2.0 + n)
        + (
            1.1851851851851851
            * (
                0.041666666666666664 * np.power(S1, 4)
                + 0.25 * np.power(S1, 2) * S2
                + 0.125 * np.power(S2, 2)
                + 0.3333333333333333 * S1 * S3
                + 0.25 * S4
            )
        )
        / n
        - (
            2.3703703703703702
            * (
                0.041666666666666664 * np.power(S1, 4)
                + 0.25 * np.power(S1, 2) * S2
                + 0.125 * np.power(S2, 2)
                + 0.3333333333333333 * S1 * S3
                + 0.25 * S4
            )
        )
        / (1.0 + n)
        + (
            2.3703703703703702
            * (
                0.041666666666666664 * np.power(S1, 4)
                + 0.25 * np.power(S1, 2) * S2
                + 0.125 * np.power(S2, 2)
                + 0.3333333333333333 * S1 * S3
                + 0.25 * S4
            )
        )
        / (2.0 + n)
        + (3.5555555555555554 * S4) / n
        - (7.111111111111111 * S4) / (1.0 + n)
        + (7.111111111111111 * S4) / (2.0 + n)
        - (0.5925925925925926 * (np.power(S2, 2) + S4)) / n
        + (1.1851851851851851 * (np.power(S2, 2) + S4)) / (1.0 + n)
        - (1.1851851851851851 * (np.power(S2, 2) + S4)) / (2.0 + n)
        - (1.1851851851851851 * (S1 * S3 - 1.0 * S31 + S4)) / n
        + (2.3703703703703702 * (S1 * S3 - 1.0 * S31 + S4)) / (1.0 + n)
        - (2.3703703703703702 * (S1 * S3 - 1.0 * S31 + S4)) / (2.0 + n)
        + (
            1.1851851851851851
            * (S1 * S21 - 2.0 * S211 + S31 + 0.5 * (np.power(S2, 2) + S4))
        )
        / n
        - (
            2.3703703703703702
            * (S1 * S21 - 2.0 * S211 + S31 + 0.5 * (np.power(S2, 2) + S4))
        )
        / (1.0 + n)
        + (
            2.3703703703703702
            * (S1 * S21 - 2.0 * S211 + S31 + 0.5 * (np.power(S2, 2) + S4))
        )
        / (2.0 + n)
        - (
            1.1851851851851851
            * (
                S211
                + 0.5 * (S1 * S3 + S1 * (S1 * S2 - 2.0 * S21 + S3) - 2.0 * S31 + S4)
            )
        )
        / n
        + (
            2.3703703703703702
            * (
                S211
                + 0.5 * (S1 * S3 + S1 * (S1 * S2 - 2.0 * S21 + S3) - 2.0 * S31 + S4)
            )
        )
        / (1.0 + n)
        - (
            2.3703703703703702
            * (
                S211
                + 0.5 * (S1 * S3 + S1 * (S1 * S2 - 2.0 * S21 + S3) - 2.0 * S31 + S4)
            )
        )
        / (2.0 + n)
        + (2.5020576131687244 * Sm2) / n
        + (0.5925925925925926 * Sm2) / np.power(1.0 + n, 2)
        - (0.6584362139917695 * Sm2) / (1.0 + n)
        + (1.8436213991769548 * Sm2) / (2.0 + n)
        - (7.901234567901234 * Sm3) / n
        + (11.061728395061728 * Sm3) / (1.0 + n)
        - (11.061728395061728 * Sm3) / (2.0 + n)
        + (4.7407407407407405 * Sm4) / n
        - (9.481481481481481 * Sm4) / (1.0 + n)
        + (9.481481481481481 * Sm4) / (2.0 + n)
    )


@nb.njit(cache=True)
def gamma_qg_nf1(n, sx):
    """Implements the part proportional to :math:`nf^1` of :math:`\\gamma_{qg}^{(3)}`.
    Parameters
    ----------
    n : complex
        Mellin moment
    sx : list
        harmonic sums cache

    Returns
    -------
    complex
        |N3LO| non-singlet anomalous dimension :math:`\\gamma_{qg}^{(3)}|_{nf^1}`

    """
    S1 = sx[0][0]
    S2 = sx[1][0]
    S3 = sx[2][0]
    S4 = sx[3][0]
    S5 = sx[4][0]
    return (
        -7871.5226542038545 / np.power(-1.0 + n, 3)
        + 13143.091386873139 / np.power(-1.0 + n, 2)
        - 8555.368284884158 / (-1.0 + n)
        + 14103.703703703704 / np.power(n, 7)
        + 2588.8395061728397 / np.power(n, 6)
        + 68802.34242841466 / np.power(n, 5)
        - 212.90108988599422 * lm13(n, S1, S2, S3)
        - 9766.692337529312 * lm13m1(n, S1, S2, S3)
        - 35.68779444531073 * lm14(n, S1, S2, S3, S4)
        - 1.8518518518518519 * lm15(n, S1, S2, S3, S4, S5)
    )


@nb.njit(cache=True)
def gamma_qg_nf2(n, sx):
    """Implements the part proportional to :math:`nf^2` of :math:`\\gamma_{qg}^{(3)}`.

    Parameters
    ----------
    n : complex
        Mellin moment
    sx : list
        harmonic sums cache

    Returns
    -------
    complex
        |N3LO| non-singlet anomalous dimension :math:`\\gamma_{qg}^{(3)}|_{nf^2}`

    """
    S1 = sx[0][0]
    S2 = sx[1][0]
    S3 = sx[2][0]
    S4 = sx[3][0]
    S5 = sx[4][0]
    return (
        314.1395295099842 / np.power(-1.0 + n, 2)
        + 419.450779112087 / (-1.0 + n)
        - 1991.111111111111 / np.power(n, 7)
        + 2069.3333333333335 / np.power(n, 6)
        - 7229.376633440217 / np.power(n, 5)
        + 72.72541176281906 * lm13(n, S1, S2, S3)
        + 0.8816004399720675 * lm13m1(n, S1, S2, S3)
        + 3.511659807956104 * lm14(n, S1, S2, S3, S4)
        + 0.411522633744856 * lm15(n, S1, S2, S3, S4, S5)
    )


@nb.njit(cache=True)
def gamma_qg(n, nf, sx):
    """Computes the |N3LO| quark-gluon singlet anomalous dimension.

    Parameters
    ----------
    n : complex
        Mellin moment
    nf : int
        Number of active flavors
    sx : list
        harmonic sums cache

    Returns
    -------
    complex
        |N3LO| quark-gluon singlet anomalous dimension
        :math:`\\gamma_{qg}^{(3)}(N)`

    See Also
    --------
    gamma_qg_nf1: :math:`\\gamma_{qg}^{(3)}|_{nf^1}`
    gamma_qg_nf2: :math:`\\gamma_{qg}^{(3)}|_{nf^2}`
    gamma_qg_nf3: :math:`\\gamma_{qg}^{(3)}|_{nf^3}`

    """
    return (
        +nf * gamma_qg_nf1(n, sx)
        + nf**2 * gamma_qg_nf2(n, sx)
        + nf**3 * gamma_qg_nf3(n, sx)
    )
