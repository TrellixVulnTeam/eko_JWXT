# -*- coding: utf-8 -*-
"""
This module defines the operator matrix elements for the non-trivial matching conditions in the |VFNS| evolution.
"""
import logging

import numpy as np
from scipy import integrate
import numba as nb

from .. import mellin
from .. import interpolation
from ..member import OpMember

from .nnlo import A_singlet_2, A_ns_2
from ..anomalous_dimensions import harmonics
from ..member import singlet_labels

# TODO: order might be removed if N3LO matching conditions will not be implemented

logger = logging.getLogger(__name__)


@nb.njit("f8(f8,string,b1,f8,f8[:,:])", cache=True)
def quad_ker(
    u,
    mode,
    is_log,
    logx,
    areas,
):
    """
    Raw kernel inside quad

    Parameters
    ----------
        u : float
            quad argument
        order : int
            perturbation order
        mode : str
            element in the singlet sector
        is_log : boolean
            logarithmic interpolation
        logx : float
            Mellin inversion point
        areas : tuple
            basis function configuration

    Returns
    -------
        ker : float
            evaluated integration kernel
    """
    is_singlet = mode[0] == "S"
    # get transformation to N integral
    if is_singlet:
        r, o = 0.4 * 16.0 / (1.0 - logx), 1.0
    else:
        r, o = 0.5, 0.0

    n = mellin.Talbot_path(u, r, o)
    jac = mellin.Talbot_jac(u, r, o)
    # check PDF is active
    if is_log:
        pj = interpolation.log_evaluate_Nx(n, logx, areas)
    else:
        pj = interpolation.evaluate_Nx(n, logx, areas)

    if pj == 0.0:
        return 0.0

    # compute the harmonics
    sx = np.array(
        [harmonics.harmonic_S1(n), harmonics.harmonic_S2(n), harmonics.harmonic_S3(n)]
    )

    # compute the actual evolution kernel
    if is_singlet:
        ker = A_singlet_2(n, sx)
        # select element of matrix
        k = 0 if mode[2] == "q" else 1
        l = 0 if mode[3] == "q" else 1
        ker = ker[k, l]
    else:
        ker = A_ns_2(n, sx)

    # recombine everthing
    mellin_prefactor = complex(0.0, -1.0 / np.pi)
    return np.real(mellin_prefactor * ker * pj * jac)


class OperatorMatrixElement:
    """
    Internal representation of a single Operator Matrix Element.

    The actual matrices are computed upon calling :meth:`compute`.

    Parameters
    ----------
        config : dict
            configuration
        managers : dict
            managers
        mellin_cut : float
            cut to the upper limit in the mellin inversion
    """

    def __init__(self, config, managers, mellin_cut=1e-2):
        self.order = config["order"]
        self.int_disp = managers["interpol_dispatcher"]
        self._mellin_cut = mellin_cut
        self.ome_members = {}

    def compute(self):
        """ compute the actual operators (i.e. run the integrations) """

        # init all ops with zeros
        grid_size = len(self.int_disp.xgrid)
        labels = ["NS", *singlet_labels]
        for n in labels:
            self.ome_members[n] = OpMember(
                np.zeros((grid_size, grid_size)), np.zeros((grid_size, grid_size))
            )

        logger.info("Matching: computing operators - 0/%d", grid_size)
        # iterate output grid
        for k, logx in enumerate(np.log(self.int_disp.xgrid_raw)):
            # iterate basis functions
            for l, bf in enumerate(self.int_disp):
                # iterate sectors
                for label in labels:
                    # compute and set
                    res = integrate.quad(
                        quad_ker,
                        0.5,
                        1.0 - self._mellin_cut,
                        args=(
                            # self.order,
                            label,
                            self.int_disp.log,
                            logx,
                            bf.areas_representation,
                        ),
                        epsabs=1e-12,
                        epsrel=1e-5,
                        limit=100,
                        full_output=1,
                    )
                    val, err = res[:2]
                    self.ome_members[label].value[k][l] = val
                    self.ome_members[label].error[k][l] = err
