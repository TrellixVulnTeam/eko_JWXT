# -*- coding: utf-8 -*-
"""
Weight 3 harmonics sum.
"""
import numba as nb

from . import g_functions as gf
from .constants import log2, zeta2, zeta3
from .polygamma import cern_polygamma


@nb.njit(cache=True)
def S3(N):
    r"""
    Computes the harmonic sum :math:`S_3(N)`.

    .. math::
      S_3(N) = \sum\limits_{j=1}^N \frac 1 {j^3} = \frac 1 2 \psi_2(N+1)+\zeta(3)

    with :math:`\psi_2(N)` the 2nd-polygamma function and :math:`\zeta` the
    Riemann zeta function.

    Parameters
    ----------
        N : complex
            Mellin moment

    Returns
    -------
        S_3 : complex
            Harmonic sum :math:`S_3(N)`

    See Also
    --------
        eko.harmonics.polygamma.cern_polygamma : :math:`\psi_k(N)`
    """
    return 0.5 * cern_polygamma(N + 1.0, 2) + zeta3


@nb.njit(cache=True)
def Sm3(N):
    r"""
    Analytic continuation of harmonic sum :math:`S_{-3}(N)`.

    .. math::
      S_{-3}(N) = \sum\limits_{j=1}^N \frac (-1)^j j^3

    Parameters
    ----------
        N : complex
            Mellin moment

    Returns
    -------
        Sm3 : complex
            Harmonic sum :math:`S_{-3}(N)`

    See Also
    --------
        eko.harmonics.w3.S3 : :math:`S_3(N)`
    """
    return (-1) ** N / 8 * (S3(N / 2) - S3((N - 1) / 2)) - 3 / 4 * zeta3


@nb.njit(cache=True)
def S21(N, S1, S2):
    r"""
    Analytic continuation of harmonic sum :math:`S_{2,1}(N)`
    as implemented in eq B.5.77 of :cite:`MuselliPhD` and eq 37 of cite:`Bl_mlein_2000`.

    Parameters
    ----------
        N : complex
            Mellin moment
        S1: complex
            Hamrmonic sum :math:`S_{1}(N)`
        S2: complex
            Hamrmonic sum :math:`S_{2}(N)`

    Returns
    -------
        S21 : complex
            Harmonic sum :math:`S_{2,1}(N)`

    See Also
    --------
        eko.harmonics.g_functions.mellin_g18 : :math:`g_18(N)`
    """
    return -gf.mellin_g18(N, S1, S2) + 2 * zeta3


@nb.njit(cache=True)
def Sm21(N, Sm1):
    r"""
    Analytic continuation of harmonic sum :math:`S_{-2,1}(N)`
    as implemented in eq B.5.75 of :cite:`MuselliPhD` and eq 22 of cite:`Bl_mlein_2000`.

    Parameters
    ----------
        N : complex
            Mellin moment
        Sm1: complex
            Hamrmonic sum :math:`S_{-1}(N)`

    Returns
    -------
        Sm21 : complex
            Harmonic sum :math:`S_{-2,1}(N)`

    See Also
    --------
        eko.harmonics.g_functions : :math:`g_3(N)`
    """
    # Note mellin g3 was integrated following x^(N-1) convention.
    return (
        -((-1) ** N) * gf.mellin_g3(N + 1) + zeta2 * Sm1 - 5 / 8 * zeta3 + zeta2 * log2
    )


@nb.njit(cache=True)
def S2m1(N, S2, Sm1, Sm2):
    r"""
    Analytic continuation of harmonic sum :math:`S_{2,-1}(N)`
    as implemented in eq B.5.76 of :cite:`MuselliPhD` and eq 23 of cite:`Bl_mlein_2000`.

    Parameters
    ----------
        N : complex
            Mellin moment
        S2: complex
            Hamrmonic sum :math:`S_{2}(N)`
        Sm1: complex
            Hamrmonic sum :math:`S_{-1}(N)`
        Sm2: complex
            Hamrmonic sum :math:`S_{-2}(N)`

    Returns
    -------
        S2m1 : complex
            Harmonic sum :math:`S_{2,-1}(N)`

    See Also
    --------
        eko.harmonics.g_functions.mellin_g4 : :math:`g_4(N)`
    """
    return (
        -((-1) ** N) * gf.mellin_g4(N)
        - log2 * (S2 - Sm2)
        - 1 / 2 * zeta2 * Sm1
        + 1 / 4 * zeta3
        - 1 / 2 * zeta2 * log2
    )


@nb.njit(cache=True)
def Sm2m1(N, S1, S2, Sm2):
    r"""
    Analytic continuation of harmonic sum :math:`S_{-2,-1}(N)`
    as implemented in eq B.5.74 of :cite:`MuselliPhD` and eq 38 of cite:`Bl_mlein_2000`.

    Parameters
    ----------
        N : complex
            Mellin moment
        S1: complex
            Hamrmonic sum :math:`S_{1}(N)`
        S2: complex
            Hamrmonic sum :math:`S_{2}(N)`
        Sm2: complex
            Hamrmonic sum :math:`S_{-2}(N)`

    Returns
    -------
        Sm2m1 : complex
            Harmonic sum :math:`S_{-2,-1}(N)`

    See Also
    --------
        eko.harmonics.g_functions.mellin_g19 : :math:`g_19(N)`
    """
    return -gf.mellin_g19(N, S1) + log2 * (S2 - Sm2) - 5 / 8 * zeta3
