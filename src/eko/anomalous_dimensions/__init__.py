# -*- coding: utf-8 -*-
r"""
Contains the Altarelli-Parisi splitting kernels.

Normalization is given by

.. math::
    \mathbf{P}(x) = \sum\limits_{j=0} a_s^{j+1} \mathbf P^{(j)}(x)

with :math:`a_s = \frac{\alpha_S(\mu^2)}{4\pi}`.
The 3-loop references for the non-singlet :cite:`Moch:2004pa`
and singlet :cite:`Vogt:2004mw` case contain also the lower
order results. The results are also determined in Mellin space in
terms of the anomalous dimensions (note the additional sign!)

.. math::
    \gamma(N) = - \mathcal{M}[\mathbf{P}(x)](N)
"""

import numba as nb
import numpy as np

from .. import basis_rotation as br
from .. import constants, harmonics
from . import aem1, aem2, as1, as1aem1, as2, as3, as4


@nb.njit(cache=True)
def exp_singlet(gamma_S):
    r"""
    Compute the exponential and the eigensystem of the singlet anomalous dimension matrix.

    Parameters
    ----------
        gamma_S : numpy.ndarray
            singlet anomalous dimension matrix

    Returns
    -------
        exp : numpy.ndarray
            exponential of the singlet anomalous dimension matrix :math:`\gamma_{S}(N)`
        lambda_p : complex
            positive eigenvalue of the singlet anomalous dimension matrix
            :math:`\gamma_{S}(N)`
        lambda_m : complex
            negative eigenvalue of the singlet anomalous dimension matrix
            :math:`\gamma_{S}(N)`
        e_p : numpy.ndarray
            projector for the positive eigenvalue of the singlet anomalous
            dimension matrix :math:`\gamma_{S}(N)`
        e_m : numpy.ndarray
            projector for the negative eigenvalue of the singlet anomalous
            dimension matrix :math:`\gamma_{S}(N)`

    See Also
    --------
        eko.anomalous_dimensions.as1.gamma_singlet : :math:`\gamma_{S}^{(0)}(N)`
        eko.anomalous_dimensions.as2.gamma_singlet : :math:`\gamma_{S}^{(1)}(N)`
        eko.anomalous_dimensions.as3.gamma_singlet : :math:`\gamma_{S}^{(2)}(N)`
    """
    # compute eigenvalues
    det = np.sqrt(
        np.power(gamma_S[0, 0] - gamma_S[1, 1], 2) + 4.0 * gamma_S[0, 1] * gamma_S[1, 0]
    )
    lambda_p = 1.0 / 2.0 * (gamma_S[0, 0] + gamma_S[1, 1] + det)
    lambda_m = 1.0 / 2.0 * (gamma_S[0, 0] + gamma_S[1, 1] - det)
    # compute projectors
    identity = np.identity(2, np.complex_)
    c = 1.0 / det
    e_p = +c * (gamma_S - lambda_m * identity)
    e_m = -c * (gamma_S - lambda_p * identity)
    exp = e_m * np.exp(lambda_m) + e_p * np.exp(lambda_p)
    return exp, lambda_p, lambda_m, e_p, e_m


@nb.njit(cache=True)
def exp_matrix(gamma_S):
    r"""
    Compute the exponential and the eigensystem of the singlet anomalous dimension matrix.

    Parameters
    ----------
        gamma_S : numpy.ndarray
            singlet anomalous dimension matrix

    Returns
    -------
        exp : numpy.ndarray
            exponential of the singlet anomalous dimension matrix :math:`\gamma_{S}(N)`
        lambda_p : complex
            positive eigenvalue of the singlet anomalous dimension matrix
            :math:`\gamma_{S}(N)`
        lambda_m : complex
            negative eigenvalue of the singlet anomalous dimension matrix
            :math:`\gamma_{S}(N)`
        e_p : numpy.ndarray
            projector for the positive eigenvalue of the singlet anomalous
            dimension matrix :math:`\gamma_{S}(N)`
        e_m : numpy.ndarray
            projector for the negative eigenvalue of the singlet anomalous
            dimension matrix :math:`\gamma_{S}(N)`

    See Also
    --------
        eko.anomalous_dimensions.as1.gamma_singlet : :math:`\gamma_{S}^{(0)}(N)`
        eko.anomalous_dimensions.as2.gamma_singlet : :math:`\gamma_{S}^{(1)}(N)`
        eko.anomalous_dimensions.as3.gamma_singlet : :math:`\gamma_{S}^{(2)}(N)`
    """
    # compute Matrix of coefficients
    w, v = np.linalg.eig(gamma_S)
    vT = np.transpose(v)
    matV = vT.dot(v)
    matC = np.linalg.inv(matV)
    # compute projectors
    tmp = matC.dot(vT)
    dim = gamma_S.shape[0]
    e = np.zeros((dim, dim, dim), np.complex_)
    # TODO check if this loop can be entirely cast to numpy
    for i in range(dim):
        e[i] = np.outer(vT[i], tmp[i])
    # TODO use correct np call
    # exp = sum(e[i] * np.exp(w[i]) for i in range(dim))
    # exp = np.sum(e * np.exp(w), axis=0)
    exp = np.zeros((dim, dim), np.complex_)
    for i in range(dim):
        exp += e[i] * np.exp(w[i])
    return exp, w, e


@nb.njit(cache=True)
def gamma_ns(order, mode, n, nf):
    r"""Compute the tower of the non-singlet anomalous dimensions.

    Parameters
    ----------
    order : tuple(int,int)
        perturbative orders
    mode : 10201 | 10101 | 10200
        sector identifier
    n : complex
        Mellin variable
    nf : int
        Number of active flavors

    Returns
    -------
    numpy.ndarray
        non-singlet anomalous dimensions

    See Also
    --------
    eko.anomalous_dimensions.as1.gamma_ns : :math:`\gamma_{ns}^{(0)}(N)`
    eko.anomalous_dimensions.as2.gamma_nsp : :math:`\gamma_{ns,+}^{(1)}(N)`
    eko.anomalous_dimensions.as2.gamma_nsm : :math:`\gamma_{ns,-}^{(1)}(N)`
    eko.anomalous_dimensions.as3.gamma_nsp : :math:`\gamma_{ns,+}^{(2)}(N)`
    eko.anomalous_dimensions.as3.gamma_nsm : :math:`\gamma_{ns,-}^{(2)}(N)`
    eko.anomalous_dimensions.as3.gamma_nsv : :math:`\gamma_{ns,v}^{(2)}(N)`
    eko.anomalous_dimensions.as4.gamma_nsp : :math:`\gamma_{ns,+}^{(3)}(N)`
    eko.anomalous_dimensions.as4.gamma_nsm : :math:`\gamma_{ns,-}^{(3)}(N)`
    eko.anomalous_dimensions.as4.gamma_nsv : :math:`\gamma_{ns,v}^{(3)}(N)`

    """
    # cache the s-es
    if order[0] >= 4:
        full_sx_cache = harmonics.compute_cache(n, 5, is_singlet=False)
        sx = np.array(
            [
                full_sx_cache[0][0],
                full_sx_cache[1][0],
                full_sx_cache[2][0],
                full_sx_cache[3][0],
            ]
        )
    else:
        sx = harmonics.sx(n, max_weight=order[0] + 1)
    # now combine
    gamma_ns = np.zeros(order[0], np.complex_)
    gamma_ns[0] = as1.gamma_ns(n, sx[0])
    # NLO and beyond
    if order[0] >= 2:
        if mode == 10101:
            gamma_ns_1 = as2.gamma_nsp(n, nf, sx)
        # To fill the full valence vector in NNLO we need to add gamma_ns^1 explicitly here
        elif mode in [10201, 10200]:
            gamma_ns_1 = as2.gamma_nsm(n, nf, sx)
        else:
            raise NotImplementedError("Non-singlet sector is not implemented")
        gamma_ns[1] = gamma_ns_1
    # NNLO and beyond
    if order[0] >= 3:
        if mode == 10101:
            gamma_ns_2 = as3.gamma_nsp(n, nf, sx)
        elif mode == 10201:
            gamma_ns_2 = as3.gamma_nsm(n, nf, sx)
        elif mode == 10200:
            gamma_ns_2 = as3.gamma_nsv(n, nf, sx)
        gamma_ns[2] = gamma_ns_2
    # N3LO
    if order[0] >= 4:
        if mode == 10101:
            gamma_ns_3 = as4.gamma_nsp(n, nf, full_sx_cache)
        elif mode == 10201:
            gamma_ns_3 = as4.gamma_nsm(n, nf, full_sx_cache)
        elif mode == 10200:
            gamma_ns_3 = as4.gamma_nsv(n, nf, full_sx_cache)
        gamma_ns[3] = gamma_ns_3
    return gamma_ns


@nb.njit(cache=True)
def gamma_singlet(order, n, nf):
    r"""Compute the tower of the singlet anomalous dimensions matrices.

    Parameters
    ----------
    order : tuple(int,int)
        perturbative orders
    n : complex
        Mellin variable
    nf : int
        Number of active flavors

    Returns
    -------
    numpy.ndarray
        singlet anomalous dimensions matrices

    See Also
    --------
    eko.anomalous_dimensions.as1.gamma_singlet : :math:`\gamma_{S}^{(0)}(N)`
    eko.anomalous_dimensions.as2.gamma_singlet : :math:`\gamma_{S}^{(1)}(N)`
    eko.anomalous_dimensions.as3.gamma_singlet : :math:`\gamma_{S}^{(2)}(N)`
    eko.anomalous_dimensions.as4.gamma_singlet : :math:`\gamma_{S}^{(3)}(N)`

    """
    # cache the s-es
    if order[0] >= 4:
        full_sx_cache = harmonics.compute_cache(n, 5, is_singlet=False)
        sx = np.array(
            [
                full_sx_cache[0][0],
                full_sx_cache[1][0],
                full_sx_cache[2][0],
                full_sx_cache[3][0],
            ]
        )
    elif order[0] >= 3:
        # here we need only S1,S2,S3,S4
        sx = harmonics.sx(n, max_weight=order[0] + 1)
    else:
        sx = harmonics.sx(n, max_weight=order[0])

    gamma_s = np.zeros((order[0], 2, 2), np.complex_)
    gamma_s[0] = as1.gamma_singlet(n, sx[0], nf)
    if order[0] >= 2:
        gamma_s[1] = as2.gamma_singlet(n, nf, sx)
    if order[0] >= 3:
        gamma_s[2] = as3.gamma_singlet(n, nf, sx)
    if order[0] >= 4:
        gamma_s[3] = as4.gamma_singlet(n, nf, full_sx_cache)
    return gamma_s


@nb.njit(cache=True)
def gamma_ns_qed(order, mode, n, nf):
    r"""
    Compute the tower of the non-singlet anomalous dimensions.

    Parameters
    ----------
        order : tuple(int,int)
            perturbative orders
        mode : 10201 | 10101 | 10200
            sector identifier
        n : complex
            Mellin variable
        nf : int
            Number of active flavors

    Returns
    -------
        gamma_ns : numpy.ndarray
            non-singlet anomalous dimensions

    See Also
    --------
        eko.anomalous_dimensions.as1.gamma_ns : :math:`\gamma_{ns}^{(0)}(N)`
        eko.anomalous_dimensions.as2.gamma_nsp : :math:`\gamma_{ns,+}^{(1)}(N)`
        eko.anomalous_dimensions.as2.gamma_nsm : :math:`\gamma_{ns,-}^{(1)}(N)`
        eko.anomalous_dimensions.as3.gamma_nsp : :math:`\gamma_{ns,+}^{(2)}(N)`
        eko.anomalous_dimensions.as3.gamma_nsm : :math:`\gamma_{ns,-}^{(2)}(N)`
        eko.anomalous_dimensions.as3.gamma_nsv : :math:`\gamma_{ns,v}^{(2)}(N)`
    """
    # cache the s-es
    max_weight = max(order)
    if max_weight >= 3:
        # here we need only S1,S2,S3,S4
        sx = harmonics.sx(n, max_weight=max_weight + 1)
    else:
        sx = harmonics.sx(n, max_weight=3)
    # now combine
    gamma_ns = np.zeros((order[0] + 1, order[1] + 1), np.complex_)
    if order[0] >= 1:
        gamma_ns[1, 0] = as1.gamma_ns(n, sx[0])
    if order[1] >= 1:
        gamma_ns[0, 1] = e2(mode) * aem1.gamma_ns(n, sx)
    if order[0] >= 1 and order[1] >= 1:
        if mode in [10102, 10103]:
            gamma_ns[1, 1] = e2(mode) * as1aem1.gamma_nsp(n, sx)
        elif mode in [10202, 10203]:
            gamma_ns[1, 1] = e2(mode) * as1aem1.gamma_nsm(n, sx)
    # NLO and beyond
    if order[0] >= 2:
        if mode in [10102, 10103]:
            gamma_ns[2, 0] = as2.gamma_nsp(n, nf, sx)
        # To fill the full valence vector in NNLO we need to add gamma_ns^1 explicitly here
        elif mode in [10202, 10203]:
            gamma_ns[2, 0] = as2.gamma_nsm(n, nf, sx)
        else:
            raise NotImplementedError("Non-singlet sector is not implemented")
    if order[1] >= 2:
        if mode == 10102:
            gamma_ns[0, 2] = constants.eu2 * aem2.gamma_nspu(n, nf, sx)
        if mode == 10103:
            gamma_ns[0, 2] = constants.ed2 * aem2.gamma_nspd(n, nf, sx)
        if mode == 10202:
            gamma_ns[0, 2] = constants.eu2 * aem2.gamma_nsmu(n, nf, sx)
        if mode == 10203:
            gamma_ns[0, 2] = constants.ed2 * aem2.gamma_nsmd(n, nf, sx)
    # NNLO and beyond
    if order[0] >= 3:
        if mode in [10102, 10103]:
            gamma_ns[3, 0] = as3.gamma_nsp(n, nf, sx)
        elif mode in [10202, 10203]:
            gamma_ns[3, 0] = as3.gamma_nsm(n, nf, sx)
    return gamma_ns


def e2(mode):
    r"""
    Compute the charge of a given non-singlet mode.

    Parameters
    ----------
        mode : int
            evolution mode

    Returns
    -------
        charge : float
            charge of selected mode
    """
    if mode in [br.non_singlet_pids_map["ns-u"], br.non_singlet_pids_map["ns+u"]]:
        return constants.eu2
    elif mode in [br.non_singlet_pids_map["ns-d"], br.non_singlet_pids_map["ns+d"]]:
        return constants.ed2
    else:
        raise NotImplementedError("Non-singlet sector is not implemented")


@nb.njit(cache=True)
def gamma_singlet_qed(order, n, nf):
    r"""
    Compute the tower of the singlet anomalous dimensions matrices.

    Parameters
    ----------
        order : tuple(int,int)
            perturbative orders
        n : complex
            Mellin variable
        nf : int
            Number of active flavors

    Returns
    -------
        gamma_singlet : numpy.ndarray
            singlet anomalous dimensions matrices

    See Also
    --------
        eko.anomalous_dimensions.as1.gamma_singlet : :math:`\gamma_{S}^{(0)}(N)`
        eko.anomalous_dimensions.as2.gamma_singlet : :math:`\gamma_{S}^{(1)}(N)`
        eko.anomalous_dimensions.as3.gamma_singlet : :math:`\gamma_{S}^{(2)}(N)`
    """
    # cache the s-es
    max_weight = max(order)
    if max_weight >= 3:
        # here we need only S1,S2,S3,S4
        sx = harmonics.sx(n, max_weight=max_weight + 1)
    else:
        sx = harmonics.sx(n, max_weight=3)
    gamma_s = np.zeros((order[0] + 1, order[1] + 1, 4, 4), np.complex_)
    if order[0] >= 1:
        gamma_s[1, 0] = as1.gamma_QEDsinglet(n, sx[0], nf)
    if order[1] >= 1:
        gamma_s[0, 1] = aem1.gamma_singlet(n, nf, sx)
    if order[0] >= 1 and order[1] >= 1:
        gamma_s[1, 1] = as1aem1.gamma_singlet(n, nf, sx)
    if order[0] >= 2:
        gamma_s[2, 0] = as2.gamma_QEDsinglet(n, nf, sx)
    if order[1] >= 2:
        gamma_s[0, 2] = aem2.gamma_singlet(n, nf, sx)
    if order[0] == 3:
        gamma_s[3, 0] = as3.gamma_QEDsinglet(n, nf, sx)
    return gamma_s


@nb.njit(cache=True)
def gamma_valence_qed(order, n, nf):
    r"""
    Compute the tower of the singlet anomalous dimensions matrices.

    Parameters
    ----------
        order : tuple(int,int)
            perturbative orders
        n : complex
            Mellin variable
        nf : int
            Number of active flavors

    Returns
    -------
        gamma_singlet : numpy.ndarray
            singlet anomalous dimensions matrices

    See Also
    --------
        eko.anomalous_dimensions.as1.gamma_singlet : :math:`\gamma_{S}^{(0)}(N)`
        eko.anomalous_dimensions.as2.gamma_singlet : :math:`\gamma_{S}^{(1)}(N)`
        eko.anomalous_dimensions.as3.gamma_singlet : :math:`\gamma_{S}^{(2)}(N)`
    """
    # cache the s-es
    max_weight = max(order)
    max_weight = max(order)
    if max_weight >= 3:
        # here we need only S1,S2,S3,S4
        sx = harmonics.sx(n, max_weight=max_weight + 1)
    else:
        sx = harmonics.sx(n, max_weight=3)
    gamma_v = np.zeros((order[0] + 1, order[1] + 1, 2, 2), np.complex_)
    if order[0] >= 1:
        gamma_v[1, 0] = as1.gamma_QEDvalence(n, sx[0])
    if order[1] >= 1:
        gamma_v[0, 1] = aem1.gamma_valence(n, nf, sx)
    if order[0] >= 1 and order[1] >= 1:
        gamma_v[1, 1] = as1aem1.gamma_valence(n, nf, sx)
    if order[0] >= 2:
        gamma_v[2, 0] = as2.gamma_QEDvalence(n, nf, sx)
    if order[1] >= 2:
        gamma_v[0, 2] = aem2.gamma_valence(n, nf, sx)
    if order[0] == 3:
        sx = np.append(sx, harmonics.S4(n))
        gamma_v[3, 0] = as3.gamma_QEDvalence(n, nf, sx)
    return gamma_v
