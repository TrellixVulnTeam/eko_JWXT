# -*- coding: utf-8 -*-
"""
This module defines the |OME| for the non-trivial matching conditions in the
|VFNS| evolution.
"""

import functools
import logging
import multiprocessing
import os
import time

import numba as nb
import numpy as np
from scipy import integrate

from .. import basis_rotation as br
from ..anomalous_dimensions import harmonics
from ..evolution_operator import QuadKerBase
from ..member import OpMember
from . import n3lo, nlo, nnlo
from .n3lo import s_functions

logger = logging.getLogger(__name__)


@nb.njit("c16[:](c16)", cache=True)
def get_smx(n):
    """Get the S-minus cache"""
    return np.array(
        [
            s_functions.harmonic_Sm1(n),
            s_functions.harmonic_Sm2(n),
            s_functions.harmonic_Sm3(n),
            s_functions.harmonic_Sm4(n),
            s_functions.harmonic_Sm5(n),
        ]
    )


@nb.njit("c16[:](c16,c16[:],c16[:])", cache=True)
def get_s3x(n, sx, smx):
    """Get the S-w3 cache"""
    return np.array(
        [
            s_functions.harmonic_S21(n, sx[0], sx[1]),
            s_functions.harmonic_S2m1(n, sx[1], smx[0], smx[1]),
            s_functions.harmonic_Sm21(n, smx[0]),
            s_functions.harmonic_Sm2m1(n, sx[0], sx[1], smx[1]),
        ]
    )


@nb.njit("c16[:](c16,c16[:],c16[:])", cache=True)
def get_s4x(n, sx, smx):
    """Get the S-w4 cache"""
    Sm31 = s_functions.harmonic_Sm31(n, smx[0], smx[1])
    return np.array(
        [
            s_functions.harmonic_S31(n, sx[1], sx[3]),
            s_functions.harmonic_S211(n, sx[0], sx[1], sx[2]),
            s_functions.harmonic_Sm22(n, Sm31),
            s_functions.harmonic_Sm211(n, smx[0]),
            s_functions.harmonic_Sm31(n, smx[0], smx[1]),
        ]
    )


@nb.njit("c16[:,:,:](u1,c16,c16[:],u4,f8,b1)", cache=True)
def A_singlet(order, n, sx, nf, L, is_msbar):
    r"""
    Computes the tower of the singlet |OME|.

    Parameters
    ----------
        order : int
            perturbative order
        n : complex
            Mellin variable
        sx : numpy.ndarray
            List of harmonic sums
        nf: int
            number of active flavor below threshold
        L : float
            :math:`log(q^2/m_h^2)`
        is_msbar: bool
            add the |MSbar| contribution

    Returns
    -------
        A_singlet : numpy.ndarray
            singlet |OME|

    See Also
    --------
        eko.matching_conditions.nlo.A_singlet_1 : :math:`A^{S,(1)}(N)`
        eko.matching_conditions.nlo.A_hh_1 : :math:`A_{HH}^{(1)}(N)`
        eko.matching_conditions.nlo.A_gh_1 : :math:`A_{gH}^{(1)}(N)`
        eko.matching_conditions.nnlo.A_singlet_2 : :math:`A_{S,(2)}(N)`
    """
    if order == 0:
        return np.zeros((1, 3, 3), np.complex_)
    A_s = np.zeros((order, 3, 3), np.complex_)
    if order >= 1:
        A_s[0] = nlo.A_singlet_1(n, sx, L)
    if order >= 2:
        A_s[1] = nnlo.A_singlet_2(n, sx, L, is_msbar)
    if order >= 3:
        A_s[2] = n3lo.A_singlet_3(n, sx, nf, L)
    return A_s


@nb.njit("c16[:,:,:](u1,c16,c16[:],u4,f8)", cache=True)
def A_non_singlet(order, n, sx, nf, L):
    r"""
    Computes the tower of the non-singlet |OME|

    Parameters
    ----------
        order : int
            perturbative order
        n : complex
            Mellin variable
        sx : numpy.ndarray
            List of harmonic sums
        nf: int
            number of active flavor below threshold
        L : float
            :math:`log(q^2/m_h^2)`

    Returns
    -------
        A_non_singlet : numpy.ndarray
            non-singlet |OME|

    See Also
    --------
        eko.matching_conditions.nlo.A_hh_1 : :math:`A_{HH}^{(1)}(N)`
        eko.matching_conditions.nnlo.A_ns_2 : :math:`A_{qq,H}^{NS,(2)}`
    """
    if order == 0:
        return np.zeros((1, 2, 2), np.complex_)
    A_ns = np.zeros((order, 2, 2), np.complex_)
    if order >= 1:
        A_ns[0] = nlo.A_ns_1(n, sx, L)
    if order >= 2:
        A_ns[1] = nnlo.A_ns_2(n, sx, L)
    if order >= 3:
        A_ns[2] = n3lo.A_ns_3(n, sx, nf, L)
    print(A_ns)
    return A_ns


@nb.njit("c16[:,:](c16[:,:,:],u4,f8,string)", cache=True)
def build_ome(A, order, a_s, backward_method):
    r"""
    Construct the matching expansion in :math:`a_s` with the appropriate method.

    Parameters
    ----------
        A : numpy.ndarray
            list of |OME|
        order : int
            perturbation order
        a_s : float
            strong coupling, needed only for the exact inverse
        backward_method : ["exact", "expanded" or ""]
            empty or method for inverting the matching condition (exact or expanded)

    Returns
    -------
        ome : numpy.ndarray
            matching operator matrix
    """
    # to get the inverse one can use this FORM snippet
    # Symbol a;
    # NTensor c,d,e;
    # Local x=-(a*c+a**2* d + a**3 * e);
    # Local bi = 1+x+x**2+x**3;
    # Print;
    # .end
    ome = np.eye(len(A[0]), dtype=np.complex_)
    A = np.ascontiguousarray(A)
    if backward_method == "expanded":
        # expended inverse
        if order >= 1:
            ome -= a_s * A[0]
        if order >= 2:
            ome += a_s**2 * (-A[1] + A[0] @ A[0])
        if order >= 3:
            ome += a_s**3 * (-A[2] + A[0] @ A[1] + A[1] @ A[0] - A[0] @ A[0] @ A[0])
    else:
        # forward or exact inverse
        if order >= 1:
            ome += a_s * A[0]
        if order >= 2:
            ome += a_s**2 * A[1]
        if order >= 3:
            ome += a_s**3 * A[2]
        # need inverse exact ?  so add the missing pieces
        if backward_method == "exact":
            ome = np.linalg.inv(ome)
    return ome


@nb.njit("f8(f8,u1,u2,u2,b1,f8,f8[:,:],f8,u1,f8,string,b1)", cache=True)
def quad_ker(
    u, order, mode0, mode1, is_log, logx, areas, a_s, nf, L, backward_method, is_msbar
):
    """
    Raw kernel inside quad

    Parameters
    ----------
        u : float
            quad argument
        order : int
            perturbation order
        mode0 : int
            pid for first element in the singlet sector
        mode1 : int
            pid for second element in the singlet sector
        is_log : boolean
            logarithmic interpolation
        logx : float
            Mellin inversion point
        areas : tuple
            basis function configuration
        a_s : float
            strong coupling, needed only for the exact inverse
        nf: int
            number of active flavor below threshold
        L : float
            :math:`log(q^2/m_h^2)`
        backward_method : ["exact", "expanded" or ""]
            empty or method for inverting the matching condition (exact or expanded)
        is_msbar: bool
            add the |MSbar| contribution
    Returns
    -------
        ker : float
            evaluated integration kernel
    """
    ker_base = QuadKerBase(u, is_log, logx, mode0)
    integrand = ker_base.integrand(areas)
    if integrand == 0.0:
        return 0.0

    # compute the harmonics
    sx = np.zeros(3, np.complex_)
    if order >= 1:
        sx = np.array(
            [harmonics.harmonic_S1(ker_base.n), harmonics.harmonic_S2(ker_base.n)]
        )
    if order >= 2:
        sx = np.append(sx, harmonics.harmonic_S3(ker_base.n))
    if order >= 3:
        sx = np.append(sx, harmonics.harmonic_S4(ker_base.n))
        sx = np.append(sx, harmonics.harmonic_S5(ker_base.n))
        smx = get_smx(ker_base.n)
        sx = np.append(sx, smx)
        sx = np.append(sx, get_s3x(ker_base.n, sx, smx))
        sx = np.append(sx, get_s4x(ker_base.n, sx, smx))
    # compute the ome
    if ker_base.is_singlet:
        indices = {21: 0, 100: 1, 90: 2}
        A = A_singlet(order, ker_base.n, sx, nf, L, is_msbar)
    else:
        indices = {200: 0, 91: 1}
        A = A_non_singlet(order, ker_base.n, sx, nf, L)

    # build the expansion in alpha_s depending on the strategy
    ker = build_ome(A, order, a_s, backward_method)

    # select the needed matrix element
    ker = ker[indices[mode0], indices[mode1]]

    # recombine everthing
    return np.real(ker * integrand)


def run_op_integration(
    log_grid,
    int_disp,
    grid_size,
    labels,
    order,
    is_log,
    a_s,
    nf,
    L,
    backward_method,
    is_msbar,
):
    """
    Integration routine per operator

    Parameters
    ----------
        log_grid : tuple(k, logx)
            log grid point with relative indices
        int_disp : eko.interpolation.interpolation_dispatcher
            instance of the interpolation dispatcher
        grid_size : int
            length of the grid
        labels : numpy.ndarray
            list of ome labels
        order : int
            perturbation order
        is_log : boolean
            logarithmic interpolation
        a_s : float
            strong coupling, needed only for the exact inverse
        nf: int
            number of active flavor below threshold
        L : float
            :math:`log(q^2/m_h^2)`
        backward_method : ["exact", "expanded" or ""]
            empty or method for inverting the matching condition (exact or expanded)
        is_msbar: bool
            add the |MSbar| contribution

    Returns
    -------
        ker : float
            evaluated integration kernel
    """
    column = []
    k, logx = log_grid
    start_time = time.perf_counter()
    # iterate basis functions
    for l, bf in enumerate(int_disp):
        if k == l and l == grid_size - 1:
            continue
        temp_dict = {}
        # iterate sectors
        for label in labels:
            # compute and set
            res = integrate.quad(
                quad_ker,
                0.5,
                1.0 - 1e-02,
                args=(
                    order,
                    label[0],
                    label[1],
                    is_log,
                    logx,
                    bf.areas_representation,
                    a_s,
                    nf,
                    L,
                    backward_method,
                    is_msbar,
                ),
                epsabs=1e-12,
                epsrel=1e-5,
                limit=100,
                full_output=1,
            )
            temp_dict[label] = res[:2]
        column.append(temp_dict)
    print(
        f"Matching: computing operators - {k + 1}/{grid_size} took: {(time.perf_counter() - start_time)} s",  # pylint: disable=line-too-long
    )
    return column


class OperatorMatrixElement:
    """
    Internal representation of a single |OME|.

    The actual matrices are computed upon calling :meth:`compute`.

    Parameters
    ----------
        config : dict
            configuration
        managers : dict
            managers
        is_backward: bool
            True for backward evolution
        mellin_cut : float
            cut to the upper limit in the mellin inversion
    """

    def __init__(self, config, managers, is_backward, mellin_cut=1e-2):

        self.backward_method = config["backward_inversion"] if is_backward else ""
        if is_backward:
            self.is_intrinsic = True
        else:
            self.is_intrinsic = bool(len(config["intrinsic_range"]) != 0)
        self.config = config
        self.sc = managers["strong_coupling"]
        self.int_disp = managers["interpol_dispatcher"]
        self._mellin_cut = mellin_cut
        self.ome_members = {}

    def labels(self):
        """
        Compute necessary sector labels to compute.

        Returns
        -------
            labels : list(str)
                sector labels
        """

        labels = []
        # non singlet labels
        if self.config["debug_skip_non_singlet"]:
            logger.warning("Matching: skipping non-singlet sector")
        else:
            labels.extend([(200, 200), (br.matching_hminus_pid, 200)])
            if self.is_intrinsic or self.backward_method != "":
                # intrinsic labels, which are not zero at NLO
                labels.append((br.matching_hminus_pid, br.matching_hminus_pid))
                # These contributions are always 0 for the moment
                # labels.extend(["NS_qH", "NS_Hq"])
        # same for singlet
        if self.config["debug_skip_singlet"]:
            logger.warning("Matching: skipping singlet sector")
        else:
            labels.extend(
                [
                    *br.singlet_labels,
                    (br.matching_hplus_pid, 21),
                    (br.matching_hplus_pid, 100),
                ]
            )
            if self.is_intrinsic or self.backward_method != "":
                labels.extend(
                    [
                        (21, br.matching_hplus_pid),
                        (100, br.matching_hplus_pid),
                        (br.matching_hplus_pid, br.matching_hplus_pid),
                    ]
                )
        return labels

    def compute(self, q2, nf, L, is_msbar):
        """
        compute the actual operators (i.e. run the integrations)

        Parameters
        ----------
            q2: float
                matching scale
            nf: int
                number of active flavor below threshold
            L: float
                log of K threshold squared
            is_msbar: bool
                add the |MSbar| contribution
        """

        # init all ops with zeros
        grid_size = len(self.int_disp.xgrid)
        labels = self.labels()
        for n in labels:
            if n[0] == n[1]:
                self.ome_members[n] = OpMember(
                    np.eye(grid_size), np.zeros((grid_size, grid_size))
                )
            else:
                self.ome_members[n] = OpMember(
                    np.zeros((grid_size, grid_size)), np.zeros((grid_size, grid_size))
                )

        # At LO you don't need anything else
        if self.config["order"] == 0:
            logger.info("Matching: no need to compute matching at LO")
            self.copy_ome()
            return

        # Note that here you need to use a_s^{nf+1}(q2)
        a_s = self.sc.a_s(q2 / self.config["fact_to_ren"], q2, nf_to=nf + 1)

        tot_start_time = time.perf_counter()

        # run integration in parallel for each grid point
        with multiprocessing.Pool(int(os.cpu_count() / 2)) as pool:
            res = pool.map(
                functools.partial(
                    run_op_integration,
                    int_disp=self.int_disp,
                    grid_size=grid_size,
                    labels=labels,
                    order=self.config["order"],
                    is_log=self.int_disp.log,
                    a_s=a_s,
                    nf=nf,
                    L=L,
                    backward_method=self.backward_method,
                    is_msbar=is_msbar,
                ),
                enumerate(np.log(self.int_disp.xgrid_raw)),
            )

        # collect results
        for k, row in enumerate(res):
            for l, entry in enumerate(row):
                for label, (val, err) in entry.items():
                    self.ome_members[label].value[k][l] = val
                    self.ome_members[label].error[k][l] = err

        # closing comment
        logger.info("Matching: Total time %f s", time.perf_counter() - tot_start_time)
        self.copy_ome()

    def copy_ome(self):
        """Add the missing |OME|, if necessary"""
        grid_size = len(self.int_disp.xgrid)
        # basic labels skipped with skip debug
        for label in [
            (200, 200),
            (br.matching_hplus_pid, 21),
            (br.matching_hplus_pid, 100),
            (br.matching_hminus_pid, 200),
            *br.singlet_labels,
        ]:
            if label not in self.ome_members:
                self.ome_members[label] = OpMember(
                    np.zeros((grid_size, grid_size)), np.zeros((grid_size, grid_size))
                )

        # intrinsic labels not computed yet
        if self.is_intrinsic:
            for label in [
                (100, br.matching_hplus_pid),
                (200, br.matching_hminus_pid),
                (br.matching_hminus_pid, br.matching_hminus_pid),
                (br.matching_hplus_pid, br.matching_hplus_pid),
                (21, br.matching_hplus_pid),
            ]:
                if label not in self.ome_members:
                    self.ome_members[label] = OpMember(
                        np.zeros((grid_size, grid_size)),
                        np.zeros((grid_size, grid_size)),
                    )
