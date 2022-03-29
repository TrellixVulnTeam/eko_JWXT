# -*- coding: utf-8 -*-
"""
This module contains implemtation of F13.
When using it, please cite :cite:`Blumlein:2009ta`.
Mellin transform is defined with the convention x^(N).
"""
import numba as nb
import numpy as np


@nb.njit(cache=True)
def F13(n, S1, S2):
    """Implements eq 9.29 of :cite:`Blumlein:2009ta`"""
    return (
        -0.15312792746068732 * n
        + (0.13621083778040208 * n) / (2.0 + n)
        - (0.474631789932249 * n) / (3.0 + n)
        + (0.24528438212633397 * n) / (4.0 + n)
        - (0.26580874921126374 * n) / (5.0 + n)
        + (1.2217722976683179 * n) / (6.0 + n)
        - (3.6324293738026023 * n) / (7.0 + n)
        + (7.4838836775956015 * n) / (8.0 + n)
        - (10.706375063797914 * n) / (9.0 + n)
        + (10.449787985527623 * n) / (10.0 + n)
        - (6.649468393739114 * n) / (11.0 + n)
        + (2.4904695902320904 * n) / (12.0 + n)
        - (0.41762920477450316 * n) / (13.0 + n)
        - 0.2720646169555415 * (-1.0 + 1 / (1.0 + n))
        - 0.0030864197530864196
        * n
        * (
            -49.613452021037574
            + 1695.6636939202713 / (1.0 + n)
            + 297.65017554444273 / (2.0 + n)
            - 53.043164791285136 / (3.0 + n)
            + (280.1816714156928 * (1.0 + (1.0 + n) * S1)) / np.power(1.0 + n, 2)
            + (566.2149227313704 * (1.0 + (2.0 + n) * (1 / (1.0 + n) + S1)))
            / np.power(2.0 + n, 2)
            - (
                115.5647471869277
                * (1.0 + (3.0 + n) * (1 / (1.0 + n) + 1 / (2.0 + n) + S1))
            )
            / np.power(3.0 + n, 2)
            - (
                1607.5136662661575
                * (
                    1.0
                    + n
                    * (1 / (1.0 + n) + (1.0 - 2.0 * (1.0 + n)) / (n * (1.0 + n)) + S1)
                )
            )
            / np.power(n, 2)
            + (
                972.0
                * (
                    1.0
                    + (2.0 + n) * (1 / (1.0 + n) + S1)
                    + np.power(2.0 + n, 2)
                    * (
                        np.power(1.0 + n, -2)
                        + S1 / (1.0 + n)
                        + 0.5 * (np.power(S1, 2) + S2)
                    )
                )
            )
            / np.power(2.0 + n, 3)
            - (
                1296.0
                * (
                    1.0
                    + (1.0 + n) * S1
                    + np.power(1.0 + n, 2)
                    * (
                        np.power(1.0 + n, -2)
                        + S1 / (1.0 + n)
                        - (1.0 * (1 / (1.0 + n) + S1)) / (1.0 + n)
                        + 0.5 * (np.power(S1, 2) + S2)
                    )
                )
            )
            / np.power(1.0 + n, 3)
            - (
                216.0
                * (
                    1.0
                    + (3.0 + n) * (1 / (1.0 + n) + 1 / (2.0 + n) + S1)
                    + np.power(3.0 + n, 2)
                    * (
                        np.power(1.0 + n, -2)
                        + np.power(2.0 + n, -2)
                        + S1 / (1.0 + n)
                        + (1 / (1.0 + n) + S1) / (2.0 + n)
                        + 0.5 * (np.power(S1, 2) + S2)
                    )
                )
            )
            / np.power(3.0 + n, 3)
            + (
                540.0
                * (
                    1.0
                    + n
                    * (1 / (1.0 + n) + (1.0 - 2.0 * (1.0 + n)) / (n * (1.0 + n)) + S1)
                    + np.power(n, 2)
                    * (
                        np.power(1.0 + n, -2)
                        + 1 / (n * (1.0 + n))
                        + S1 / (1.0 + n)
                        + ((1.0 - 2.0 * (1.0 + n)) * (1 / (1.0 + n) + S1))
                        / (n * (1.0 + n))
                        + 0.5 * (np.power(S1, 2) + S2)
                    )
                )
            )
            / np.power(n, 3)
        )
    )
