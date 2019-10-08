# -*- coding: utf-8 -*-
r"""
This file contains the Altarelli-Parisi splitting kernels.

Normalization is given by

.. math::
      \frac{dq_{ns}^i}{d\ln\mu^2}
      = - \sum\limits_{n=0} a^{n+1} P_{ns}^{(n),i} q_{ns}^i \
          \quad \text{with}~ a = \frac{\alpha_S1(\mu^2)}{4\pi}


References
----------
  The 3-loop references are for the non-singlet [4]_ and singlet [5]_ case given below.
  They also contain the lower order results

  .. [4] S. Moch et al. "The Three loop splitting functions in QCD: The Nonsinglet case"
     in Nucl.Phys. B688 (2004), p. 101. doi: 10.1016/j.nuclphysb.2004.03.030. arxiv: hep-ph/0403192
  .. [5] A. Vogt et al. "The Three-loop splitting functions in QCD: The Singlet case"
     in Nucl.Phys. B691 (2004), p. 129. doi: 10.1016/j.nuclphysb.2004.04.024. arxiv: hep-ph/0404111
"""
from numpy import euler_gamma
from scipy.special import digamma
from eko import t_float, t_complex

def _S1(N : t_complex):
    """Computes the simple harmonic sum

    Parameters
    ----------
      N : t_complex
        Mellin moment

    Returns
    -------
      S : t_complex
        Harmonic sum up to N :math:`S_1(N)`
    """
    return digamma(N + 1) + euler_gamma

def gamma_ns_0(N : t_complex, nf : int, CA : t_float, CF : t_float): # pylint: disable=unused-argument
    """Computes the leading-order non-singlet anomalous dimension.

    Implements Eq. (3.4) of [4]_.
    For the sake of unification we keep a unique function signature for *all* coefficients.

    Parameters
    ----------
      N : t_complex
        Mellin moment
      nf : int
        Number of active flavours (which is actually not used here)
      CA : t_float
       Casimir constant of adjoint representation (which is actually not used here)
      CF : t_float
       Casimir constant of fundamental representation

    Returns
    -------
      gamma_ns_0 : t_complex
        Leading-order non-singlet anomalous dimension :math:`\\gamma_{ns}^{(0)}(N)`
    """
    f = 2*(_S1(N-1) + _S1(N+1)) - 3
    return CF * f

def gamma_ps_0(N : t_complex, nf : int, CA : t_float, CF : t_float): # pylint: disable=unused-argument
    """Computes the leading-order pure-singlet anomalous dimension

    Implements Eq. (3.5) of [5]_.
    For the sake of unification we keep a unique function signature for *all* coefficients.

    Parameters
    ----------
      N : t_complex
        Mellin moment
      nf : int
        Number of active flavours (which is actually not used here)
      CA : t_float
       Casimir constant of adjoint representation (which is actually not used here)
      CF : t_float
       Casimir constant of fundamental representation (which is actually not used here)

    Returns
    -------
      gamma_ps_0 : t_complex
        Leading-order pure-singlet anomalous dimension :math:`\\gamma_{ps}^{(0)}(N)`
    """
    return 0.

def gamma_qg_0(N : t_complex, nf : int, CA : t_float, CF : t_float): # pylint: disable=unused-argument
    """Computes the leading-order quark-gluon anomalous dimension

    Implements Eq. (3.5) of [5]_.
    For the sake of unification we keep a unique function signature for *all* coefficients.

    Parameters
    ----------
      N : t_complex
        Mellin moment
      nf : int
        Number of active flavours
      CA : t_float
       Casimir constant of adjoint representation (which is actually not used here)
      CF : t_float
       Casimir constant of fundamental representation (which is actually not used here)

    Returns
    -------
      gamma_qg_0 : t_complex
        Leading-order quark-gluon anomalous dimension :math:`\\gamma_{qg}^{(0)}(N)`
    """
    f = _S1(N-1)+ 4.*_S1(N+1) - 2.*_S1(N+2) - 3.*_S1(N)
    return 2.*nf*f

def gamma_gq_0(N : t_complex, nf : int, CA : t_float, CF : t_float): # pylint: disable=unused-argument
    """Computes the leading-order gluon-quark anomalous dimension

    Implements Eq. (3.5) of [5]_.
    For the sake of unification we keep a unique function signature for *all* coefficients.

    Parameters
    ----------
      N : t_complex
        Mellin moment
      nf : int
        Number of active flavours (which is actually not used here)
      CA : t_float
       Casimir constant of adjoint representation (which is actually not used here)
      CF : t_float
       Casimir constant of fundamental representation

    Returns
    -------
      gamma_qg_0 : t_complex
        Leading-order gluon-quark anomalous dimension :math:`\\gamma_{gq}^{(0)}(N)`
    """
    f = 2.*_S1(N-2) - 4.*_S1(N-1) - _S1(N+1) + 3.*_S1(N)
    return 2.*CF*f

def gamma_gg_0(N : t_complex, nf : int, CA : t_float, CF : t_float): # pylint: disable=unused-argument
    """Computes the leading-order gluon-gluon anomalous dimension

    Implements Eq. (3.5) of [5]_.
    For the sake of unification we keep a unique function signature for *all* coefficients.

    Parameters
    ----------
      N : t_complex
        Mellin moment
      nf : int
        Number of active flavours
      CA : t_float
       Casimir constant of adjoint representation
      CF : t_float
       Casimir constant of fundamental representation (which is actually not used here)

    Returns
    -------
      gamma_qg_0 : t_complex
        Leading-order gluon-gluon anomalous dimension :math:`\\gamma_{gg}^{(0)}(N)`
    """
    f = _S1(N-2) - 2.*_S1(N-1) - 2.*_S1(N+1) + _S1(N+2) + 3.*_S1(N)
    return CA * (4. * f - 11./3.) + 2./3. * nf
