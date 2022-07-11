# -*- coding: utf-8 -*-
import numba as nb
import numpy as np


@nb.njit(cache=True)
def A_qqNS(n, sx, nf, L):
    r"""Computes the |N3LO| singlet |OME| :math:`A_{qq}^{NS,(3)}(N)`.
    The expression is presented in :cite:`Bierenbaum:2009mv` and
    :cite:`Ablinger:2014vwa`. It contains some weight 5 harmonics sums.

    When using the code, please cite the complete list of references
    available in :mod:`eko.matching_conditions.as3`.

    Note the part proportional to nf^0 includes weight = 5
    harmonics and has been parametrized in Mellin space.
    For this piece the accuracy wrt the known moments is below the 0.01% (N<1000)
    and the absolute diff is within 5e-3.
    All the other contributions are provided exact.

    Parameters
    ----------
    n : complex
        Mellin moment
    sx : list
        harmonic sums cache
    nf : int
        number of active flavor below the threshold
    L : float
        :math:`\ln(\mu_F^2 / m_h^2)`

    Returns
    -------
    complex
        :math:`A_{qq}^{NS,(3)}(N)`

    """
    S1, _ = sx[0]
    S2, Sm2 = sx[1]
    S3, _, _, Sm21, _, Sm3 = sx[2]
    S4, S31, _, Sm22, Sm211, _, Sm4 = sx[3]
    a_qqNS_l0_nf1 = (
        0.3333333333333333
        * nf
        * (
            (
                0.0054869684499314125
                * (
                    432.0
                    + 144.0 * n
                    - 2016.0 * np.power(n, 2)
                    + 1712.0 * np.power(n, 3)
                    + 15165.0 * np.power(n, 4)
                    + 25380.0 * np.power(n, 5)
                    + 23870.0 * np.power(n, 6)
                    + 14196.0 * np.power(n, 7)
                    + 3549.0 * np.power(n, 8)
                )
            )
            / (np.power(n, 4) * np.power(1.0 + n, 4))
            - 33.00960219478738 * S1
            + 11.39728026699467
            * (
                (-0.5 * (2.0 + 3.0 * n + 3.0 * np.power(n, 2))) / (n * (1.0 + n))
                + 2.0 * S1
            )
            + 1.5802469135802468 * S2
            + 7.901234567901234 * S3
            - 4.7407407407407405 * S4
        )
    )
    # Parametrized part
    a_qqNS_l0_nf0 = (
        3461.323400827195 / (1.0 + n) ** 5
        - (819109.4159686691 * n) / (1.0 + n) ** 5
        - (588978.6568109449 * n**2) / (1.0 + n) ** 5
        - (89270.88285749684 * n**3) / (1.0 + n) ** 5
        - (3636.6667539128853 * n**4) / (1.0 + n) ** 5
        + (494039.49940412445 * S1) / (1.0 + n) ** 4
        + (230195.51806989315 * n * S1) / (1.0 + n) ** 4
        + (25247.421575674347 * n**2 * S1) / (1.0 + n) ** 4
        + (1025.2898493649648 * n**3 * S1) / (1.0 + n) ** 4
        + (60.18259379702244 * n**4 * S1) / (1.0 + n) ** 4
        - 4.30629116458179 * S1**2
        + 0.160466156494926 * S1**3
        - 108.40179984327544 * S2
    )
    a_qqNS_l0 = a_qqNS_l0_nf0 + a_qqNS_l0_nf1
    a_qqNS_l3 = (
        8.592592592592593 / (1.0 + n)
        + 5.728395061728395 / (n * (1.0 + n))
        + (8.592592592592593 * n) / (1.0 + n)
        - (0.5925925925925926 * nf) / (1.0 + n)
        - (0.3950617283950617 * nf) / (n * (1.0 + n))
        - (0.5925925925925926 * n * nf) / (1.0 + n)
        - 11.45679012345679 * S1
        + 0.7901234567901234 * nf * S1
    )
    a_qqNS_l2 = (
        113.33333333333333 / np.power(1.0 + n, 3)
        + 7.111111111111111 / (np.power(n, 3) * np.power(1.0 + n, 3))
        + 23.703703703703702 / (np.power(n, 2) * np.power(1.0 + n, 3))
        + 63.111111111111114 / (n * np.power(1.0 + n, 3))
        + (124.0 * n) / np.power(1.0 + n, 3)
        + (89.33333333333333 * np.power(n, 2)) / np.power(1.0 + n, 3)
        + (29.77777777777778 * np.power(n, 3)) / np.power(1.0 + n, 3)
        + 4.6419753086419755 / np.power(1.0 + n, 2)
        - 1.1851851851851851 / (np.power(n, 2) * np.power(1.0 + n, 2))
        + 1.9753086419753085 / (n * np.power(1.0 + n, 2))
        + (0.5925925925925926 * n) / np.power(1.0 + n, 2)
        + (0.2962962962962963 * np.power(n, 2)) / np.power(1.0 + n, 2)
        - 44.839506172839506 * S1
        - (7.111111111111111 * S1) / np.power(1.0 + n, 2)
        - (9.481481481481481 * S1) / (np.power(n, 2) * np.power(1.0 + n, 2))
        - (18.962962962962962 * S1) / (n * np.power(1.0 + n, 2))
        - (14.222222222222221 * n * S1) / np.power(1.0 + n, 2)
        - (7.111111111111111 * np.power(n, 2) * S1) / np.power(1.0 + n, 2)
        + 2.3703703703703702 * S2
        - (14.222222222222221 * S2) / (1.0 + n)
        - (9.481481481481481 * S2) / (n * (1.0 + n))
        - (14.222222222222221 * n * S2) / (1.0 + n)
        + 18.962962962962962 * S1 * S2
        - 2.3703703703703702 * S3
        + (2.3703703703703702 * Sm2) / (n * (1.0 + n))
        - 4.7407407407407405 * S1 * Sm2
        + 4.7407407407407405 * Sm21
        - 2.3703703703703702 * Sm3
    )
    a_qqNS_l1 = (
        -211.92592592592592 / np.power(1.0 + n, 4)
        + 18.962962962962962 / (np.power(n, 4) * np.power(1.0 + n, 4))
        + 16.0 / (np.power(n, 3) * np.power(1.0 + n, 4))
        + 24.098765432098766 / (np.power(n, 2) * np.power(1.0 + n, 4))
        + 18.864197530864196 / (n * np.power(1.0 + n, 4))
        - (115.55555555555556 * n) / np.power(1.0 + n, 4)
        + (444.69135802469134 * np.power(n, 2)) / np.power(1.0 + n, 4)
        + (469.037037037037 * np.power(n, 3)) / np.power(1.0 + n, 4)
        + (117.25925925925925 * np.power(n, 4)) / np.power(1.0 + n, 4)
        - 70.23315829196848 / (1.0 + n)
        - 46.82210552797899 / (n * (1.0 + n))
        - (70.23315829196848 * n) / (1.0 + n)
        - (16.016460905349795 * nf) / np.power(1.0 + n, 3)
        + (1.1851851851851851 * nf) / (np.power(n, 3) * np.power(1.0 + n, 3))
        - (0.7901234567901234 * nf) / (np.power(n, 2) * np.power(1.0 + n, 3))
        - (8.823045267489713 * nf) / (n * np.power(1.0 + n, 3))
        - (25.267489711934157 * n * nf) / np.power(1.0 + n, 3)
        - (25.925925925925927 * np.power(n, 2) * nf) / np.power(1.0 + n, 3)
        - (8.641975308641975 * np.power(n, 3) * nf) / np.power(1.0 + n, 3)
        + 93.64421105595798 * S1
        + (143.60493827160494 * S1) / np.power(1.0 + n, 3)
        - (27.25925925925926 * S1) / (np.power(n, 3) * np.power(1.0 + n, 3))
        - (22.91358024691358 * S1) / (np.power(n, 2) * np.power(1.0 + n, 3))
        + (78.22222222222223 * S1) / (n * np.power(1.0 + n, 3))
        + (127.4074074074074 * n * S1) / np.power(1.0 + n, 3)
        + (127.4074074074074 * np.power(n, 2) * S1) / np.power(1.0 + n, 3)
        + (42.46913580246913 * np.power(n, 3) * S1) / np.power(1.0 + n, 3)
        + 8.954732510288066 * nf * S1
        - 132.74074074074073 * S2
        + (62.41975308641975 * S2) / np.power(1.0 + n, 2)
        - (18.962962962962962 * S2) / (np.power(n, 2) * np.power(1.0 + n, 2))
        + (12.641975308641975 * S2) / (n * np.power(1.0 + n, 2))
        + (23.703703703703702 * n * S2) / np.power(1.0 + n, 2)
        + (11.851851851851851 * np.power(n, 2) * S2) / np.power(1.0 + n, 2)
        + 3.950617283950617 * nf * S2
        - 63.20987654320987 * S1 * S2
        + 18.962962962962962 * np.power(S2, 2)
        + (18.567901234567902 * S3) / (1.0 + n)
        - (5.925925925925926 * S3) / (n * (1.0 + n))
        + (18.567901234567902 * n * S3) / (1.0 + n)
        - 2.3703703703703702 * nf * S3
        + 11.851851851851851 * S1 * S3
        + 47.407407407407405 * S31
        - 30.814814814814813 * S4
        - (12.641975308641975 * Sm2) / np.power(1.0 + n, 2)
        + (2.3703703703703702 * Sm2) / (np.power(n, 2) * np.power(1.0 + n, 2))
        - (7.901234567901234 * Sm2) / (n * np.power(1.0 + n, 2))
        + 15.802469135802468 * S1 * Sm2
        - 4.7407407407407405 * S2 * Sm2
        - (15.802469135802468 * Sm21) / (1.0 + n)
        + (4.7407407407407405 * Sm21) / (n * (1.0 + n))
        - (15.802469135802468 * n * Sm21) / (1.0 + n)
        - 9.481481481481481 * S1 * Sm21
        + 18.962962962962962 * Sm211
        - 4.7407407407407405 * Sm22
        + (7.901234567901234 * Sm3) / (1.0 + n)
        + (2.3703703703703702 * Sm3) / (n * (1.0 + n))
        + (7.901234567901234 * n * Sm3) / (1.0 + n)
        - 4.7407407407407405 * S1 * Sm3
        - 4.7407407407407405 * Sm4
    )
    return a_qqNS_l0 + a_qqNS_l1 * L + a_qqNS_l2 * L**2 + a_qqNS_l3 * L**3
