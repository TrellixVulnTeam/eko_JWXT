# -*- coding: utf-8 -*-
"""
This file contains the next-to-next-to-leading-order Altarelli-Parisi splitting kernels.

These expression have been obtained from:
https://www.liverpool.ac.uk/~avogt/p2mom.f
:cite:`Moch:2004pa`.
"""
import numpy as np
import numba as nb

from . import harmonics

# pylint: disable=line-too-long

# TODO: is sign convention correct? 

# abbreviation
def e1(n):
    S1 = harmonics.harmonic_S1(n)
    S2 = harmonics.harmonic_S2(n)
    zeta2 = harmonics.zeta2

    return S1/n ** 2 + (S2 - zeta2)/n

# abbreviation
def e2(n):
    S1 = harmonics.harmonic_S1(n)
    S2 = harmonics.harmonic_S2(n)
    S3 = harmonics.harmonic_S3(n)
    zeta2 = harmonics.zeta2
    zeta3 = harmonics.zeta3

    return 2.0 * ( - S1/n ** 3 + (zeta2 - S2)/n ** 2 - (S3 - zeta3)/n )

# abbreviation for the Singlet
def e11(n):
    S1 = harmonics.harmonic_S1(n)
    S2 = harmonics.harmonic_S2(n)
    zeta2 = harmonics.zeta2

    return ( S1 + 1.0/(n + 1.0) )/(n + 1.0) ** 2 + ( S2 + 1.0/(n + 1.0) ** 2 - zeta2 )/(n + 1.0)

# abbreviation for the Singlet
def b21(n):
    S1 = harmonics.harmonic_S1(n)
    S2 = harmonics.harmonic_S2(n)

    return (( S1 + 1.0/(n + 1.0) ) ** 2 + S2 + 1.0/(n + 1.0) ** 2 )/(n + 1.0)

# abbreviation for the Singlet
def b3(n):
    S1 = harmonics.harmonic_S1(n)
    S2 = harmonics.harmonic_S2(n)
    S3 = harmonics.harmonic_S3(n)

    return - ( S1 ** 3 + 3.0 * S1 * S2 + 2.0 * S3 )/n

# abbreviation for the Singlet
def b4(n):
    S1 = harmonics.harmonic_S1(n)
    S2 = harmonics.harmonic_S2(n)
    S3 = harmonics.harmonic_S3(n)
    S4 = harmonics.harmonic_S4(n)

    return ( S1 ** 4 + 6.0 * S1 ** 2 * S2 + 8.0 * S1 * S3 + 3.0 * S2 ** 2 + 6.0 * S4 )/n

# common part for NS plus and NS minus
def pf2_nfnf(n):

    S1 = harmonics.harmonic_S1(n)
    S2 = harmonics.harmonic_S2(n)
    S3 = harmonics.harmonic_S3(n)

    res = - ( 17.0/72.0 - 2.0/27.0 * S1 - 10.0/27.0 * S2 \
        + 2.0/9.0 * S3 - ( 12.0 * n ** 4 + 2.0 * n ** 3 - 12.0 * n ** 2 \
            - 2.0 * n + 3.0 )/( 27.0 * n ** 3 * (n + 1.0) ** 3) ) * 32.0/3.0
    return res

@nb.njit("c16(c16,u1)", cache=True)
def gamma_nsm_2(n, nf: int):
    """
    Computes the next-to-next-to-leading-order valence-like non-singlet anomalous dimension.

    Implements Eq. (3.8) of :cite:`Moch:2004pa`.

    Parameters
    ----------
        n : complex
            Mellin moment
        nf : int
            Number of active flavors

    Returns
    -------
        gamma_nsm_2 : complex
            Next-to-next-to-leading-order valence-like non-singlet anomalous dimension
            :math:`\\gamma_{ns,-}^{(2)}(N)`
    """
    S1 = harmonics.harmonic_S1(n)
    E1 = e1(n)

    # The QCD colour factors have been hard-wired in the parametrizations.

    pm2 = - 1174.898 * ( S1 + 1.0/n ) + 1295.470 - 714.1 * S1/n - 433.2/(n + 3.0) \
        + 297.0/(n + 2.0) - 3505.0/(n + 1.0) + 1860.2/n - 1465.2/n ** 2 \
            + 399.2 * 2.0/n ** 3 - 320.0/9.0 * 6.0/n ** 4 - 116.0/81.0 * 6.0/(n + 1.0) ** 4 \
                + 684.0 * E1 + 251.2 * e2(n)

    pm2_nf = + 183.187 * ( S1 + 1.0/n ) - 173.933 + 5120/81.0 * S1/n \
        + 34.76/(n + 3.0) + 77.89/(n + 2.0) + 406.5/(n + 1.0) - 216.62/n \
            + 172.69/n ** 2 - 3216.0/81.0 * 2.0/n ** 3 + 256.0/81.0 * 6.0/n ** 4 \
                - 65.43 * E1 + 1.136 * 6.0/(n + 1.0) ** 4

    result = pm2 + nf * pm2_nf + nf ** 2 * pf2_nfnf(n)
    return result

@nb.njit("c16(c16,u1)", cache=True)
def gamma_nsp_2(n, nf: int):
    """
    Computes the next-to-next-to-leading-order singlet-like non-singlet anomalous dimension.

    Implements Eq. (3.7) of :cite:`Moch:2004pa`.

    Parameters
    ----------
        n : complex
            Mellin moment
        nf : int
            Number of active flavors

    Returns
    -------
        gamma_nsp_2 : complex
            Next-to-next-to-leading-order singlet-like non-singlet anomalous dimension
            :math:`\\gamma_{ns,+}^{(2)}(N)`
    """
    S1 = harmonics.harmonic_S1(n)
    E1 = e1(n)


    # The QCD colour factors have been hard-wired in the parametrizations.

    pp2 = - 1174.898 * ( S1 + 1.0/n ) + 1295.384 - 714.1 * S1/n - 522.1/(n + 3.0) \
        + 243.6/(n + 2.0) - 3135.0/(n + 1.0) + 1641.1/n - 1258.0/n ** 2 \
            + 294.9 * 2.0/n ** 3 - 800/27.0 * 6.0/n ** 4 + 128/81.0 * 24.0/n ** 5 \
                + 563.9 * E1 + 256.8 * e2(n)

    pp2_nf = + 183.187 * ( S1 + 1.0/n ) - 173.924 + 5120/81.0 * S1/n \
        + 44.79/(n + 3.0) + 72.94/(n + 2.0) + 381.1/(n + 1.0) - 197.0/n \
            + 152.6/n ** 2 - 2608.0/81.0 * 2.0/n ** 3 + 192.0/81.0 * 6.0/n ** 4 \
                - 56.66 * E1 + 1.497 * 6.0/(n + 1.0) ** 4

    result = pp2 + nf * pp2_nf + nf ** 2 * pf2_nfnf(n)
    return result

@nb.njit("c16(c16,u1)", cache=True)
def gamma_nsv_2(n, nf: int):
    """
    Computes the next-to-next-to-leading-order singlet-like non-singlet anomalous dimension.

    Implements Eq. (3.9) of :cite:`Moch:2004pa`.

    Parameters
    ----------
        n : complex
            Mellin moment
        nf : int
            Number of active flavors

    Returns
    -------
        gamma_nsv_2 : complex
            Next-to-next-to-leading-order singlet-like non-singlet anomalous dimension
            :math:`\\gamma_{ns,v}^{(2)}(N)`
    """
    S1 = harmonics.harmonic_S1(n)
    zeta2 = harmonics.zeta2


    B11 = - ( S1 + 1.0/(n + 1.0) )/(n + 1.0)
    B12 = - ( S1 + 1.0/(n + 1.0) + 1.0/(n + 2.0) )/(n + 2.0)

    # TODO: is this needed ? 
    # with special care for the first moment of x^-1 ln(1-x)
    if abs( n.imag ) < 1.0e-5 and abs( n - 1.0 ) < 1.0e-5 :
        B1M = - zeta2
    else:
        B1M = - ( S1 - 1.0/n )/(n - 1.0)

    ps2 = - 163.9 * (B1M + S1/n) - 7.208 * (B11 - B12) + 4.82 * ( 1.0/(n + 3.0) - 1.0/(n + 4.0) ) \
        - 43.12 * ( 1.0/(n + 2.0) - 1.0/(n + 3.0) ) + 44.51 * ( 1.0/(n + 1.0) - 1.0/(n + 2.0) ) + 151.49 * ( 1.0/n - 1.0/(n + 1.0) ) \
            - 178.04/n ** 2 + 6.892 * 2.0/n ** 3 - 40.0/27.0 * ( - 2.0 * 6.0/n ** 4 - 24.0/n ** 5 ) \
                - 173.1 * e1(n) + 46.18 * e2(n)

    result = gamma_nsm_2(n, nf) + nf * ps2
    return result

@nb.njit("c16(c16,u1)", cache=True)
def gamma_ps_2(n, nf: int):
    """
    Computes the next-to-next-to-leading-order pure-singlet quark-quark anomalous dimension.

    Implements Eq. (3.10) of :cite:`Vogt:2004mw`.

    Parameters
    ----------
        n : complex
            Mellin moment
        nf : int
            Number of active flavors

    Returns
    -------
        gamma_ps_2 : complex
            Next-to-next-to-leading-order pure-singlet quark-quark anomalous dimension
            :math:`\\gamma_{ps}^{(2)}(N)`
    """
    S1 = harmonics.harmonic_S1(n)
    S2 = harmonics.harmonic_S2(n)
    S3 = harmonics.harmonic_S3(n)
    E1 = e1(n)
    E11 = e1(n)
    B21 = b21(n)


    B31 = - (( S1 + 1.0/(n + 1.0)) ** 3 + 3.0 * (S1 + 1.0/(n + 1.0)) * (S2 + 1.0/(n + 1.0) ** 2) + 2.0 * (S3 + 1.0/(n + 1.0) ** 3))/(n + 1.0)

    ps1 = - 3584.0/27.0 * (- 1.0/(n - 1.0) ** 2 + 1.0/n ** 2) - 506.0 * (1.0/(n - 1.0) - 1.0/n) + 160.0/27.0 * (24.0/n ** 5 - 24.0/(n + 1.0) ** 5) \
        - 400.0/9.0 * ( - 6.0/n ** 4 + 6.0/(n + 1.0) ** 4 ) + 131.4 * (2.0/n ** 3 - 2.0/(n + 1.0) ** 3) - 661.6 * (1.0/n ** 2 + 1.0/(n + 1.0) ** 2) \
            - 5.926 * ( b3(n) - B31 ) - 9.751 * ( ( S1 ** 2 + S2 )/n - B21) - 72.11 * (- S1/n + ( S1 + 1.0/(n + 1.0) )/(n + 1.0)) \
                + 177.4 * ( 1.0/n - 1.0/(n + 1.0) ) + 392.9 * ( 1.0/(n + 1.0) - 1.0/(n + 2.0) ) - 101.4 * ( 1.0/(n + 2.0) - 1.0/(n + 3.0) ) \
                    - 57.04 * ( E1 - E11 )

    ps2 = 256.0/81.0 * (1.0/(n - 1.0) - 1.0/n) + 32.0/27.0 * (- 6.0/n ** 4 + 6.0/(n + 1.0) ** 4) + 17.89 * (2.0/n ** 3 - 2.0/(n + 1.0) ** 3) \
        + 61.75 * (- 1.0/n ** 2 + 1.0/(n + 1.0) ** 2) + 1.778 * (( S1 ** 2 + S2 )/n - B21 ) + 5.944 * (- S1/n + (S1 + 1.0/(n + 1.0))/(n + 1.0)) \
            + 100.1 * (1.0/n - 1.0/(n + 1.0)) - 125.2 * (1.0/(n + 1.0) - 1.0/(n + 2.0)) + 49.26 * (1.0/(n + 2.0) - 1.0/(n + 3.0)) \
                - 12.59 * (1.0/(n + 3.0) - 1.0/(n + 4.0)) - 1.889 * (E1 - E11)

    result = nf * ps1 + nf ** 2 * ps2
    return result

@nb.njit("c16(c16,u1)", cache=True)
def gamma_qg_2(n, nf: int):
    """
    Computes the next-to-next-to-leading-order quark-gluon singlet anomalous dimension.

    Implements Eq. (3.11) of :cite:`Vogt:2004mw`.

    Parameters
    ----------
        n : complex
            Mellin moment
        nf : int
            Number of active flavors

    Returns
    -------
        gamma_qg_2 : complex
            Next-to-next-to-leading-order quark-gluon singlet anomalous dimension
            :math:`\\gamma_{qg}^{(2)}(N)`
    """
    S1 = harmonics.harmonic_S1(n)
    S2 = harmonics.harmonic_S2(n)
    E1 = e1(n)
    E2 = e2(n)
    B3 = b3(n)

    qg1 = + 896.0/3.0/(n - 1.0) ** 2 - 1268.3/(n - 1.0) + 536.0/27.0 * 24.0/n ** 5 + 44.0/3.0 * 6.0/n ** 4 \
        + 881.5 * 2.0/n ** 3 - 424.9/n ** 2 + 100.0/27.0 * b4(n) - 70.0/9.0 * B3 \
            - 120.5 * ( S1 ** 2 + S2 )/n - 104.42 * S1/n + 2522.0/n - 3316.0/(n + 1.0) \
                + 2126.0/(n + 2.0) + 1823.0 * E1 - 25.22 * E2 + 252.5 * 6.0/(n + 1.0) ** 4

    qg2 = 1112.0/243.0/(n - 1.0) - 16.0/9.0 * 24.0/n ** 5 + 376.0/27.0 * 6.0/n ** 4 - 90.8 * 2.0/n ** 3 \
        + 254.0/n ** 2 + 20.0/27.0 * B3 + 200.0/27.0 * ( S1 ** 2 + S2 )/n + 5.496 * S1/n \
            - 252.0/n + 158.0/(n + 1.0) + 145.4/(n + 2.0) - 139.28/(n + 3.0) \
                - 53.09 * E1 - 80.616 * E2 - 98.07 * 2.0/(n + 1.0) ** 3 - 11.70 * 6.0/(n + 1.0) ** 4

    result = nf * qg1 + nf ** 2 * qg2
    return result

@nb.njit("c16(c16,u1)", cache=True)
def gamma_gq_2(n, nf: int):
    """
    Computes the next-to-next-to-leading-order gluon-quark singlet anomalous dimension.

    Implements Eq. (3.12) of :cite:`Vogt:2004mw`.

    Parameters
    ----------
        n : complex
            Mellin moment
        nf : int
            Number of active flavors

    Returns
    -------
        gamma_gq_2 : complex
            Next-to-next-to-leading-order gluon-quark singlet anomalous dimension
            :math:`\\gamma_{gq}^{(2)}(N)`
    """
    S1 = harmonics.harmonic_S1(n)
    S2 = harmonics.harmonic_S2(n)
    E1 = e1(n)
    E2 = e2(n)
    B3 = b3(n)

    gq0 = - 1189.3 * 1.0/(n - 1.0) ** 2 + 6163.1/(n - 1.0) - 4288.0/81.0 * 24.0/n ** 5 - 1568.0/9.0 * 6.0/n ** 4 \
        - 1794.0 * 2.0/n ** 3 - 4033.0 * 1.0/n ** 2 + 400.0/81.0 * b4(n) + 2200.0/27.0 * B3 \
            + 606.3 * ( S1 ** 2 + S2 )/n - 2193.0 * S1/n - 4307.0/n + 489.3/(n + 1.0) \
                + 1452.0/(n + 2.0) + 146.0/(n + 3.0) - 447.3 * E2 - 972.9 * 2.0/(n + 1.0) ** 3

    gq1 = - 71.082/(n - 1.0) ** 2 - 46.41/(n - 1.0) + 128.0/27.0 * 24.0/n ** 5 - 704/81.0 * 6.0/n ** 4 \
        + 20.39 * 2.0/n ** 3 - 174.8 * 1.0/n ** 2 - 400.0/81.0 * B3 - 68.069 * ( S1 ** 2 + S2 )/n \
            + 296.7 * S1/n - 183.8/n + 33.35/(n + 1.0) - 277.9/(n + 2.0) \
                + 108.6 * 2.0/(n + 1.0) ** 3 - 49.68 * E1

    gq2 = (64.0 * (- 1.0/(n - 1.0) + 1.0/n + 2.0/(n + 1.0)) + 320.0 * (- ( S1 - 1.0/n )/(n - 1.0) + S1/n + 0.8 * - ( S1 + 1.0/(n + 1.0) )/(n + 1.0) ) \
        + 96.0 * ((( S1 - 1.0/n ) ** 2 + S2 - 1.0/n ** 2 )/(n - 1.0) - ( S1 ** 2 + S2 )/n + 0.5 * b21(n)))/27.0

    result = gq0 + nf * gq1 + nf **2 * gq2

    return result

@nb.njit("c16(c16,u1)", cache=True)
def gamma_gg_2(n, nf: int):
    """
    Computes the next-to-next-to-leading-order gluon-gluon singlet anomalous dimension.

    Implements Eq. (3.13) of :cite:`Vogt:2004mw`.

    Parameters
    ----------
        n : complex
            Mellin moment
        nf : int
            Number of active flavors

    Returns
    -------
        gamma_gg_2 : complex
            Next-to-next-to-leading-order gluon-gluon singlet anomalous dimension
            :math:`\\gamma_{gg}^{(2)}(N)`
    """
    S1 = harmonics.harmonic_S1(n)
    E1 = e1(n)
    E2 = e2(n)

    gg0 = - 2675.8/(n - 1.0) ** 2 + 14214.0/(n - 1.0) - 144.0 * 24.0/n ** 5 - 72.0 * 6.0/n ** 4 \
        - 7471.0 * 2.0/n ** 3 - 274.4/n ** 2 - 20852.0/n + 3968.0/(n + 1.0) \
            - 3363.0/(n + 2.0) + 4848.0/(n + 3.0) + 7305.0 * E1 + 8757.0 * E2 \
                - 3589.0 * S1/n + 4425.894 - 2643.521 * ( S1 - 1.0/n )

    gg1 = - 157.27/(n - 1.0) ** 2 + 182.96/(n - 1.0) + 512.0/27.0 * 24.0/n ** 5 \
        - 832.0/9.0 * 6.0/n ** 4 + 491.3 * 2.0/n ** 3 - 1541.0/n ** 2 - 350.2/n \
            + 755.7/(n + 1.0) - 713.8/(n + 2.0)+ 559.3/(n + 3.0) + 26.15 * E1 \
                - 808.7 * E2 + 320.0 * S1/n - 528.723 + 412.172 * ( S1 - 1.0/n )

    gg2 = - 680.0/243.0/(n - 1.0) + 32.0/27.0 * 6.0/n ** 4 + 9.680 * 2.0/n ** 3 \
        + 3.422/n ** 2 - 13.878/n + 153.41/(n + 1.0) - 187.7/(n + 2.0) \
            + 52.75/(n + 3.0) - 115.6 * E1 + 85.25 * e11(n) - 63.23 * E2 \
                + 6.4630 + 16.0/9.0 * ( S1 - 1.0/n )

    result = gg0 + nf * gg1 + nf ** 2 * gg2
    return result

@nb.njit("c16[:,:](c16,u1)", cache=True)
def gamma_singlet_2(N, nf: int):
    r"""
      Computes the next-to-next-to-leading-order singlet anomalous dimension matrix

      .. math::
          \gamma_S^{(2)} = \left(\begin{array}{cc}
            \gamma_{qq}^{(2)} & \gamma_{qg}^{(2)}\\
            \gamma_{gq}^{(2)} & \gamma_{gg}^{(2)}
          \end{array}\right)

      Parameters
      ----------
        N : complex
          Mellin moment
        nf : int
          Number of active flavors

      Returns
      -------
        gamma_S_2 : numpy.ndarray
            Next-to-next-to-leading-order singlet anomalous dimension matrix :math:`\gamma_{S}^{(2)}(N)`

      See Also
      --------
        gamma_nsp_2 : :math:`\gamma_{qq}^{(2)}`
        gamma_ps_2 : :math:`\gamma_{qq}^{(2)}`
        gamma_qg_2 : :math:`\gamma_{qg}^{(2)}`
        gamma_gq_2 : :math:`\gamma_{gq}^{(2)}`
        gamma_gg_2 : :math:`\gamma_{gg}^{(2)}`
    """
    gamma_qq = gamma_nsp_2(N, nf) + gamma_ps_2(N, nf)
    gamma_qg = gamma_qg_2(N, nf)
    gamma_gq = gamma_gq_2(N, nf)
    gamma_gg = gamma_gg_2(N, nf)
    gamma_S_0 = np.array([[gamma_qq, gamma_qg], [gamma_gq, gamma_gg]], np.complex_)
    return gamma_S_0


#######################
# temp dict TO PYTHON
#######################
    #    NI = 1.0/n 
    #    NI2 = 1.0/n ** 2 
    #    NI3 = 1.0/n ** 3
    #    NM = n - 1.0
    #    NMI = 1.0/(n - 1.0)
    #    NMI2 = 1.0/(n - 1.0) ** 2 

    #    N1 = n + 1.0
    #    N1I = 1.0/(n + 1.0)
    #    N1I2 = 1.0/(n + 1.0) ** 2 
    #    N1I3 = 1.0/(n + 1.0) ** 3
    #    N2 = n + 2.0
    #    N2I = 1.0/(n + 2.0)

    #    S1M = S1 - 1.0/n 
    #    S11 = S1 + 1.0/(n + 1.0)
    #    S2M = S2 - 1.0/n ** 2 
    #    S21 = S2 + 1.0/(n + 1.0) ** 2 
    #    S31 = S3 + 1.0/(n + 1.0) ** 3

    #    A0 = - ( S1 - 1.0/n )
    #    B1 = - S1/n 
    #    B1M = - ( S1 - 1.0/n )/(n - 1.0)
    #    B11 = - ( S1 + 1.0/(n + 1.0) )/(n + 1.0)
    #    B2 = ( S1 ** 2 + S2 )/n
    #    B2M = (( S1 - 1.0/n ) ** 2 + S2 - 1.0/n ** 2 )/(n - 1.0)
    #    B21 = (( S1 + 1.0/(n + 1.0) ) ** 2 + S2 + 1.0/(n + 1.0) ** 2 )/(n + 1.0)
    #    B3 = - ( S1 ** 3 + 3.0 * S1 * S2 + 2.0 * S3 )/n 
    #    B31 = - (( S1 + 1.0/(n + 1.0)) ** 3 + 3.0 * (S1 + 1.0/(n + 1.0)) * (S2 + 1.0/(n + 1.0) ** 2) + 2.0 * (S3 + 1.0/(n + 1.0) ** 3))/(n + 1.0)
    #    B4 = ( S1 ** 4 + 6.0 * S1 ** 2 * S2 + 8.0 * S1 * S3 + 3.0 * S2 ** 2 + 6.0 * S4 )/n 

    #    C0 = 1.0/n
    #    CM = 1.0/(n - 1.0)
    #    C1 = 1.0/(n + 1.0)
    #    C2 = 1.0/(n + 2.0)
    #    C3 = 1.0/(n + 3.0)
    #    C4 = 1.0/(n + 4.0)

    #    D1 = - 1.0/n ** 2
    #    D1M = - 1.0/(n - 1.0) ** 2
    #    D11 = - 1.0/(n + 1.0) ** 2 
    #    D2 = 2.0/n ** 3
    #    D21 = 2.0/(n + 1.0) ** 3
    #    D3 = - 6.0/n ** 4
    #    D31 = - 6.0/(n + 1.0) ** 4 
    #    D4 = 24.0/n ** 5
    #    D41 = 24.0/(n + 1.0) ** 5

#######################
