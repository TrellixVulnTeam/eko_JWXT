# -*- coding: utf-8 -*-
"""
Colletion of singlet EKOs.
"""

import numpy as np

import numba as nb

from .. import beta
from .. import anomalous_dimensions as ad

from . import evolution_integrals as ei
from . import utils


@nb.njit
def lo_exact(gamma_singlet, a1, a0, nf):
    """
    Singlet leading order exact EKO

    Parameters
    ----------
        gamma_singlet : numpy.ndarray
            singlet anomalous dimensions matrices
        a1 : float
            target coupling value
        a0 : float
            initial coupling value
        nf : int
            number of active flavors

    Returns
    -------
        e_s^0 : numpy.ndarray
            singlet leading order exact EKO
    """
    return ad.exp_singlet(gamma_singlet[0] * ei.j00(a1, a0, nf))[0]


@nb.njit
def nlo_decompose(gamma_singlet, a1, a0, nf, j01, j11):
    """
    Singlet next-to-leading order decompose EKO

    Parameters
    ----------
        gamma_singlet : numpy.ndarray
            singlet anomalous dimensions matrices
        a1 : float
            target coupling value
        a0 : float
            initial coupling value
        nf : int
            number of active flavors
        j01 : float
            LO-NLO evolution integral
        j11 : float
            NLO-NLO evolution integral

    Returns
    -------
        e_s^1 : numpy.ndarray
            singlet next-to-leading order decompose EKO
    """
    return ad.exp_singlet(
        gamma_singlet[0] * j01(a1, a0, nf) + gamma_singlet[1] * j11(a1, a0, nf)
    )[0]


@nb.njit
def nlo_decompose_exact(gamma_singlet, a1, a0, nf):
    """
    Singlet next-to-leading order decompose-exact EKO

    Parameters
    ----------
        gamma_singlet : numpy.ndarray
            singlet anomalous dimensions matrices
        a1 : float
            target coupling value
        a0 : float
            initial coupling value
        nf : int
            number of active flavors

    Returns
    -------
        e_s^1 : numpy.ndarray
            singlet next-to-leading order decompose-exact EKO
    """
    return nlo_decompose(gamma_singlet, a1, a0, nf, ei.j01_exact, ei.j11_exact)


@nb.njit
def nlo_decompose_expanded(gamma_singlet, a1, a0, nf):
    """
    Singlet next-to-leading order decompose-expanded EKO

    Parameters
    ----------
        gamma_singlet : numpy.ndarray
            singlet anomalous dimensions matrices
        a1 : float
            target coupling value
        a0 : float
            initial coupling value
        nf : int
            number of active flavors

    Returns
    -------
        e_s^1 : numpy.ndarray
            singlet next-to-leading order decompose-expanded EKO
    """
    return nlo_decompose(gamma_singlet, a1, a0, nf, ei.j01_expanded, ei.j11_expanded)


@nb.njit
def nlo_iterate(gamma_singlet, a1, a0, nf, ev_op_iterations):
    """
    Singlet next-to-leading order iterated (exact) EKO

    Parameters
    ----------
        gamma_singlet : numpy.ndarray
            singlet anomalous dimensions matrices
        a1 : float
            target coupling value
        a0 : float
            initial coupling value
        nf : int
            number of active flavors
        ev_op_iterations : int
            number of evolution steps

    Returns
    -------
        e_s^1 : complex
            singlet next-to-leading order iterated (exact) EKO
    """
    a_steps = utils.geomspace(a0, a1, ev_op_iterations)
    beta0 = beta.beta(0, nf)
    beta1 = beta.beta(1, nf)
    e = np.identity(2, np.complex_)
    al = a_steps[0]
    for ah in a_steps[1:]:
        a_half = (ah + al) / 2.0
        delta_a = ah - al
        ln = (
            (gamma_singlet[0] * a_half + gamma_singlet[1] * a_half ** 2)
            / (beta0 * a_half ** 2 + beta1 * a_half ** 3)
            * delta_a
        )
        ek = ad.exp_singlet(ln)[0]
        e = ek @ e
        al = ah
    return e


@nb.njit
def r_vec(gamma_singlet, nf, ev_op_max_order, is_exact):
    r"""
    Compute singlet R vector for perturbative mode.

    .. math::
        \frac{d}{da_s} \dSV{1}{a_s} &= \frac{\mathbf R (a_s)}{a_s} \cdot \dSV{1}{a_s}\\
        \mathbf R (a_s) &= \sum\limits_{k=0} a_s^k \mathbf R_{k}

    Parameters
    ----------
        gamma_singlet : numpy.ndarray
            singlet anomalous dimensions matrices
        nf : int
            number of active flavors
        ev_op_iterations : int
            number of evolution steps
        is_exact : boolean
            fill up r-vector?

    Returns
    -------
        r : np.ndarray
            R vector
    """
    r = np.zeros((ev_op_max_order + 1, 2, 2), np.complex_)  # k = 0 .. max_order
    beta0 = beta.beta(0, nf)
    b1 = beta.b(1, nf)
    # fill explicit elements
    r[0] = gamma_singlet[0] / beta0
    r[1] = gamma_singlet[1] / beta0 - b1 * r[0]
    # fill rest
    if is_exact:
        for kk in range(2, ev_op_max_order + 1):
            r[kk] = -b1 * r[kk - 1]
    return r


@nb.njit
def nlo_r_exact(gamma_singlet, nf, ev_op_max_order):
    """
    Compute singlet R vector for perturbative-exact mode.

    Parameters
    ----------
        gamma_singlet : list(numpy.ndarray)
            singlet anomalous dimensions matrices
        nf : int
            number of active flavors
        ev_op_iterations : int
            number of evolution steps

    Returns
    -------
        r : np.ndarray
            R vector

    See Also
    --------
        r_vec : compute R vector
    """
    return r_vec(gamma_singlet, nf, ev_op_max_order, True)


@nb.njit
def nlo_r_expanded(gamma_singlet, nf, ev_op_max_order):
    """
    Compute singlet R vector for perturbative-expanded mode.

    Parameters
    ----------
        gamma_singlet : list(numpy.ndarray)
            singlet anomalous dimensions matrices
        nf : int
            number of active flavors
        ev_op_iterations : int
            number of evolution steps

    Returns
    -------
        r : np.ndarray
            R vector

    See Also
    --------
        r_vec : compute R vector
    """
    return r_vec(gamma_singlet, nf, ev_op_max_order, False)


@nb.njit
def u_vec(r, ev_op_max_order):
    r"""
    Compute the elements of the singlet U vector.

    .. math::
        \ESk{n}{a_s}{a_s^0} &= \mathbf U (a_s) \ESk{0}{a_s}{a_s^0} {\mathbf U}^{-1} (a_s^0)\\
        \mathbf U (a_s) &= \mathbf I + \sum\limits_{k=1} a_s^k \mathbf U_k

    Parameters
    ----------
        r : numpy.ndarray
            singlet R vector
        ev_op_max_order : int
            perturbative expansion order of U

    Returns
    -------
        u : np.ndarray
            U vector
    """
    u = np.zeros((ev_op_max_order + 1, 2, 2), np.complex_)  # k = 0 .. max_order
    # init
    u[0] = np.identity(2, np.complex_)
    _, r_p, r_m, e_p, e_m = ad.exp_singlet(r[0])
    for kk in range(1, ev_op_max_order + 1):
        # compute R'
        rp = np.zeros((2, 2), np.complex_)
        for jj in range(kk):
            rp += r[kk - jj] @ u[jj]
        # now compose U
        u[kk] = (
            (e_m @ rp @ e_m + e_p @ rp @ e_p) / kk
            + ((e_p @ rp @ e_m) / (r_m - r_p + kk))
            + ((e_m @ rp @ e_p) / (r_p - r_m + kk))
        )
    return u


@nb.njit
def sum_u(uvec, a):
    r"""
    Sums up the actual U operator.


    .. math::
        \mathbf U (a_s) = \mathbf I + \sum\limits_{k=1} a_s^k \mathbf U_k

    Parameters
    ----------
        uvec : numpy.ndarray
            U vector (elements)
        a : float
            strong coupling

    Returns
    -------
        u : numpy.ndarray
            sum
    """
    p = 1.0
    res = np.zeros((2, 2), np.complex_)
    for uk in uvec:
        res += p * uk
        p *= a
    # alternative implementation:
    # al_vec = al**(np.arange(len(uk)))
    # ul = np.sum(al_vec * uk.T,-1).T
    return res


@nb.njit
def nlo_perturbative(
    gamma_singlet, a1, a0, nf, ev_op_iterations, ev_op_max_order, r_fnc
):
    """
    Singlet next-to-leading order pertubative EKO

    Parameters
    ----------
        gamma_singlet : numpy.ndarray
            singlet anomalous dimensions matrices
        a1 : float
            target coupling value
        a0 : float
            initial coupling value
        nf : int
            number of active flavors
        ev_op_iterations : int
            number of evolution steps
        ev_op_max_order : int
            perturbative expansion order of U
        r_fnc : callable
            getter for the R vector

    Returns
    -------
        e_s^1 : numpy.ndarray
            singlet next-to-leading order perturbative EKO
    """
    r = r_fnc(gamma_singlet, nf, ev_op_max_order)
    uk = u_vec(r, ev_op_max_order)
    e = np.identity(2, np.complex_)
    # iterate elements
    a_steps = utils.geomspace(a0, a1, ev_op_iterations)
    al = a_steps[0]
    for ah in a_steps[1:]:
        e0 = lo_exact(gamma_singlet, ah, al, nf)
        uh = sum_u(uk, ah)
        ul = sum_u(uk, al)
        # join elements
        ek = uh @ e0 @ np.linalg.inv(ul)
        e = ek @ e
        al = ah
    return e


@nb.njit
def nlo_perturbative_exact(
    gamma_singlet, a1, a0, nf, ev_op_iterations, ev_op_max_order
):
    """
    Singlet next-to-leading order pertubative-exact EKO

    Parameters
    ----------
        gamma_singlet : numpy.ndarray
            singlet anomalous dimensions matrices
        a1 : float
            target coupling value
        a0 : float
            initial coupling value
        nf : int
            number of active flavors
        ev_op_iterations : int
            number of evolution steps
        ev_op_max_order : int
            perturbative expansion order of U

    Returns
    -------
        e_s^1 : numpy.ndarray
            singlet next-to-leading order perturbative-exact EKO

    See Also
    --------
        nlo_perturbative : called function
    """
    return nlo_perturbative(
        gamma_singlet, a1, a0, nf, ev_op_iterations, ev_op_max_order, nlo_r_exact
    )


@nb.njit
def nlo_perturbative_expanded(
    gamma_singlet, a1, a0, nf, ev_op_iterations, ev_op_max_order
):
    """
    Singlet next-to-leading order pertubative-expanded EKO

    Parameters
    ----------
        gamma_singlet : numpy.ndarray
            singlet anomalous dimensions matrices
        a1 : float
            target coupling value
        a0 : float
            initial coupling value
        nf : int
            number of active flavors
        ev_op_iterations : int
            number of evolution steps
        ev_op_max_order : int
            perturbative expansion order of U

    Returns
    -------
        e_s^1 : numpy.ndarray
            singlet next-to-leading order perturbative-expanded EKO

    See Also
    --------
        nlo_perturbative : called function
    """
    return nlo_perturbative(
        gamma_singlet, a1, a0, nf, ev_op_iterations, ev_op_max_order, nlo_r_expanded
    )


@nb.njit
def nlo_truncated(gamma_singlet, a1, a0, nf, ev_op_iterations):
    """
    Singlet next-to-leading order truncated EKO

    Parameters
    ----------
        gamma_singlet : numpy.ndarray
            singlet anomalous dimensions matrices
        a1 : float
            target coupling value
        a0 : float
            initial coupling value
        nf : int
            number of active flavors
        ev_op_iterations : int
            number of evolution steps

    Returns
    -------
        e_s^1 : numpy.ndarray
            singlet next-to-leading order truncated EKO
    """
    r = nlo_r_expanded(gamma_singlet, nf, 1)
    u = u_vec(r, 1)
    e = np.identity(2, np.complex_)
    # iterate elements
    a_steps = utils.geomspace(a0, a1, ev_op_iterations)
    al = a_steps[0]
    for ah in a_steps[1:]:
        e0 = lo_exact(gamma_singlet, ah, al, nf)
        ek = e0 + ah * u[1] @ e0 - al * e0 @ u[1]
        e = ek @ e
        al = ah
    return e


def dispatcher_lo(_method):
    """
    Determine used kernel in LO.

    In LO we will always use the exact solution.

    Parameters
    ----------
        method : str
            method

    Returns
    -------
        ker : callable
            kernel
    """
    return lo_exact


def dispatcher_nlo(method):
    """
    Determine used kernel in NLO.

    Parameters
    ----------
        method : str
            method

    Returns
    -------
        ker : callable
            kernel
    """
    if method in ["iterate-exact", "iterate-expanded"]:
        return nlo_iterate
    if method == "decompose-exact":
        return nlo_decompose_exact
    if method == "decompose-expanded":
        return nlo_decompose_expanded
    if method == "perturbative-exact":
        return nlo_perturbative_exact
    if method == "perturbative-expanded":
        return nlo_perturbative_expanded
    if method in ["truncated", "ordered-truncated"]:
        return nlo_truncated
    raise ValueError(f"Unknown method: {method}")
