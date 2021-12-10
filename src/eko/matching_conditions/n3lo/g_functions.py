import numpy as np
import numba as nb

from ...anomalous_dimensions.harmonics import (
    cern_polygamma,
    harmonic_S1,
    harmonic_S2,
    harmonic_S3,
)
from ...anomalous_dimensions.harmonics import zeta2, zeta3

a1 = np.array(
    [
        0.999999974532238,
        -0.499995525889840,
        0.333203435557262,
        -0.248529457782640,
        0.191451164719161,
        -0.137466222728331,
        0.0792107412244877,
        -0.0301109656912626,
        0.00538406208663153,
        0.0000001349586745,
    ]
)

c1 = np.array(
    [
        2.2012182965269744e-8,
        2.833327652357064,
        -1.8330909624101532,
        0.7181879191200942,
        -0.0280403220046588,
        -0.181869786537805,
        0.532318519269331,
        -1.07281686995035,
        1.38194913357518,
        -1.11100841298484,
        0.506649587198046,
        -0.100672390783659,
    ]
)

c3 = np.array(
    [
        0,
        1.423616247405256,
        -0.08001203559240111,
        -0.39875367195395994,
        0.339241791547134,
        -0.0522116678353452,
        -0.0648354706049337,
        0.0644165053822532,
        -0.0394927322542075,
        0.0100879370657869,
    ]
)

p11 = np.array([11.0 / 6.0, -3.0, 3.0 / 2.0, -1.0 / 3.0])
p32 = np.array([-25.0 / 24.0, 2.0, -3.0 / 2.0, 2.0 / 3.0, -1.0 / 8.0])
p31 = np.array([205.0 / 144.0, -25.0 / 12.0, 23.0 / 24.0, -13.0 / 36.0, 1.0 / 16])


@nb.njit("c16(c16)", cache=True)
def mellin_g4(N):
    r"""
    Computes the Mellin transform of :math:`\text{Li}_2(-x)/(1+x)`.

    Implementation and defition in B.5.25 of :cite:`MuselliPhD` or
    in eq 61 of :cite:`Bl_mlein_2000`, but none of them is fully correct.


    Parameters
    ----------
        N : complex
            Mellin moment

    Returns
    -------
        mellin_g4 : complex
            Mellin transform :math:`\mathcal{M}[\text{Li}_2(-x)/(1+x)](N)`
    """
    g4 = -1 / 2 * zeta2 * np.log(2)
    for k, ak in enumerate(a1):
        Nk = N + k + 1
        beta = 1 / 2 * (harmonic_S1((Nk) / 2) - harmonic_S1((Nk - 1) / 2))
        g4 += ak * (N / Nk * zeta2 / 2 + (k + 1) / Nk ** 2 * (np.log(2) - beta))
    return g4


@nb.njit("c16(c16)", cache=True)
def mellin_g5(N):
    r"""
    Computes the Mellin transform of :math:`(\text{Li}_2(x)ln(x))/(1+x)`.

    Implementation and defition in B.5.26 of :cite:`MuselliPhD` or
    in eq 62 of :cite:`Bl_mlein_2000`, but none of them is fully correct.

    Parameters
    ----------
        N : complex
            Mellin moment

    Returns
    -------
        mellin_g5 : complex
            Mellin transform :math:`\mathcal{M}[(\text{Li}_2(x)ln(x))/(1+x)](N)`
    """
    g5 = 0.0
    for k, ak in enumerate(a1):
        Nk = N + k + 1
        g5 -= ak * (
            (k + 1)
            / Nk ** 2
            * (zeta2 + cern_polygamma(Nk + 1, 1) - 2 * harmonic_S1(Nk) / Nk)
        )
    return g5


@nb.njit("c16(c16)", cache=True)
def mellin_g6(N):
    r"""
    Computes the Mellin transform of :math:`\text{Li}_3(x)/(1+x)`.

    Implementation and defition in B.5.27 of :cite:`MuselliPhD` or
    in eq 63 of :cite:`Bl_mlein_2000`, but none of them is fully correct.

    Parameters
    ----------
        N : complex
            Mellin moment

    Returns
    -------
        mellin_g6 : complex
            Mellin transform :math:`\mathcal{M}[\text{Li}_3(x)/(1+x)](N)`


    """
    g6 = zeta3 * np.log(2)
    for k, ak in enumerate(a1):
        Nk = N + k + 1
        g6 -= ak * (N / Nk * zeta3 + (k + 1) / Nk ** 2 * (zeta2 - harmonic_S1(Nk) / Nk))
    return g6


@nb.njit("c16(c16)", cache=True)
def mellin_g8(N):
    r"""
    Computes the Mellin transform of :math:`S_{1,2}(x)/(1+x)`.

    Implementation and defition in B.5.29 of :cite:`MuselliPhD` or
    in eq 65 of :cite:`Bl_mlein_2000`, but none of them is fully correct.

    Parameters
    ----------
        N : complex
            Mellin moment

    Returns
    -------
        mellin_g8 : complex
            Mellin transform :math:`\mathcal{M}[S_{1,2}(x)/(1+x)](N)`
    """
    g8 = zeta3 * np.log(2)
    for k, ak in enumerate(a1):
        Nk = N + k + 1
        g8 -= ak * (
            N / Nk * zeta3
            + (k + 1) / Nk ** 2 * 1 / 2 * (harmonic_S1(Nk) ** 2 + harmonic_S2(Nk))
        )
    return g8


@nb.njit("c16(c16,c16,c16)", cache=True)
def mellin_g18(N, S1, S2):
    r"""
    Computes the Mellin transform of :math:`-(\text{Li}_2(x) - \zeta_2)/(1-x)`.

    Implementation and defition in eq 124 of :cite:`Bl_mlein_2000`

    Note: comparing to :cite:`Bl_mlein_2000`, we believe :cite:`MuselliPhD`
    was not changing the notations of :math:`P^{(1)}_{2}` to :math:`P^{(1)}_{1}`.
    So we implement eq 124 of :cite:`Bl_mlein_2000` but using :cite:`MuselliPhD`
    notation.

    Parameters
    ----------
        N : complex
            Mellin moment
        S1 : complex
           harmonics.harmonic_S1(N)
        S2 : complex
           harmonics.harmonic_S2(N)
    Returns
    -------
        mellin_g18 : complex
            Mellin transform :math:`\mathcal{M}[-(\text{Li}_2(x) - \zeta_2)/(1-x)](N)`
    """
    g18 = (S1 ** 2 + S2) / (N) - zeta2 * S1
    for k, ck in enumerate(c1):
        Nk = N + k
        g18 += ck * (N) / (Nk) * harmonic_S1(Nk)
    for k, p11k in enumerate(p11):
        Nk = N + k
        g18 -= p11k * (N) / (Nk) * (harmonic_S1(Nk) ** 2 + harmonic_S2(Nk))
    return g18


@nb.njit("c16(c16,c16)", cache=True)
def mellin_g19(N, S1):
    r"""
    Computes the Mellin transform of :math:`-(\text{Li}_2(-x) + \zeta_2/2)/(1-x)`.

    Implementation and defition in B.5.40 of :cite:`MuselliPhD` or in 125 of
    :cite:`Bl_mlein_2000`, but none of them is fully correct.

    Parameters
    ----------
        N : complex
            Mellin moment
        S1 : complex
           harmonics.harmonic_S1(N)

    Returns
    -------
        mellin_g19 : complex
            Mellin transform :math:`\mathcal{M}[-(\text{Li}_2(-x) + \zeta_2/2)/(1-x)](N)`
    """
    g19 = 1 / 2 * zeta2 * S1
    for k, ak in enumerate(a1):
        Nk = N + k
        g19 -= ak / (k + 1) * harmonic_S1(Nk + 1)
    return g19


@nb.njit("c16(c16,c16,c16,c16)", cache=True)
def mellin_g21(N, S1, S2, S3):
    r"""
    Computes the Mellin transform of :math:`-(S_{1,2}(x) - \zeta_3)/(1-x)`.

    Implementation and defition in B.5.42 of :cite:`MuselliPhD`

    Note: comparing to :cite:`Bl_mlein_2000`, we believe :cite:`MuselliPhD`
    was not changing the notations of :math:`P^{(3)}_{2}` to :math:`P^{(3)}_{1}`
    and :math:`P^{(3)}_{3}` to :math:`P^{(3)}_{2}`.
    So we implement eq 127 of :cite:`Bl_mlein_2000` but using :cite:`MuselliPhD`
    notation.

    Parameters
    ----------
        N : complex
            Mellin moment
        S1 : complex
           harmonics.harmonic_S1(N)
        S2 : complex
           harmonics.harmonic_S2(N)
        S3 : complex
           harmonics.harmonic_S3(N)

    Returns
    -------
        mellin_g21 : complex
            Mellin transform :math:`\mathcal{M}[-(S_{1,2}(x) - \zeta_3)/(1-x)](N)`
    """
    g21 = -zeta3 * S1 + (S1 ** 3 + 3 * S1 * S2 + 2 * S3) / (2 * N)
    for k, ck in enumerate(c3):
        Nk = N + k
        g21 += ck * N / Nk * harmonic_S1(Nk)
    for k in range(0, 5):
        Nk = N + k
        g21 += (
            N
            / Nk
            * (
                p32[k]
                * (
                    harmonic_S1(Nk) ** 3
                    + 3 * harmonic_S1(Nk) * harmonic_S2(Nk)
                    + 2 * harmonic_S3(Nk)
                )
                - p31[k] * (harmonic_S1(Nk) ** 2 + harmonic_S2(Nk))
            )
        )
    return g21


@nb.njit("c16(c16)", cache=True)
def mellin_g22(N):
    r"""
    Computes the Mellin transform of :math:`-(\text{Li}_2(x) ln(x))/(1-x)`.

    Implementation and defition in B.5.43 of :cite:`MuselliPhD`

    Note: comparing to :cite:`Bl_mlein_2000`, we believe :cite:`MuselliPhD`
    was not changing the notations of :math:`P^{(1)}_{2}` to :math:`P^{(1)}_{1}`
    So we implement eq 128 of :cite:`Bl_mlein_2000` but using :cite:`MuselliPhD`
    notation.

    Parameters
    ----------
        N : complex
            Mellin moment

    Returns
    -------
        mellin_g22 : complex
            Mellin transform :math:`\mathcal{M}[-(\text{Li}_2(x) ln(x))/(1-x)](N)`
    """
    g22 = 0.0
    for k, ck in enumerate(c1):
        Nk = N + k
        g22 += ck * cern_polygamma(Nk + 1, 1)
    for k, p11k in enumerate(p11):
        Nk = N + k
        g22 -= p11k * (
            harmonic_S1(Nk) * cern_polygamma(Nk + 1, 1)
            - 1 / 2 * cern_polygamma(Nk + 1, 2)
        )
    return g22