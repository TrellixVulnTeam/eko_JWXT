# -*- coding: utf-8 -*-
"""
This module defines the |OME| for the non-trivial matching conditions in the
|VFNS| evolution.
"""

import functools
import logging

import numba as nb
import numpy as np

from .. import basis_rotation as br
from .. import harmonics
from .. import quad_ker_base as qkb
from ..evolution_operator import Operator
from . import (
    A_non_singlet_as1,
    A_non_singlet_as2,
    A_non_singlet_as3,
    A_singlet_as1,
    A_singlet_as2,
    A_singlet_as3,
)

logger = logging.getLogger(__name__)


@nb.njit(cache=True)
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


@nb.njit(cache=True)
def quad_ker_as1(
    u, order, mode0, mode1, is_log, logx, areas, a_s, nf, L, backward_method, is_msbar
):
    """Raw |NLO| kernel inside quad.

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
    nf : int
        number of active flavor below threshold
    L : float
        :math:`log(q^2/m_h^2)`
    backward_method : ["exact", "expanded" or ""]
        empty or method for inverting the matching condition (exact or expanded)
    is_msbar : bool
        add the |MSbar| contribution

    Returns
    -------
    float
        |NLO| evaluated integration kernel
    """
    ker_base = qkb.QuadKerBase(qkb.MODE_MATCHING, u, is_log, logx, areas, mode0, mode1)
    if ker_base.is_empty:
        return 0.0

    sx = harmonics.compute_harmonics_cache(ker_base.n, order, ker_base.is_singlet)
    sx_ns = None

    # compute the ome
    if ker_base.is_singlet:
        A = A_singlet_as1(ker_base.n, sx, L, is_msbar, nf, sx_ns)
    else:
        A = A_non_singlet_as1(ker_base.n, sx, L, nf)

    # build the expansion in alpha_s depending on the strategy
    ker = build_ome(A, order, a_s, backward_method)

    return ker_base.compute_matching(ker)


@nb.njit(cache=True)
def quad_ker_as2(
    u, order, mode0, mode1, is_log, logx, areas, a_s, nf, L, backward_method, is_msbar
):
    """Raw |NNLO| kernel inside quad.

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
    nf : int
        number of active flavor below threshold
    L : float
        :math:`log(q^2/m_h^2)`
    backward_method : ["exact", "expanded" or ""]
        empty or method for inverting the matching condition (exact or expanded)
    is_msbar : bool
        add the |MSbar| contribution

    Returns
    -------
    float
        |NNLO| evaluated integration kernel
    """
    ker_base = qkb.QuadKerBase(qkb.MODE_MATCHING, u, is_log, logx, areas, mode0, mode1)
    if ker_base.is_empty:
        return 0.0

    sx = harmonics.compute_harmonics_cache(ker_base.n, order, ker_base.is_singlet)
    sx_ns = None

    # compute the ome
    if ker_base.is_singlet:
        A = A_singlet_as2(ker_base.n, sx, L, is_msbar, nf, sx_ns)
    else:
        A = A_non_singlet_as2(ker_base.n, sx, L, nf)

    # build the expansion in alpha_s depending on the strategy
    ker = build_ome(A, order, a_s, backward_method)
    return ker_base.compute_matching(ker)


@nb.njit(cache=True)
def quad_ker_as3(
    u, order, mode0, mode1, is_log, logx, areas, a_s, nf, L, backward_method, is_msbar
):
    """Raw |N3LO| kernel inside quad.

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
    nf : int
        number of active flavor below threshold
    L : float
        :math:`log(q^2/m_h^2)`
    backward_method : ["exact", "expanded" or ""]
        empty or method for inverting the matching condition (exact or expanded)
    is_msbar : bool
        add the |MSbar| contribution

    Returns
    -------
    float
        |N3LO| evaluated integration kernel
    """
    ker_base = qkb.QuadKerBase(qkb.MODE_MATCHING, u, is_log, logx, areas, mode0, mode1)
    if ker_base.is_empty:
        return 0.0

    sx = harmonics.compute_harmonics_cache(ker_base.n, order, ker_base.is_singlet)
    sx_ns = None
    if (backward_method != "" and ker_base.is_singlet) or (
        mode0 == 100 and mode0 == 100
    ):
        # At N3LO for A_qq singlet or backward you need to compute
        # both the singlet and non-singlet like harmonics
        # avoiding recomputing all of them ...
        sx_ns = sx.copy()
        smx_ns = harmonics.smx(ker_base.n, np.array([s[0] for s in sx]), False)
        for w, sm in enumerate(smx_ns):
            sx_ns[w][-1] = sm
        sx_ns[2][2] = harmonics.S2m1(ker_base.n, sx[0][1], smx_ns[0], smx_ns[1], False)
        sx_ns[2][3] = harmonics.Sm21(ker_base.n, sx[0][0], smx_ns[0], False)
        sx_ns[3][5] = harmonics.Sm31(ker_base.n, sx[0][0], smx_ns[0], smx_ns[1], False)
        sx_ns[3][4] = harmonics.Sm211(ker_base.n, sx[0][0], sx[0][1], smx_ns[0], False)
        sx_ns[3][3] = harmonics.Sm22(
            ker_base.n, sx[0][0], sx[0][1], smx_ns[1], sx_ns[3][5], False
        )

    # compute the ome
    if ker_base.is_singlet:
        A = A_singlet_as3(ker_base.n, sx, L, is_msbar, nf, sx_ns)
    else:
        A = A_non_singlet_as3(ker_base.n, sx, L, nf)

    # build the expansion in alpha_s depending on the strategy
    ker = build_ome(A, order, a_s, backward_method)
    return ker_base.compute_matching(ker)


class OperatorMatrixElement(Operator):
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
        q2: float
            matching scale
        nf: int
            number of active flavor below threshold
        L: float
            log of K threshold squared
        is_msbar: bool
            add the |MSbar| contribution
    """

    log_label = "Matching"
    # complete list of possible matching operators labels
    full_labels = [
        *br.singlet_labels,
        (br.matching_hplus_pid, 21),
        (br.matching_hplus_pid, 100),
        (21, br.matching_hplus_pid),
        (100, br.matching_hplus_pid),
        (br.matching_hplus_pid, br.matching_hplus_pid),
        (200, 200),
        (200, br.matching_hminus_pid),
        (br.matching_hminus_pid, 200),
        (br.matching_hminus_pid, br.matching_hminus_pid),
    ]

    def __init__(self, config, managers, nf, q2, is_backward, L, is_msbar):
        super().__init__(config, managers, nf, q2)
        self.backward_method = config["backward_inversion"] if is_backward else ""
        if is_backward:
            self.is_intrinsic = True
        else:
            self.is_intrinsic = bool(len(config["intrinsic_range"]) != 0)
        self.L = L
        self.is_msbar = is_msbar

    @property
    def labels(self):
        """
        Compute necessary sector labels to compute.

        Returns
        -------
            labels : list(str)
                sector labels
        """

        labels = []
        # non-singlet labels
        if self.config["debug_skip_non_singlet"]:
            logger.warning("%s: skipping non-singlet sector", self.log_label)
        else:
            labels.append((200, 200))
            if self.is_intrinsic or self.backward_method != "":
                # intrinsic labels, which are not zero at NLO
                labels.append((br.matching_hminus_pid, br.matching_hminus_pid))
                # These contributions are always 0 for the moment
                # labels.extend([(200, br.matching_hminus_pid), (br.matching_hminus_pid, 200)])
        # same for singlet
        if self.config["debug_skip_singlet"]:
            logger.warning("%s: skipping singlet sector", self.log_label)
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

    def quad_ker(self, label, logx, areas):
        """
        Partially initialized integrand function

        Parameters
        ----------
            label: tuple
                operator element pids
            logx: float
                Mellin inversion point
            areas : tuple
                basis function configuration

        Returns
        -------
            quad_ker : functools.partial
                partially initialized intration kernel

        """
        qk = quad_ker_as1
        if self.config["order"] >= 2:
            qk = quad_ker_as2
        if self.config["order"] >= 3:
            qk = quad_ker_as3
        return functools.partial(
            qk,
            order=self.config["order"],
            mode0=label[0],
            mode1=label[1],
            is_log=self.int_disp.log,
            logx=logx,
            areas=areas,
            a_s=self.a_s,
            nf=self.nf,
            L=self.L,
            backward_method=self.backward_method,
            is_msbar=self.is_msbar,
        )

    @property
    def a_s(self):
        """
        Returns the computed values for :math:`a_s`.
        Note that here you need to use :math:`a_s^{n_f+1}`
        """
        sc = self.managers["strong_coupling"]
        return sc.a_s(self.q2_from / self.fact_to_ren, self.q2_from, nf_to=self.nf + 1)

    def compute(self):
        """
        compute the actual operators (i.e. run the integrations)
        """
        self.initialize_op_members()

        # At LO you don't need anything else
        if self.config["order"] == 0:
            logger.info("%s: no need to compute matching at LO", self.log_label)
            return

        self.integrate()
