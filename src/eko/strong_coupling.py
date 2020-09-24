# -*- coding: utf-8 -*-
r"""
This file contains the QCD beta function coefficients and the handling of the running
coupling :math:`\alpha_s`.

See :doc:`pQCD ingredients </Theory/pQCD>`.
"""

import logging

import numpy as np
import scipy
import numba as nb

from eko import constants
from eko import thresholds

logger = logging.getLogger(__name__)


@nb.njit
def beta_0(nf: int):
    """
    Computes the first coefficient of the QCD beta function.

    Implements Eq. (3.1) of :cite:`Herzog:2017ohr`.

    Parameters
    ----------
        nf : int
            number of active flavours

    Returns
    -------
        beta_0 : float
            first coefficient of the QCD beta function :math:`\\beta_0^{n_f}`
    """
    beta_0 = 11.0 / 3.0 * constants.CA - 4.0 / 3.0 * constants.TR * nf
    return beta_0


@nb.njit
def beta_1(nf: int):
    """
    Computes the second coefficient of the QCD beta function.

    Implements Eq. (3.2) of :cite:`Herzog:2017ohr`.

    Parameters
    ----------
        nf : int
            number of active flavours

    Returns
    -------
        beta_1 : float
            second coefficient of the QCD beta function :math:`\\beta_1^{n_f}`
    """
    TF = constants.TR * nf
    b_ca2 = 34.0 / 3.0 * constants.CA * constants.CA
    b_ca = -20.0 / 3.0 * constants.CA * TF
    b_cf = -4.0 * constants.CF * TF
    beta_1 = b_ca2 + b_ca + b_cf
    return beta_1


@nb.njit
def beta_2(nf: int):
    """
    Computes the third coefficient of the QCD beta function

    Implements Eq. (3.3) of :cite:`Herzog:2017ohr`.

    Parameters
    ----------
        nf : int
            number of active flavours

    Returns
    -------
        beta_2 : float
            third coefficient of the QCD beta function :math:`\\beta_2^{n_f}`
    """
    TF = constants.TR * nf
    beta_2 = (
        2857.0 / 54.0 * constants.CA * constants.CA * constants.CA
        - 1415.0 / 27.0 * constants.CA * constants.CA * TF
        - 205.0 / 9.0 * constants.CF * constants.CA * TF
        + 2.0 * constants.CF * constants.CF * TF
        + 44.0 / 9.0 * constants.CF * TF * TF
        + 158.0 / 27.0 * constants.CA * TF * TF
    )
    return beta_2


@nb.njit
def beta(k, nf):
    """
    Compute value of a beta coefficients

    Parameters
    ----------
        k : int
            perturbative orde
        nf : int
            number of active flavours

    Returns
    -------
        beta : float
            beta_k(nf)
    """
    beta_ = 0
    if k == 0:
        beta_ = beta_0(nf)
    elif k == 1:
        beta_ = beta_1(nf)
    elif k == 2:
        beta_ = beta_2(nf)
    else:
        raise ValueError("Beta coefficients beyond NNLO are not implemented!")
    return beta_


@nb.njit
def b(k, nf):
    """
    Compute b coefficient.

    Parameters
    ----------
        k : int
            perturbative orde
        nf : int
            number of active flavours

    Returns
    -------
        b : float
            b_k(nf)
    """
    return beta(k, nf) / beta(0, nf)


class StrongCoupling:
    r"""
        Computes the strong coupling constant :math:`a_s`.

        Note that

        - all scale parameters (``scale_ref`` and ``scale_to``),
          have to be given as squared values, i.e. in units of :math:`\text{GeV}^2`
        - although, we only provide methods for
          :math:`a_s = \frac{\alpha_s(\mu^2)}{4\pi}` the reference value has to be
          given in terms of :math:`\alpha_s(\mu_0^2)` due to legacy reasons
        - the ``order`` refers to the perturbative order of the beta function, thus
          ``order=0`` means leading order beta function, means evolution with :math:`\beta_0`,
          means running at 1-loop - so there is a natural mismatch between ``order`` and the
          number of loops by one unit

        Normalization is given by :cite:`Herzog:2017ohr`:

        .. math::
            \frac{da_s(\mu^2)}{d\ln\mu^2} = \beta(a_s) \
            = - \sum\limits_{n=0} \beta_n a_s^{n+2}(\mu^2) \quad
            \text{with}~ a_s = \frac{\alpha_s(\mu^2)}{4\pi}

        See :doc:`pQCD ingredients </Theory/pQCD>`.

        Parameters
        ----------
            alpha_s_ref : float
                alpha_s(!) at the reference scale :math:`\alpha_s(\mu_0^2)`
            scale_ref : float
                reference scale :math:`\mu_0^2`
            threshold_holder : eko.thresholds.ThresholdsConfig
                An instance of :class:`~eko.thresholds.ThresholdsConfig`
            order: int
                Evaluated order of the beta function: ``0`` = LO, ...
            method : ["expanded", "exact"]
                Applied method to solve the beta function

        Examples
        --------
            >>> alpha_ref = 0.35
            >>> scale_ref = 2
            >>> threshold_holder = ThresholdsConfig( ... )
            >>> sc = StrongCoupling(alpha_ref, scale_ref, threshold_holder)
            >>> q2 = 91.1**2
            >>> sc.a_s(q2)
            0.118
    """

    def __init__(
        self,
        alpha_s_ref,
        scale_ref,
        thresh,
        order=0,
        method="exact",
    ):
        # Sanity checks
        if alpha_s_ref <= 0:
            raise ValueError(f"alpha_s_ref has to be positive - got {alpha_s_ref}")
        if scale_ref <= 0:
            raise ValueError(f"scale_ref has to be positive - got {scale_ref}")
        if not isinstance(thresh, thresholds.ThresholdsConfig):
            raise ValueError("Needs a Threshold instance")
        if order not in [0, 1, 2]:
            raise NotImplementedError("a_s beyond NNLO is not implemented")
        self._order = order
        if method not in ["expanded", "exact"]:
            raise ValueError(f"Unknown method {method}")
        self._method = method

        # create new threshold object
        self.as_ref = alpha_s_ref / 4.0 / np.pi  # convert to a_s
        if thresh.scheme == "FFNS":
            self._threshold_holder = thresholds.ThresholdsConfig(
                scale_ref, thresh.scheme, nf=thresh.nf_ref
            )
        else:
            self._threshold_holder = thresholds.ThresholdsConfig(
                scale_ref, thresh.scheme, threshold_list=thresh._area_walls
            )
        logger.info(
            "Strong Coupling: Reference a_s(Q^2=%f)=%f", self.q2_ref, self.as_ref
        )

    @property
    def q2_ref(self):
        """ reference scale """
        return self._threshold_holder.q2_ref

    @classmethod
    def from_dict(cls, setup, thresholds_config=None):
        """
        Create object from theory dictionary.

        Read keys:

            - alphas : required, reference value for  alpha_s (!)
            - Qref : required, reference value in GeV (!)
            - PTO : required, perturbative order
            - ModEv : optional, method to solve RGE, default=EXA

        Parameters
        ----------
            setup : dict
                theory dictionary
            thresholds_config : eko.thresholds.ThresholdsConfig
                threshold configuration

        Returns
        -------
            cls : StrongCoupling
                created object
        """
        # read my values
        # TODO cast to a_s here
        alpha_ref = setup["alphas"]
        q2_alpha = pow(setup["Qref"], 2)
        order = setup["PTO"]
        mod_ev = setup.get("ModEv", "EXA")
        if mod_ev == "EXA":
            method = "exact"
        elif mod_ev in ["TRN", "EXP", "perturbative-expanded"]:
            method = "expanded"
        else:
            raise ValueError(f"Unknown evolution mode {mod_ev}")
        # eventually read my dependents
        if thresholds_config is None:
            thresholds_config = thresholds.ThresholdsConfig.from_dict(setup)
        return cls(alpha_ref, q2_alpha, thresholds_config, order, method)

    # Hidden computation functions
    def _compute_expanded(self, as_ref, nf, scale_from, scale_to):
        """
        Compute via expanded expression.

        Parameters
        ----------
            as_ref: float
                reference alpha_s
            nf: int
                value of nf for computing alpha_s
            scale_from: float
                reference scale
            scale_to : float
                target scale

        Returns
        -------
            a_s : float
                coupling at target scale :math:`a_s(Q^2)`
        """
        # common vars
        beta0 = beta(0, nf)
        lmu = np.log(scale_to / scale_from)
        den = 1.0 + beta0 * as_ref * lmu
        # LO
        as_LO = as_ref / den
        res = as_LO
        # NLO
        if self._order >= 1:
            beta1 = beta(1, nf)
            b1 = beta1 / beta0
            as_NLO = as_LO * (1 - b1 * as_LO * np.log(den))
            res = as_NLO
            # NNLO
            if self._order == 2:
                beta2 = beta(2, nf)
                b2 = beta2 / beta0
                res = as_LO * (
                    1.0
                    + as_LO * (as_LO - as_ref) * (b2 - b1 ** 2)
                    + as_NLO * b1 * np.log(as_NLO / as_ref)
                )

        return res

    def _compute_exact(self, as_ref, nf, scale_from, scale_to):
        """
        Compute via RGE.

        Parameters
        ----------
            as_ref: float
                reference alpha_s
            nf: int
                value of nf for computing alpha_s
            scale_from: float
                reference scale
            scale_to : float
                target scale

        Returns
        -------
            a_s : float
                strong coupling at target scale :math:`a_s(Q^2)`
        """
        # in LO fallback to expanded, as this is the full solution
        if self._order == 0:
            return self._compute_expanded(as_ref, nf, scale_from, scale_to)
        # otherwise rescale the RGE to run in terms of
        # u = beta0 * ln(scale_to/scale_from)
        beta0 = beta(0, nf)
        u = beta0 * np.log(scale_to / scale_from)
        b_vec = [1]
        # NLO
        if self._order >= 1:
            beta1 = beta(1, nf)
            b1 = beta1 / beta0
            b_vec.append(b1)
            # NNLO
            if self._order >= 2:
                beta2 = beta(2, nf)
                b2 = beta2 / beta0
                b_vec.append(b2)
        # integration kernel
        def rge(_t, a, b_vec):
            return -(a ** 2) * np.sum([a ** k * b for k, b in enumerate(b_vec)])

        # let scipy solve
        res = scipy.integrate.solve_ivp(rge, (0, u), (as_ref,), args=[b_vec])
        return res.y[0][-1]

    def _compute(self, as_ref, nf, scale_from, scale_to):
        """
        Wrapper in order to pass the computation to the corresponding
        method (depending on the calculation method).

        Parameters
        ----------
            as_ref: float
                reference alpha_s
            nf: int
                value of nf for computing alpha_s
            scale_from: float
                reference scale
            scale_to : float
                target scale

        Returns
        -------
            a_s : float
                strong coupling at target scale :math:`a_s(Q^2)`
        """
        # TODO set up a cache system here
        # at the moment everything is expanded - and type has been checked in the constructor
        if self._method == "exact":
            as_new = self._compute_exact(as_ref, nf, scale_from, scale_to)
        else:
            as_new = self._compute_expanded(as_ref, nf, scale_from, scale_to)
        return as_new

    def a_s(self, scale_to, fact_scale=None):
        """
        Computes strong coupling :math:`a_s(Q^2) = \\frac{\\alpha_s(Q^2)}{4\\pi}`.

        Parameters
        ----------
            scale_to : float
                final scale to evolve to :math:`Q^2`

        Returns
        -------
            a_s : float
                strong coupling :math:`a_s(Q^2) = \\frac{\\alpha_s(Q^2)}{4\\pi}`
        """
        # Set up the path to follow in order to go from q2_0 to q2_ref
        final_as = self.as_ref
        area_path = self._threshold_holder.get_path_from_q2_ref(scale_to)
        # as a default assume mu_F^2 = mu_R^2
        if fact_scale is None:
            fact_scale = scale_to
        for k, area in enumerate(area_path):
            q2_from = area.q2_ref
            q2_to = area.q2_towards(scale_to)
            if np.isclose(q2_from, q2_to):
                continue
            new_as = self._compute(final_as, area.nf, q2_from, q2_to)
            # apply matching conditions: see hep-ph/9706430
            # - if there is yet a step to go
            if k < len(area_path) - 1:
                next_nf_is_down = area_path[k + 1].nf < area.nf
                # q2_to is the threshold value
                L = np.log(scale_to / fact_scale)
                if next_nf_is_down:
                    c1 = -4.0 / 3.0 * constants.TR * L
                    # TODO recover color constants
                    c2 = 4.0 / 9.0 * L ** 2 - 38.0 / 3.0 * L - 14.0 / 3.0
                else:
                    c1 = 4.0 / 3.0 * constants.TR * L
                    c2 = 4.0 / 9.0 * L ** 2 + 38.0 / 3.0 * L + 14.0 / 3.0
                # shift
                if self._order == 1:
                    new_as *= 1 + c1 * new_as
                elif self._order == 2:
                    new_as *= 1 + c1 * new_as + c2 * new_as ** 2
            final_as = new_as
        return final_as
