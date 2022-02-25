# -*- coding: utf-8 -*-
r"""
This module contains the scale variation for ``ModSV=exponentiated``.
"""
import numba as nb

from .. import beta


@nb.njit(["c16[:,:,:](c16[:,:,:],u1,u1,f8)", "c16[:](c16[:],u1,u1,f8)"], cache=True)
def gamma_variation(gamma, order, nf, L):
    """
    Adjust the anomalous dimensions with the scale variations.

    Parameters
    ----------
        gamma : numpy.ndarray
            anomalous dimensions
        order : int
            perturbation order
        nf : int
            number of active flavors
        L : float
            logarithmic ratio of factorization and renormalization scale

    Returns
    -------
        gamma : numpy.ndarray
            adjusted singlet anomalous dimensions
    """
    # since we are modifying *in-place* be carefull, that the order matters!
    # and indeed, we need to adjust the high elements first
    beta0 = beta.beta(0, nf)
    beta1 = beta.beta(1, nf)
    if order >= 3:
        gamma[3] -= (
            3 * beta0 * L * gamma[2]
            + (2 * beta1 * L - 3 * beta0**2 * L**2) * gamma[1]
            + (
                beta.beta(2, nf) * L
                - 5 / 2 * beta1 * beta0 * L**2
                + beta0**3 * L**3
            )
            * gamma[0]
        )
    if order >= 2:
        gamma[2] -= (
            2 * beta0 * gamma[1] * L + (beta1 * L - beta0**2 * L**2) * gamma[0]
        )
    if order >= 1:
        gamma[1] -= beta0 * gamma[0] * L
    return gamma