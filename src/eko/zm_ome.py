# -*- coding: utf-8 -*-
r"""
This module containse the NNLO operator-matrix elements (OMEs) for the matching condtions in ZM-VNFS :cite:`Buza_1998`.
The approzximated experessions are copied from the Pegasus Fortran code :cite:`Vogt:2004ns`:
``asg2mom.f``, `ans2mom.f``
"""
import numba as nb
import numpy as np

from . import constants
from .anomalous_dimensions import harmonics

# Global variables
zeta2 = harmonics.zeta2
zeta3 = harmonics.zeta3


@nb.njit("c16(c16,c16[:])", cache=True)
def A_ns_2(n, sx):
    """
    Implemtation of :math:`A_{qq,H}^{NS,(2)}` given in Eq. (B.4) of :cite:`Buza_1998`
    in the MS(bar) scheme for mu_f^2 = m_H^2.

    Parameters
    ----------
        N : complex
            Mellin moment
        sx : np array
            List of harmonic sums

    Returns
    -------
        A_ns_2 : numpy.ndarray
            Next-to-next-to-leading-order non singlet `A_{qq,H}^{NS,(2)}` operator-matrix element
    """

    S1 = sx[0]
    S2 = sx[1]
    S3 = sx[2]

    a_qq_2 = (
        -224.0 / 27.0 * (S1 - 1.0 / n)
        - 8.0 / 3.0 * zeta3
        + 40 / 9.0 * zeta2
        + 73.0 / 18.0
        + 44.0 / 27.0 / n
        - 268.0 / 27.0 / (n + 1.0)
        + 8.0 / 3.0 * (-1.0 / n ** 2 + 1.0 / (n + 1.0) ** 2)
        + 20.0 / 9.0 * (S2 - 1.0 / n ** 2 - zeta2 + S2 + 1.0 / (n + 1.0) ** 2 - zeta2)
        + 2.0
        / 3.0
        * (
            -2.0 * (S3 - 1.0 / n ** 3 - zeta3)
            - 2.0 * (S3 + 1.0 / (n + 1.0) ** 3 - zeta3)
        )
    )

    return constants.CF * constants.TR * a_qq_2


@nb.njit("c16(c16,c16[:])", cache=True)
def A_hq_2(n, sx):
    """
    Implemtation of :math:`A_{Hq}^{PS,(2)}` given in Eq. (B.1) of :cite:`Buza_1998`
    in the MS(bar) scheme for mu_f^2 = m_H^2.

    Parameters
    ----------
        N : complex
            Mellin moment
        sx : np array
            List of harmonic sums

    Returns
    -------
        A_hq_2 : numpy.ndarray
            Next-to-next-to-leading-order singlet `A_{Hq}^{PS,(2)}` operator-matrix element
    """

    S2 = sx[1]

    F1M = 1.0 / (n - 1.0) * (zeta2 - S2 - 1.0 / n ** 2)
    F11 = 1.0 / (n + 1.0) * (zeta2 - S2 + 1.0 / (n + 1.0) ** 2)
    F12 = 1.0 / (n + 2.0) * (zeta2 - S2 + 1.0 / (n + 1.0) ** 2 + 1.0 / (n + 2.0) ** 2)
    F21 = -(zeta2 - S2 + 1.0 / (n + 1.0) ** 2) / (n + 1.0) ** 2

    a_hq_2 = (
        -(
            32.0 / 3.0 / (n - 1.0)
            + 8.0 * (1.0 / n - 1.0 / (n + 1.0))
            - 32.0 / 3.0 * 1.0 / (n + 2.0)
        )
        * zeta2
        - 448.0 / 27.0 / (n - 1.0)
        - 4.0 / 3.0 / n
        - 124.0 / 3.0 * 1.0 / (n + 1.0)
        + 1600.0 / 27.0 / (n + 2.0)
        - 4.0 / 3.0 * (-6.0 / n ** 4 - 6.0 / (n + 1.0) ** 4)
        + 2.0 * 2.0 / n ** 3
        + 10.0 * 2.0 / (n + 1.0) ** 3
        + 16.0 / 3.0 * 2.0 / (n + 2.0) ** 3
        - 16.0 * zeta2 * (-1.0 / n ** 2 - 1.0 / (n + 1.0) ** 2)
        + 56.0 / 3.0 / n ** 2
        + 88.0 / 3.0 / (n + 1.0) ** 2
        + 448.0 / 9.0 / (n + 2.0) ** 2
        + 32.0 / 3.0 * F1M
        + 8.0 * ((zeta2 - S2) / n - F11)
        - 32.0 / 3.0 * F12
        + 16.0 * (-(zeta2 - S2) / n ** 2 + F21)
    )

    return constants.CF * constants.TR * a_hq_2


@nb.njit("c16(c16,c16[:])", cache=True)
def A_hg_2(n, sx):
    """
    Implemtation of :math:`A_{Hg}^{S,(2)}` given in Eq. (B.3) of :cite:`Buza_1998`
    in the MS(bar) scheme for mu_f^2 = m_H^2.

    Parameters
    ----------
        N : complex
            Mellin moment
        sx : np array
            List of harmonic sums

    Returns
    -------
        A_hg_2 : numpy.ndarray
            Next-to-next-to-leading-order singlet `A_{Hg}^{S,(2)}` operator-matrix element
    """

    S1 = sx[0]
    S2 = sx[1]
    S3 = sx[2]

    E2 = 2.0 / n * (zeta3 - S3 + 1.0 / n * (zeta2 - S2 - S1 / n))

    a_hg_2 = (
        -0.006
        + 1.111 * (S1 ** 3 + 3.0 * S1 * S2 + 2.0 * S3) / n
        - 0.400 * (S1 ** 2 + S2) / n
        + 2.770 * S1 / n
        - 24.89 / (n - 1.0)
        - 187.8 / n
        + 249.6 / (n + 1.0)
        + 1.556 * 6.0 / n ** 4
        - 3.292 * 2.0 / n ** 3
        + 93.68 * 1.0 / n ** 2
        - 146.8 * E2
    )

    return a_hg_2


@nb.njit("c16(c16,c16[:])", cache=True)
def A_gq_2(n, sx):
    """
    Implemtation of :math:`A_{gq,H}^{S,(2)}` given in Eq. (B.5) of :cite:`Buza_1998`
    in the MS(bar) scheme for mu_f^2 = m_H^2.

    Parameters
    ----------
        N : complex
            Mellin moment
        sx : np array
            List of harmonic sums

    Returns
    -------
        A_gq_2 : numpy.ndarray
            Next-to-next-to-leading-order singlet `A_{gq,H}^{S,(2)}` operator-matrix element
    """

    S1 = sx[0]
    S2 = sx[1]

    B2M = ((S1 - 1.0 / n) ** 2 + S2 - 1.0 / n ** 2) / (n - 1.0)
    B21 = ((S1 + 1.0 / (n + 1.0)) ** 2 + S2 + 1.0 / (n + 1.0) ** 2) / (n + 1.0)

    a_gq_2 = (
        4.0 / 3.0 * (2.0 * B2M - 2.0 * (S1 ** 2 + S2) / n + B21)
        + 8.0
        / 9.0
        * (
            -10.0 * (S1 - 1.0 / n) / (n - 1.0)
            + 10.0 * S1 / n
            - 8.0 * (S1 + 1.0 / (n + 1.0)) / (n + 1.0)
        )
        + 1.0 / 27.0 * (448.0 * (1.0 / (n - 1.0) - 1.0 / n) + 344.0 / (n + 1.0))
    )

    return constants.CF * constants.CF * a_gq_2


@nb.njit("c16(c16,c16[:])", cache=True)
def A_gg_2(n, sx):
    """
    Implemtation of :math:`A_{gg,H}^{S,(2)} ` given in Eq. (B.7) of :cite:`Buza_1998`
    in the MS(bar) scheme for mu_f^2 = m_H^2.

    Parameters
    ----------
        N : complex
            Mellin moment
        sx : np array
            List of harmonic sums

    Returns
    -------
        A_gg_2 : numpy.ndarray
            Next-to-next-to-leading-order singlet `A_{gg,H}^{S,(2)}` operator-matrix element
    """
    S1 = sx[0]

    D1 = -1.0 / n ** 2
    D11 = -1.0 / (n + 1.0) ** 2
    D2 = 2.0 / n ** 3
    D21 = 2.0 / (n + 1.0) ** 3

    a_gg_2f = (
        -15.0
        - 8.0 / (n - 1.0)
        + 80.0 / n
        - 48.0 / (n + 1.0)
        - 24.0 / (n + 2.0)
        + 4.0 / 3.0 * (-6.0 / n ** 4 - 6.0 / (n + 1.0) ** 4)
        + 6.0 * D2
        + 10.0 * D21
        + 32.0 * D1
        + 48.0 * D11
    )
    a_gg_2a = (
        -224.0 / 27.0 * (S1 - 1.0 / n)
        + 10.0 / 9.0
        + 4.0 / 3.0 * (S1 + 1.0 / (n + 1.0)) / (n + 1.0)
        + 1.0
        / 27.0
        * (556.0 / (n - 1.0) - 628.0 / n + 548.0 / (n + 1.0) - 700.0 / (n + 2.0))
        + 4.0 / 3.0 * (D2 + D21)
        + 1.0 / 9.0 * (52.0 * D1 + 88.0 * D11)
    )

    return constants.TR * (constants.CF * a_gg_2f + constants.CA * a_gg_2a)


@nb.njit("c16[:,:](c16,c16[:])", cache=True)
def A_singlet_2(n, sx):
    r"""
      Computes the next-to-next-leading-order heavy-quark singlet operator 
      matrix elements in the MS(bar) scheme for mu_f^2 = m_H^2.

      .. math::
          \A^{S,(2)} = \left(\begin{array}{cc}
            \A_{qq,H}^{NS,(2)} + \A_{hq}^{PS,(2)} & \A_{hg}^{S,(2)}\\
            \A_{gq, H}^{S,(2)} & \A_{gg, H}^{S,(2)}
          \end{array}\right)

      Parameters
      ----------
        N : complex
            Mellin moment
        sx : np array
            List of harmonic sums

      Returns
      -------
        A_S_2 : numpy.ndarray
            Next-to-next-to-leading-order heavy-quark singlet operator matrix elements :math:`\A^{S,(2)}(N)`

      See Also
      --------
        A_ns_2 : :math:`\a_{qq,H}^{NS,(2)}`
        A_hq_2 : :math:`\a_{hq}^{PS,(2)}`
        A_hg_2 : :math:`\a_{hg}^{S,(2)}`
        A_gq_2 : :math:`\a_{gq, H}^{S,(2)}`
        A_gg_2 : :math:`\a_{gg, H}^{S,(2)}`
    """
    # TODO: do we need to the NS here?? check pegasus
    A_hq = A_ns_2(n, sx) + A_hq_2(n, sx)
    A_hg = A_hg_2(n, sx)
    A_gq = A_gq_2(n, sx)
    A_gg = A_gg_2(n, sx)
    A_S_2 = np.array([[A_hq, A_hg], [A_gq, A_gg]], np.complex_)
    return A_S_2


# # * ..Some abbreviations

#        G1  = S2 - 1.0/N ** 2 - zeta2
#        G12 = S2 +1.0/(N + 1.0) ** 2 - zeta2
#        G2  = - 2.0 * ( S3 - 1.0/N ** 3 - zeta3 )
#        G22 = - 2.0 * ( S3 + 1.0/(N + 1.0) ** 3 - zeta3 )

# *
# * ..Some abbreviations
# *
#        NM = N - 1.0
#        N1 = N + 1.0
#        N2 = N + 2.0
#        NI = 1.0/N
#        NMI = 1.0/(N - 1.0)
#        N1I = 1.0/(N + 1.0)
#        N2I = 1.0/(N + 2.0)

#        S1M = S1 - 1.0/N
#        S2M = S2 - 1.0/N ** 2
#        S3M = S3 - 1.0/N ** 3
#        S11 = S1 + 1.0/(N + 1.0)
#        S21 = S2 + 1.0/(N + 1.0) ** 2
#        S31 = S3 + 1.0/(N + 1.0) ** 3
#        S22 = S2 + 1.0/(N + 1.0) ** 2 + 1.0/(N + 2.0) ** 2

#        A0  = - (S1 - 1.0/N)

#        B1  = - S1 / N
#        B1M = - (S1 - 1.0/N) / (N - 1.0)
#        B11 = - (S1 + 1.0/(N + 1.0)) / (N + 1.0)
#        B2  = ( S1 ** 2 + S2 ) / N
#        B2M = ( (S1 - 1.0/N) ** 2 + S2 - 1.0/N ** 2 ) / (N - 1.0)
#        B21 = ( (S1 + 1.0/(N + 1.0)) ** 2 +  S2 + 1.0/(N + 1.0) ** 2 ) / (N + 1.0)
#        B3  = - ( S1 ** 3 + 3.0 * S1 * S2 + 2.0 * S3) / N

#        C0 = 1.0/N
#        CM = 1.0/(N - 1.0)
#        C1 = 1.0/(N + 1.0)
#        C2 = 1.0/(N + 2.0)

#        D1  = - 1.0/N ** 2
#        D11 = - 1.0/(N + 1.0) ** 2
#        D12 = - 1.0/(N + 2.0) ** 2
#        D2  = 2.0 / N ** 3
#        D21 = 2.0 / (N + 1.0) ** 3
#        D22 = 2.0 / (N + 2.0) ** 3
#        D3  = - 6.0 / N ** 4
#        D31 = - 6.0 / (N + 1.0) ** 4

#        E2 = 2.0 / N * ( zeta3 - S3 + 1.0/N * (zeta2 - S2 - S1 / N) )

#        F1  = ( zeta2 - S2 ) / N
#        F1M = 1.0/(N - 1.0) * ( zeta2 - S2 - 1.0/N ** 2 )
#        F11 = 1.0/(N + 1.0) * ( zeta2 - S2 + 1.0/(N + 1.0) ** 2 )
#        F12 = 1.0/(N + 2.0) * ( zeta2 - S2 + 1.0/(N + 1.0) ** 2 + 1.0/(N + 2.0) ** 2 )
#        F2  = - ( zeta2 - S2 ) / N ** 2
#        F21 = - ( zeta2 - S2 + 1.0/(N + 1.0) ** 2 ) / (N + 1.0) ** 2


# * ---------------------------------------------------------------------
# *
# * ..The moments of the OME's A_Hq^{PS,(2)} and A_Hg^{S,(2)} given in
# *    Eqs. (B.1) and (B.3) of BMSN. For the latter quantity an accurate
# *    x-space parametrization is used instead of the full expression.
# *
#        A2HQ = - (32./3.D0 * CM + 8.* (C0-C1) - 32./3.D0 * C2) * ZETA(2)
#      1        - 448./27.D0 * CM - 4./3.D0 * C0 - 124./3.D0 * C1
#      2        + 1600./27.D0 * C2 - 4./3.D0 * (D3 + D31) + 2.* D2
#      3        + 10.* D21 + 16./3.D0 * D22 - 16.* ZETA(2) * (D1 + D11)
#      4        - 56./3.D0 * D1 - 88./3.D0 * D11 - 448./9.D0 * D12
#      5        + 32./3.D0 * F1M + 8.* (F1 - F11) - 32./3.D0 * F12
#      6        + 16.* (F2 + F21)
# *
#        A2HG = - 0.006 - 1.111 * B3 - 0.400 * B2 - 2.770 * B1
#      1        - 24.89 * CM - 187.8 * C0 + 249.6 * C1
#      2        - 1.556 * D3 - 3.292 * D2 - 93.68 * D1 - 146.8 * E2
# *
# * ..The moments of the OME's A_{gq,H}^{S,(2)} and A_{gg,H}^{S,(2)}
# *    given in Eqs. (B.5) and (B.7) of BMSN.
# *
#        A2GQ =   4./3.D0 * (2.* B2M - 2.* B2 + B21)
#      1        + 8./9.D0 * (10.* B1M - 10.* B1 + 8.* B11)
#      2        + 1./27.D0 * (448.* (CM - C0) + 344.* C1)
# *
#        A2GGF = - 15. - 8.* CM + 80.* C0 - 48.* C1 - 24.* C2
#      1         + 4./3.D0 * (D3 + D31) + 6.* D2 + 10.* D21 + 32.* D1
#      2         + 48.* D11
#        A2GGA =   224./27.D0 * A0 + 10./9.D0 - 4./3.D0 * B11
#      1         + 1./27.D0 * (556.* CM - 628.* C0 + 548.* C1 - 700.* C2)
#      2         + 4./3.D0 * (D2 + D21) + 1./9.D0 * (52.* D1 + 88.* D11)
# *
# * ---------------------------------------------------------------------
# *
# * ..Output to the array
# *
#        A2SG(KN,1,1) = CF*TR * A2HQ
#        A2SG(KN,1,2) = A2HG
#        A2SG(KN,2,1) = CF*TR * A2GQ
#        A2SG(KN,2,2) = TR * (CF * A2GGF + CA * A2GGA)
