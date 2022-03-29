# -*- coding: utf-8 -*-
"""
This module contains implemtation of F11.
When using it, please cite :cite:`Blumlein:2009ta`.
Mellin transform is defined with the convention x^(N).
"""
import numba as nb
import numpy as np


@nb.njit(cache=True)
def F11(n, S1, S2):
    """Implements eq 9.27 of :cite:`Blumlein:2009ta`"""
    return (
        -0.1570209743051114 * n
        - (0.4961137242141078 * n) / (2.0 + n)
        + (0.14325154607236013 * n) / (3.0 + n)
        + (0.043572446555835365 * n) / (4.0 + n)
        - (0.1367619721729137 * n) / (5.0 + n)
        + (0.5737638752229648 * n) / (6.0 + n)
        - (1.6610332243741988 * n) / (7.0 + n)
        + (3.333896376517311 * n) / (8.0 + n)
        - (4.660416088583179 * n) / (9.0 + n)
        + (4.454651830395971 * n) / (10.0 + n)
        - (2.7814009672516686 * n) / (11.0 + n)
        + (1.0238605215663694 * n) / (12.0 + n)
        - (0.16899247190231767 * n) / (13.0 + n)
        - 0.4887437258762844 * (-1.0 + 1 / (1.0 + n))
        - 1.0
        * n
        * (
            -0.1570209813585035
            + 0.4166666666666667 / np.power(n, 3)
            + 0.47941919157221546 / np.power(n, 2)
            - 1.0 / np.power(1.0 + n, 3)
            - 1.75 / np.power(1.0 + n, 2)
            + 0.009326544681477866 / (1.0 + n)
            + 0.75 / np.power(2.0 + n, 3)
            + 1.25 / np.power(2.0 + n, 2)
            + 0.8057445842680144 / (2.0 + n)
            - 0.16666666666666666 / np.power(3.0 + n, 3)
            - 0.25 / np.power(3.0 + n, 2)
            - 0.13958627001930435 / (3.0 + n)
            - (0.25 * (4.0 + 7.0 * (1.0 + n)) * S1) / np.power(1.0 + n, 2)
            + (0.75 * (1 / (1.0 + n) + S1)) / np.power(2.0 + n, 2)
            + (1.25 * (1 / (1.0 + n) + S1)) / (2.0 + n)
            - (0.16666666666666666 * (1 / (1.0 + n) + 1 / (2.0 + n) + S1))
            / np.power(3.0 + n, 2)
            - (0.25 * (1 / (1.0 + n) + 1 / (2.0 + n) + S1)) / (3.0 + n)
            - (
                0.002777777777777778
                * (22.59090896599757 - 172.59090896599758 * (1.0 + n))
                * (1 / (1.0 + n) + (1.0 - 2.0 * (1.0 + n)) / (n * (1.0 + n)) + S1)
            )
            / np.power(n, 2)
            + (
                0.75
                * (
                    np.power(1.0 + n, -2)
                    + S1 / (1.0 + n)
                    + 0.5 * (np.power(S1, 2) + S2)
                )
            )
            / (2.0 + n)
            - (
                1.0
                * (
                    np.power(1.0 + n, -2)
                    + S1 / (1.0 + n)
                    - (1.0 * (1 / (1.0 + n) + S1)) / (1.0 + n)
                    + 0.5 * (np.power(S1, 2) + S2)
                )
            )
            / (1.0 + n)
            - (
                0.16666666666666666
                * (
                    np.power(1.0 + n, -2)
                    + np.power(2.0 + n, -2)
                    + S1 / (1.0 + n)
                    + (1 / (1.0 + n) + S1) / (2.0 + n)
                    + 0.5 * (np.power(S1, 2) + S2)
                )
            )
            / (3.0 + n)
            + (
                0.4166666666666667
                * (
                    np.power(1.0 + n, -2)
                    + 1 / (n * (1.0 + n))
                    + S1 / (1.0 + n)
                    + ((1.0 - 2.0 * (1.0 + n)) * (1 / (1.0 + n) + S1)) / (n * (1.0 + n))
                    + 0.5 * (np.power(S1, 2) + S2)
                )
            )
            / n
        )
    )
