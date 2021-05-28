# -*- coding: utf-8 -*-
r"""
This module contains the |NLO| |OME| (OMEs)
for the matching conditions in the |VFNS|.
Heavy quark contribution for intrinsic evolution are taken from :cite:`Ball_2016`
and Mellin transformed with Mathematica.
The other matching conditions for the |VFNS| at :math:`\mu_F^2 \neq m_H^2`
are provided in :cite:`Buza_1998` and Mellin transformed with Mathematica.
"""
import numba as nb
import numpy as np

from eko.anomalous_dimensions import harmonics
from ..constants import CF


@nb.njit("c16(c16,f8)", cache=True)
def A_hh_1(n, L):
    r"""
    |NLO| heavy-heavy |OME| :math:`A_{HH}^{(1)}` defined as the
    mellin transform of :math:`K_{hh}` given in Eq. (20a) of :cite:`Ball_2016`.

    Parameters
    ----------
        N : complex
            Mellin moment
        L : float
            :math:`\ln(\mu_F^2 / m_h^2)`

    Returns
    -------
        A_hh_1 : complex
            |NLO| heavy-heavy |OME| :math:`A_{HH}^{(1)}`
    """
    # TODO: if the harmonics are used also at nnlo we can pass them as argument
    S1m = harmonics.harmonic_S1(n - 1)
    S2m = harmonics.harmonic_S2(n - 1)
    ahh_l = L * (2 + n - 3 * n ** 2 + 4 * n * (1 + n) * S1m) / (2 * n * (1 + n))
    ahh = (
        2
        + 5 * n
        + n ** 2
        - 6 * n ** 3
        - 2 * n ** 4
        - 2 * n * (-1 - 2 * n + n ** 3) * S1m
        + 2 * (n * (1 + n)) ** 2 * (S1m ** 2 + S2m)
    ) / (n * (1 + n)) ** 2
    return -2 * CF * (ahh_l + ahh)


@nb.njit("c16(c16,f8)", cache=True)
def A_hg_1(n, L):
    r"""
    |NLO| heavy-gluon |OME| :math:`A_{Hg}^{S,(1)}` defined as the
    mellin transform of Eq. (B.2) from :cite:`Buza_1998`.

    Parameters
    ----------
        N : complex
            Mellin moment
        L : float
            :math:`\ln(\mu_F^2 / m_h^2)`

    Returns
    -------
        A_hg_1 : complex
            |NLO| heavy-gluon |OME| :math:`A_{Hg}^{S,(1)}`
    """
    den = 1.0 / (n * (n + 1) * (2 + n))
    num = 2 * (2 + n + n ** 2)
    return num * den * L


@nb.njit("c16(c16,f8)", cache=True)
def A_gh_1(n, L):
    r"""
    |NLO| gluon-heavy |OME| :math:`A_{gH}^{(1)}` defined as the
    mellin transform of :math:`K_{gh}` given in Eq. (20b) of :cite:`Ball_2016`.

    Parameters
    ----------
        n : complex
            Mellin moment
        L : float
            :math:`\ln(\mu_F^2 / m_h^2)`

    Returns
    -------
        A_hg_1 : complex
            |NLO| gluon-heavy |OME| :math:`A_{gH}^{(1)}`
    """

    den = 1.0 / (n * (n ** 2 - 1)) ** 2
    agh = -4 + n * (2 + n * (15 + n * (3 + n - n ** 2)))
    agh_l = n * (n ** 2 - 1) * (2 + n + n ** 2) * L
    return 2 * CF * den * (agh + agh_l)


@nb.njit("c16(c16,f8)", cache=True)
def A_gg_1(n, L):
    r"""
    |NLO| gluon-gluon |OME| :math:`A_{gg,H}^{S,(1)}` defined as the
    mellin transform of Eq. (B.6) from :cite:`Buza_1998`.

    Parameters
    ----------
        N : complex
            Mellin moment
        L : float
            :math:`\ln(\mu_F^2 / m_h^2)`

    Returns
    -------
        A_gg_1 : complex
            |NLO| gluon-gluon |OME| :math:`A_{gg,H}^{S,(1)}`
    """
    return -2.0 / 3.0 * L


@nb.njit("c16[:,:](c16,f8)", cache=True)
def A_singlet_1(n, L):
    r"""
      Computes the |NLO| singlet |OME|.

      .. math::
          A^{S,(1)} = \left(\begin{array}{cc}
            A_{gg,H}^{S,(1)} & 0 & 0 \\
            A_{hg}^{S,(1)} & 0 & 0 \\
            A_{hg}^{S,(1)} & 0 & 0
          \end{array}\right)

      Parameters
      ----------
        N : complex
            Mellin moment
        L : float
            :math:`\ln(\mu_F^2 / m_h^2)`

      Returns
      -------
        A_S_1 : numpy.ndarray
            |NLO| singlet |OME| :math:`A^{S,(1)}(N)`

      See Also
      --------
        A_hg_1 : :math:`A_{hg}^{S,(1)}`
        A_gg_1 : :math:`A_{gg,H}^{S,(1)}`
    """
    A_hg = A_hg_1(n, L)
    A_gg = A_gg_1(n, L)
    A_S_1 = np.array(
        [[A_gg, 0.0, 0.0], [A_hg, 0.0, 0.0], [A_hg, 0.0, 0.0]], np.complex_
    )
    return A_S_1


@nb.njit("c16[:,:](c16,f8)", cache=True)
def A_singlet_1_intrinsic(n, L):
    r"""
      Computes the |NLO| singlet |OME| with intrinsic contibution.

      .. math::
          A^{S,(1)} = \left(\begin{array}{cc}
            A_{gg,H}^{S,(1)} & 0  & A_{gH}^{(1)} \\
            A_{hg}^{S,(1)} & 0 & 0 \\
            A_{hg}^{S,(1)} & 0 & A_{HH}^{(1)}
          \end{array}\right)

      Parameters
      ----------
        N : complex
            Mellin moment
        L : float
            :math:`\ln(\mu_F^2 / m_h^2)`

      Returns
      -------
        A_S_1 : numpy.ndarray
            |NLO| singlet |OME| :math:`A^{S,(1)}(N)`

      See Also
      --------
        A_hg_1 : :math:`A_{hg}^{S,(1)}`
        A_gg_1 : :math:`A_{gg,H}^{S,(1)}`
        A_gh_1 : :math:`A_{gH}^{(1)}`
        A_hh_1 : :math:`A_{HH}^{(1)}`
    """
    A_S_1 = A_singlet_1(n, L)
    A_S_1[0, 2] = A_gh_1(n, L)
    A_S_1[2, 2] = A_hh_1(n, L)
    return A_S_1


@nb.njit("c16[:,:](c16,f8)", cache=True)
def A_ns_1_intrinsic(n, L):
    r"""
      Computes the |NLO| non-singlet |OME| with intrinsic contibutions.

      .. math::
          A^{NS,(1)} = \left(\begin{array}{cc}
            0 & 0 \\
            0 & A_{HH}^{(1)}
          \end{array}\right)

      Parameters
      ----------
        N : complex
            Mellin moment
        L : float
            :math:`\ln(\mu_F^2 / m_h^2)`
      Returns
      -------
        A_NS_1 : numpy.ndarray
            |NLO| non-singlet |OME| :math:`A^{S,(1)}(N)`

      See Also
      --------
        A_hh_1 : :math:`A_{HH}^{(1)}`
    """
    return np.array([[0 + 0j, 0 + 0j], [0 + 0j, A_hh_1(n, L)]], np.complex_)
