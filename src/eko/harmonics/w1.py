# -*- coding: utf-8 -*-
"""
Weight 1 harmonic sums.
"""
import numba as nb
import numpy as np

from .constants import log2
from .polygamma import cern_polygamma


@nb.njit(cache=True)
def S1(N):
    r"""
    Computes the harmonic sum :math:`S_1(N)`.

    .. math::
      S_1(N) = \sum\limits_{j=1}^N \frac 1 j = \psi_0(N+1)+\gamma_E

    with :math:`\psi_0(N)` the digamma function and :math:`\gamma_E` the
    Euler-Mascheroni constant.

    Parameters
    ----------
        N : complex
            Mellin moment

    Returns
    -------
        S_1 : complex
            (simple) Harmonic sum :math:`S_1(N)`

    See Also
    --------
        eko.harmonics.polygamma.cern_polygamma : :math:`\psi_k(N)`
    """
    return cern_polygamma(N + 1.0, 0) + np.euler_gamma


@nb.njit(cache=True)
def Sm1(N):
    r"""
    Analytic continuation of harmonic sum :math:`S_{-1}(N)`.

    .. math::
      S_{-1}(N) = \sum\limits_{j=1}^N \frac {(-1)^j} j

    Parameters
    ----------
        N : complex
            Mellin moment

    Returns
    -------
        Sm1 : complex
            Harmonic sum :math:`S_{-1}(N)`

    See Also
    --------
        eko.anomalous_dimension.w1.S1 : :math:`S_1(N)`
    """
    return (-1) ** N / 2 * (S1(N / 2) - S1((N - 1) / 2)) - log2
