# -*- coding: utf-8 -*-
import numba as nb
import numpy as np

from . import s_functions as sf

# The expressions are based on:
# - :cite:`Bierenbaum:2009mv`. Isabella Bierenbaum, Johannes Blumlein, and Sebastian Klein. Mellin Moments of the O(alpha**3(s)) Heavy Flavor Contributions to unpolarized Deep-Inelastic Scattering at Q**2 \ensuremath >\ensuremath > m**2 and Anomalous Dimensions. Nucl. Phys. B, 820:417-482, 2009. arXiv:0904.3563, doi:10.1016/j.nuclphysb.2009.06.005. # pylint: disable=line-too-long
# - :cite:`Bl_mlein_2000`. Johannes Blümlein. Analytic continuation of mellin transforms up to two-loop order. Computer Physics Communications, 133(1):76-104, Dec 2000. URL: http://dx.doi.org/10.1016/S0010-4655(00)00156-9, doi:10.1016/s0010-4655(00)00156-9. # pylint: disable=line-too-long
# - :cite:`Bierenbaum:2009zt`. Isabella Bierenbaum, Johannes Blumlein, and Sebastian Klein. The Gluonic Operator Matrix Elements at O(alpha(s)**2) for DIS Heavy Flavor Production. Phys. Lett. B, 672:401-406, 2009. arXiv:0901.0669, doi:10.1016/j.physletb.2009.01.057. # pylint: disable=line-too-long
# - :cite:`Ablinger:2010ty`. J. Ablinger, J. Blumlein, S. Klein, C. Schneider, and F. Wissbrock. The $O(\alpha _s^3)$ Massive Operator Matrix Elements of $O(n_f)$ for the Structure Function $F_2(x,Q^2)$ and Transversity. Nucl. Phys. B, 844:26-54, 2011. arXiv:1008.3347, doi:10.1016/j.nuclphysb.2010.10.021. # pylint: disable=line-too-long
# - :cite:`Ablinger:2014vwa`. J. Ablinger, A. Behring, J. Blümlein, A. De Freitas, A. Hasselhuhn, A. von Manteuffel, M. Round, C. Schneider, and F. Wißbrock. The 3-Loop Non-Singlet Heavy Flavor Contributions and Anomalous Dimensions for the Structure Function $F_2(x,Q^2)$ and Transversity. Nucl. Phys. B, 886:733-823, 2014. arXiv:1406.4654, doi:10.1016/j.nuclphysb.2014.07.010. # pylint: disable=line-too-long
# - :cite:`Ablinger:2014uka`. J. Ablinger, J. Blümlein, A. De Freitas, A. Hasselhuhn, A. von Manteuffel, M. Round, and C. Schneider. The $O(\alpha _s^3 T_F^2)$ Contributions to the Gluonic Operator Matrix Element. Nucl. Phys. B, 885:280-317, 2014. arXiv:1405.4259, doi:10.1016/j.nuclphysb.2014.05.028. # pylint: disable=line-too-long
# - :cite:`Behring:2014eya`. A. Behring, I. Bierenbaum, J. Blümlein, A. De Freitas, S. Klein, and F. Wißbrock. The logarithmic contributions to the $O(\alpha ^3_s)$ asymptotic massive Wilson coefficients and operator matrix elements in deeply inelastic scattering. Eur. Phys. J. C, 74(9):3033, 2014. arXiv:1403.6356, doi:10.1140/epjc/s10052-014-3033-x. # pylint: disable=line-too-long
# - :cite:`Blumlein:2017wxd`. Johannes Blümlein, Jakob Ablinger, Arnd Behring, Abilio De Freitas, Andreas von Manteuffel, Carsten Schneider, and C. Schneider. Heavy Flavor Wilson Coefficients in Deep-Inelastic Scattering: Recent Results. PoS, QCDEV2017:031, 2017. arXiv:1711.07957, doi:10.22323/1.308.0031. # pylint: disable=line-too-long
# - :cite:`Ablinger_2014`. J. Ablinger, J. Blümlein, A. De Freitas, A. Hasselhuhn, A. von Manteuffel, M. Round, C. Schneider, and F. Wißbrock. The transition matrix element a_gq(n) of the variable flavor number scheme at o(α_s^3). Nuclear Physics B, 882:263-288, May 2014. URL: http://dx.doi.org/10.1016/j.nuclphysb.2014.02.007, doi:10.1016/j.nuclphysb.2014.02.007. # pylint: disable=line-too-long
# - :cite:`Ablinger_2015`. J. Ablinger, A. Behring, J. Blümlein, A. De Freitas, A. von Manteuffel, and C. Schneider. The 3-loop pure singlet heavy flavor contributions to the structure function f2(x,q2) and the anomalous dimension. Nuclear Physics B, 890:48-151, Jan 2015. URL: http://dx.doi.org/10.1016/j.nuclphysb.2014.10.008, doi:10.1016/j.nuclphysb.2014.10.008. # pylint: disable=line-too-long


@nb.njit("c16(c16,c16[:],c16[:],c16[:],c16[:],u4,f8)", cache=True)
def A_qqNS_3(n, sx, smx, s3x, s4x, nf, L):  # pylint: disable=too-many-locals
    r"""
    Computes the |N3LO| singlet |OME| :math:`A_{qq}^{NS,(3)}(N)`.
    The experssion is presented in :cite:`Bierenbaum:2009mv` and
    :cite:`Ablinger:2014vwa`.
    It contains some weight 5 harmonics sums.

    Parameters
    ----------
        n : complex
            Mellin moment
        sx : numpy.ndarray
            list S1 ... S5
        smx : numpy.ndarray
            list Sm1 ... Sm5
        s3x : numpy.ndarray
            list S21, S2m1, Sm21, Sm2m1
        s4x : numpy.ndarray
            list S31, S221, Sm22, Sm211, Sm31
        nf : int
            number of active flavor below the threshold
        L : float
            :math:`\ln(\mu_F^2 / m_h^2)`

    Returns
    -------
        A_qqNS_3 : complex
            :math:`A_{qq}^{NS,(3)}(N)`
    """
    S1, S2, S3, S4, S5 = sx[0], sx[1], sx[2], sx[3], sx[4]
    Sm1, Sm2, Sm3, Sm4, Sm5 = smx[0], smx[1], smx[2], smx[3], smx[4]
    S21, S2m1, Sm21 = s3x[0], s3x[1], s3x[2]
    S31, S211, Sm22, Sm211 = s4x[0], s4x[1], s4x[2], s4x[3]
    S41 = sf.harmonic_S41(n, S1, S2, S3)
    S311 = sf.harmonic_S311(n, S1, S2)
    S221 = sf.harmonic_S221(n, S1, S2, S21)
    Sm221 = sf.harmonic_Sm221(n, S1, Sm1, S21, Sm21)
    S21m2 = sf.harmonic_S21m2(n, S1, S2, Sm1, Sm2, Sm3, S21, Sm21, S2m1)
    S2111 = sf.harmonic_S2111(n, S1, S2, S3)
    Sm2111 = sf.harmonic_Sm2111(n, S1, S2, S3, Sm1)
    S23 = sf.harmonic_S23(n, S1, S2, S3)
    Sm23 = sf.harmonic_Sm23(n, Sm1, Sm2, Sm3)
    S2m3 = sf.harmonic_S2m3(n, S2, Sm1, Sm2, Sm3)
    a_qqNS_l0 = (
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
        + 0.3333333333333333
        * (
            (
                -0.0027434842249657062
                * (
                    -432.0
                    - 144.0 * n
                    + 2016.0 * np.power(n, 2)
                    + 4312.0 * np.power(n, 3)
                    + 11943.0 * np.power(n, 4)
                    + 28836.0 * np.power(n, 5)
                    + 36370.0 * np.power(n, 6)
                    + 21948.0 * np.power(n, 7)
                    + 5487.0 * np.power(n, 8)
                )
            )
            / (np.power(n, 4) * np.power(1.0 + n, 4))
            + 16.54869684499314 * S1
            - 19.945240467240673
            * (
                (-0.5 * (2.0 + 3.0 * n + 3.0 * np.power(n, 2))) / (n * (1.0 + n))
                + 2.0 * S1
            )
            + 0.7901234567901234 * S2
            + 3.950617283950617 * S3
            - 2.3703703703703702 * S4
        )
        + 2.0
        * (
            (
                0.09876543209876543
                * (
                    72.0
                    + 132.0 * n
                    + 101.0 * np.power(n, 2)
                    + 485.0 * np.power(n, 3)
                    + 1283.0 * np.power(n, 4)
                    + 1371.0 * np.power(n, 5)
                    + 847.0 * np.power(n, 6)
                    + 138.0 * np.power(n, 7)
                    + 39.0 * np.power(n, 8)
                )
            )
            / (np.power(n, 5) * np.power(1.0 + n, 5))
            + (
                0.0013717421124828531
                * (
                    5184.0
                    + 4752.0 * n
                    + 6336.0 * np.power(n, 2)
                    + 51804.0 * np.power(n, 3)
                    + 126914.0 * np.power(n, 4)
                    + 247433.0 * np.power(n, 5)
                    + 396657.0 * np.power(n, 6)
                    + 321746.0 * np.power(n, 7)
                    + 106856.0 * np.power(n, 8)
                    + 825.0 * np.power(n, 9)
                    + 165.0 * np.power(n, 10)
                )
            )
            / (np.power(n, 5) * np.power(1.0 + n, 5))
            - (
                0.5925925925925926
                * (
                    -12.0
                    - 10.0 * n
                    + 39.0 * np.power(n, 2)
                    + 77.0 * np.power(n, 3)
                    + 70.0 * np.power(n, 4)
                    + 9.0 * np.power(n, 5)
                    + 3.0 * np.power(n, 6)
                )
                * S1
            )
            / (np.power(n, 4) * np.power(1.0 + n, 4))
            + (
                3.5555555555555554
                * (1.0 + 2.0 * n + 2.0 * np.power(n, 2))
                * np.power(S1, 2)
            )
            / (np.power(n, 3) * np.power(1.0 + n, 3))
            + (3.5555555555555554 * (1.0 + 2.0 * n + 2.0 * np.power(n, 2)) * S2)
            / (np.power(n, 3) * np.power(1.0 + n, 3))
            - 2.3703703703703702 * np.power(S1, 3) * S2
            - (
                0.4444444444444444
                * (14.0 + 15.0 * n + 15.0 * np.power(n, 2))
                * np.power(S2, 2)
            )
            / (n * (1.0 + n))
            + 1.2020569031595942
            * (
                (
                    0.037037037037037035
                    * (
                        -432.0
                        - 682.0 * n
                        - 3505.0 * np.power(n, 2)
                        - 4278.0 * np.power(n, 3)
                        - 2103.0 * np.power(n, 4)
                        + 648.0 * np.power(n, 5)
                    )
                )
                / (np.power(n, 2) * np.power(1.0 + n, 2))
                + (
                    0.14814814814814814
                    * (108.0 + 593.0 * n + 593.0 * np.power(n, 2))
                    * S1
                )
                / (n * (1.0 + n))
                - 16.0 * np.power(S1, 2)
                + 16.0 * S2
            )
            - (
                0.8888888888888888
                * (
                    -8.0
                    - 5.0 * n
                    - 15.0 * np.power(n, 2)
                    + 18.0 * np.power(n, 3)
                    + 16.0 * np.power(n, 4)
                    + 12.0 * np.power(n, 5)
                )
                * S21
            )
            / (np.power(n, 2) * np.power(1.0 + n, 2))
            + 4.0
            * (
                (-0.5 * (2.0 + 3.0 * n + 3.0 * np.power(n, 2))) / (n * (1.0 + n))
                + 2.0 * S1
            )
            * (-15.338278920632018 - 4.0 * S211)
            + 24.88888888888889 * S2111
            - 28.444444444444443 * S21m2
            + 21.333333333333332 * S221
            - 42.666666666666664 * S23
            + 28.444444444444443 * S2m3
            - (
                0.09876543209876543
                * (
                    -36.0
                    + 144.0 * n
                    + 1151.0 * np.power(n, 2)
                    + 1573.0 * np.power(n, 3)
                    + 863.0 * np.power(n, 4)
                    + 27.0 * np.power(n, 5)
                )
                * S3
            )
            / (np.power(n, 2) * np.power(1.0 + n, 2))
            - (0.2962962962962963 * (4.0 + 13.0 * n) * (9.0 + 13.0 * n) * S31)
            / (n * (1.0 + n))
            - 28.444444444444443 * S311
            + (0.14814814814814814 * (78.0 + 443.0 * n + 443.0 * np.power(n, 2)) * S4)
            / (n * (1.0 + n))
            + 28.444444444444443 * S41
            - 24.88888888888889 * S5
            + (
                (
                    0.3950617283950617
                    * (
                        18.0
                        - 3.0 * n
                        + 82.0 * np.power(n, 2)
                        + 266.0 * np.power(n, 3)
                        + 181.0 * np.power(n, 4)
                    )
                )
                / (np.power(n, 3) * np.power(1.0 + n, 3))
                - (
                    0.7901234567901234
                    * (
                        9.0
                        + 9.0 * n
                        + 121.0 * np.power(n, 2)
                        + 224.0 * np.power(n, 3)
                        + 112.0 * np.power(n, 4)
                    )
                    * S1
                )
                / (np.power(n, 2) * np.power(1.0 + n, 2))
                + (7.111111111111111 * np.power(S1, 2)) / (n * (1.0 + n))
                - 4.7407407407407405 * np.power(S1, 3)
                + 23.703703703703702 * S2
                + 28.444444444444443 * S21
                - 9.481481481481481 * S3
            )
            * Sm2
            + S2
            * (
                (
                    0.04938271604938271
                    * (
                        72.0
                        + 63.0 * n
                        + 27.0 * np.power(n, 2)
                        + 940.0 * np.power(n, 3)
                        + 2487.0 * np.power(n, 4)
                        + 2469.0 * np.power(n, 5)
                        + 868.0 * np.power(n, 6)
                    )
                )
                / (np.power(n, 3) * np.power(1.0 + n, 3))
                - 21.333333333333332 * S21
                + 18.37037037037037 * S3
                - 42.666666666666664 * Sm21
            )
            + (
                0.7901234567901234
                * (18.0 - 39.0 * n + 112.0 * np.power(n, 2) + 112.0 * np.power(n, 3))
                * Sm21
            )
            / (np.power(n, 2) * (1.0 + n))
            + np.power(S1, 2)
            * (
                (
                    0.4444444444444444
                    * (
                        8.0
                        + 7.0 * n
                        + 3.0 * np.power(n, 2)
                        + 10.0 * np.power(n, 3)
                        + 11.0 * np.power(n, 4)
                        + 3.0 * np.power(n, 5)
                    )
                )
                / (np.power(n, 3) * np.power(1.0 + n, 3))
                + (3.5555555555555554 * S2) / (n * (1.0 + n))
                + 14.222222222222221 * S21
                - 8.88888888888889 * S3
                + 14.222222222222221 * Sm21
            )
            - (9.481481481481481 * (-3.0 + 10.0 * n + 10.0 * np.power(n, 2)) * Sm211)
            / (n * (1.0 + n))
            + 113.77777777777777 * Sm2111
            + (2.3703703703703702 * (-3.0 + 10.0 * n + 10.0 * np.power(n, 2)) * Sm22)
            / (n * (1.0 + n))
            + S1
            * (
                (
                    -0.0054869684499314125
                    * (
                        1620.0
                        + 3456.0 * n
                        + 3240.0 * np.power(n, 2)
                        + 702.0 * np.power(n, 3)
                        + 7027.0 * np.power(n, 4)
                        + 39178.0 * np.power(n, 5)
                        + 62898.0 * np.power(n, 6)
                        + 43228.0 * np.power(n, 7)
                        + 10807.0 * np.power(n, 8)
                    )
                )
                / (np.power(n, 4) * np.power(1.0 + n, 4))
                - (
                    1.7777777777777777
                    * (-1.0 + n)
                    * (-2.0 - 1.0 * n - 1.0 * np.power(n, 2) + 2.0 * np.power(n, 3))
                    * S2
                )
                / (np.power(n, 2) * np.power(1.0 + n, 2))
                + 12.444444444444445 * np.power(S2, 2)
                - (0.8888888888888888 * (16.0 + 9.0 * n + 9.0 * np.power(n, 2)) * S21)
                / (n * (1.0 + n))
                + (8.88888888888889 * np.power(1.0 + 2.0 * n, 2) * S3) / (n * (1.0 + n))
                + 21.333333333333332 * S31
                - 23.11111111111111 * S4
                + (
                    4.7407407407407405
                    * (-3.0 + 10.0 * n + 10.0 * np.power(n, 2))
                    * Sm21
                )
                / (n * (1.0 + n))
                - 56.888888888888886 * Sm211
                + 14.222222222222221 * Sm22
            )
            - 28.444444444444443 * Sm221
            - 28.444444444444443 * Sm23
            + (
                (
                    -0.3950617283950617
                    * (
                        39.0
                        + 169.0 * n
                        + 224.0 * np.power(n, 2)
                        + 112.0 * np.power(n, 3)
                    )
                )
                / (n * np.power(1.0 + n, 2))
                + (2.3703703703703702 * (3.0 + 10.0 * n + 10.0 * np.power(n, 2)) * S1)
                / (n * (1.0 + n))
                - 7.111111111111111 * np.power(S1, 2)
                - 7.111111111111111 * S2
            )
            * Sm3
            + (
                (2.3703703703703702 * (3.0 + 10.0 * n + 10.0 * np.power(n, 2)))
                / (n * (1.0 + n))
                - 14.222222222222221 * S1
            )
            * Sm4
            - 14.222222222222221 * Sm5
        )
        + 0.8888888888888888
        * (
            (
                -0.19753086419753085
                * (
                    72.0
                    + 132.0 * n
                    + 101.0 * np.power(n, 2)
                    + 485.0 * np.power(n, 3)
                    + 1283.0 * np.power(n, 4)
                    + 1371.0 * np.power(n, 5)
                    + 847.0 * np.power(n, 6)
                    + 138.0 * np.power(n, 7)
                    + 39.0 * np.power(n, 8)
                )
            )
            / (np.power(n, 5) * np.power(1.0 + n, 5))
            + (
                0.012345679012345678
                * (
                    -144.0
                    + 336.0 * n
                    + 1424.0 * np.power(n, 2)
                    + 3280.0 * np.power(n, 3)
                    - 2307.0 * np.power(n, 4)
                    - 32383.0 * np.power(n, 5)
                    - 79721.0 * np.power(n, 6)
                    - 95154.0 * np.power(n, 7)
                    - 72513.0 * np.power(n, 8)
                    - 31095.0 * np.power(n, 9)
                    - 6219.0 * np.power(n, 10)
                )
            )
            / (np.power(n, 5) * np.power(1.0 + n, 5))
            + (
                1.1851851851851851
                * (
                    -12.0
                    - 10.0 * n
                    + 39.0 * np.power(n, 2)
                    + 77.0 * np.power(n, 3)
                    + 70.0 * np.power(n, 4)
                    + 9.0 * np.power(n, 5)
                    + 3.0 * np.power(n, 6)
                )
                * S1
            )
            / (np.power(n, 4) * np.power(1.0 + n, 4))
            - (
                7.111111111111111
                * (1.0 + 2.0 * n + 2.0 * np.power(n, 2))
                * np.power(S1, 2)
            )
            / (np.power(n, 3) * np.power(1.0 + n, 3))
            + 1.2020569031595942
            * (
                (
                    0.2222222222222222
                    * (
                        48.0
                        + 302.0 * n
                        + 767.0 * np.power(n, 2)
                        + 1122.0 * np.power(n, 3)
                        + 561.0 * np.power(n, 4)
                    )
                )
                / (np.power(n, 2) * np.power(1.0 + n, 2))
                - 134.22222222222223 * S1
                - 21.333333333333332 * S2
            )
            - (7.111111111111111 * (1.0 + 2.0 * n + 2.0 * np.power(n, 2)) * S2)
            / (np.power(n, 3) * np.power(1.0 + n, 3))
            - (
                0.5925925925925926
                * (-6.0 + 31.0 * n + 31.0 * np.power(n, 2))
                * np.power(S2, 2)
            )
            / (n * (1.0 + n))
            + np.power(S1, 3)
            * (
                (-0.5925925925925926 * (1.0 + 2.0 * n))
                / (np.power(n, 2) * np.power(1.0 + n, 2))
                + 4.7407407407407405 * S2
            )
            + (
                1.7777777777777777
                * (
                    -4.0
                    - 4.0 * n
                    + 3.0 * np.power(n, 2)
                    + 14.0 * np.power(n, 3)
                    + 7.0 * np.power(n, 4)
                )
                * S21
            )
            / (np.power(n, 2) * np.power(1.0 + n, 2))
            + 4.0
            * (
                (-0.5 * (2.0 + 3.0 * n + 3.0 * np.power(n, 2))) / (n * (1.0 + n))
                + 2.0 * S1
            )
            * (17.688679036730377 + 2.6666666666666665 * S211)
            + 56.888888888888886 * S21m2
            + 28.444444444444443 * S23
            - 56.888888888888886 * S2m3
            + (
                0.09876543209876543
                * (
                    -84.0
                    + 492.0 * n
                    + 1853.0 * np.power(n, 2)
                    + 1954.0 * np.power(n, 3)
                    + 977.0 * np.power(n, 4)
                )
                * S3
            )
            / (np.power(n, 2) * np.power(1.0 + n, 2))
            + (0.5925925925925926 * (30.0 + 89.0 * n + 89.0 * np.power(n, 2)) * S31)
            / (n * (1.0 + n))
            + 28.444444444444443 * S311
            - (6.518518518518518 * (6.0 + 17.0 * n + 17.0 * np.power(n, 2)) * S4)
            / (n * (1.0 + n))
            - 56.888888888888886 * S41
            + 56.888888888888886 * S5
            + (
                (
                    -0.7901234567901234
                    * (
                        18.0
                        - 3.0 * n
                        + 82.0 * np.power(n, 2)
                        + 266.0 * np.power(n, 3)
                        + 181.0 * np.power(n, 4)
                    )
                )
                / (np.power(n, 3) * np.power(1.0 + n, 3))
                + (
                    1.5802469135802468
                    * (
                        9.0
                        + 9.0 * n
                        + 121.0 * np.power(n, 2)
                        + 224.0 * np.power(n, 3)
                        + 112.0 * np.power(n, 4)
                    )
                    * S1
                )
                / (np.power(n, 2) * np.power(1.0 + n, 2))
                - (14.222222222222221 * np.power(S1, 2)) / (n * (1.0 + n))
                + 9.481481481481481 * np.power(S1, 3)
                - 47.407407407407405 * S2
                - 56.888888888888886 * S21
                + 18.962962962962962 * S3
            )
            * Sm2
            + np.power(S1, 2)
            * (
                (
                    -0.8888888888888888
                    * (
                        2.0
                        - 7.0 * n
                        - 9.0 * np.power(n, 2)
                        + 3.0 * np.power(n, 3)
                        + 7.0 * np.power(n, 4)
                        + 2.0 * np.power(n, 5)
                    )
                )
                / (np.power(n, 3) * np.power(1.0 + n, 3))
                - (7.111111111111111 * S2) / (n * (1.0 + n))
                - 14.222222222222221 * S21
                + 21.333333333333332 * S3
                - 28.444444444444443 * Sm21
            )
            - (
                1.5802469135802468
                * (18.0 - 39.0 * n + 112.0 * np.power(n, 2) + 112.0 * np.power(n, 3))
                * Sm21
            )
            / (np.power(n, 2) * (1.0 + n))
            + S2
            * (
                (
                    -0.09876543209876543
                    * (
                        162.0
                        + 93.0 * n
                        + 31.0 * np.power(n, 2)
                        + 1595.0 * np.power(n, 3)
                        + 3433.0 * np.power(n, 4)
                        + 2718.0 * np.power(n, 5)
                        + 906.0 * np.power(n, 6)
                    )
                )
                / (np.power(n, 3) * np.power(1.0 + n, 3))
                + 9.481481481481481 * S3
                + 85.33333333333333 * Sm21
            )
            + (18.962962962962962 * (-3.0 + 10.0 * n + 10.0 * np.power(n, 2)) * Sm211)
            / (n * (1.0 + n))
            - 227.55555555555554 * Sm2111
            + S1
            * (
                (
                    0.024691358024691357
                    * (
                        -432.0
                        - 552.0 * n
                        - 424.0 * np.power(n, 2)
                        - 5824.0 * np.power(n, 3)
                        - 3497.0 * np.power(n, 4)
                        + 23272.0 * np.power(n, 5)
                        + 43326.0 * np.power(n, 6)
                        + 28632.0 * np.power(n, 7)
                        + 7131.0 * np.power(n, 8)
                    )
                )
                / (np.power(n, 4) * np.power(1.0 + n, 4))
                + (
                    0.19753086419753085
                    * (
                        45.0
                        + 54.0 * n
                        + 484.0 * np.power(n, 2)
                        + 896.0 * np.power(n, 3)
                        + 448.0 * np.power(n, 4)
                    )
                    * S2
                )
                / (np.power(n, 2) * np.power(1.0 + n, 2))
                - 7.111111111111111 * np.power(S2, 2)
                + (14.222222222222221 * S21) / (n * (1.0 + n))
                - (2.3703703703703702 * (9.0 + 40.0 * n + 40.0 * np.power(n, 2)) * S3)
                / (n * (1.0 + n))
                - 35.55555555555556 * S31
                + 78.22222222222223 * S4
                - (9.481481481481481 * (-3.0 + 10.0 * n + 10.0 * np.power(n, 2)) * Sm21)
                / (n * (1.0 + n))
                + 113.77777777777777 * Sm211
                - 28.444444444444443 * Sm22
            )
            - (4.7407407407407405 * (-3.0 + 10.0 * n + 10.0 * np.power(n, 2)) * Sm22)
            / (n * (1.0 + n))
            + 56.888888888888886 * Sm221
            + 56.888888888888886 * Sm23
            + (
                (
                    0.7901234567901234
                    * (
                        39.0
                        + 169.0 * n
                        + 224.0 * np.power(n, 2)
                        + 112.0 * np.power(n, 3)
                    )
                )
                / (n * np.power(1.0 + n, 2))
                - (4.7407407407407405 * (3.0 + 10.0 * n + 10.0 * np.power(n, 2)) * S1)
                / (n * (1.0 + n))
                + 14.222222222222221 * np.power(S1, 2)
                + 14.222222222222221 * S2
            )
            * Sm3
            + (
                (-4.7407407407407405 * (3.0 + 10.0 * n + 10.0 * np.power(n, 2)))
                / (n * (1.0 + n))
                + 28.444444444444443 * S1
            )
            * Sm4
            + 28.444444444444443 * Sm5
        )
    )
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
