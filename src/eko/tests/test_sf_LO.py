# -*- coding: utf-8 -*-
# Test splitting functions
import numpy as np
from numpy.testing import assert_almost_equal

from eko.constants import Constants

import eko.splitting_functions_LO as spf_LO
from eko import t_complex

constants = Constants()
CA = constants.CA
CF = constants.CF
NF = 5


def check_values(function, inputs, known_values):
    """ Takes advantages of the unified signature for all coefficients
    to check the value for N == `N1` """
    for N, val in zip(inputs, known_values):
        result = function(N, NF, CA, CF)
        assert_almost_equal(result, val)


def test_gsl_digamma():
    """ test the cffi implementation of digamma """
    from scipy.special import digamma as scipy_digamma

    for r, i in np.random.rand(4, 2):
        test_val = np.complex(r, i)
        scipy_result = scipy_digamma(test_val)
        gsl_result = spf_LO.gsl_digamma(test_val)
        assert_almost_equal(scipy_result, gsl_result)


def test__S1():
    """test harmonic sum _S1"""
    # test on real axis
    known_vals = [1.0, 1.0 + 1.0 / 2.0, 1.0 + 1.0 / 2.0 + 1.0 / 3.0]
    for i, val in enumerate(known_vals):
        cval = t_complex(val)
        result = spf_LO._S1(1 + i)  # pylint: disable=protected-access
        assert_almost_equal(result, cval)


def test_number_momentum_conservation():
    """test number/momentum conservation"""
    # number
    input_N = [complex(1.0, 0.0)]
    known_vals = [complex(0.0, 0.0)]
    check_values(spf_LO.gamma_ns_0, input_N, known_vals)

    # quark momentum
    input_N = [complex(2.0, 0.0)]
    known_vals = [complex(0.0, 0.0)]

    def _sum(*args):
        return spf_LO.gamma_ns_0(*args) + spf_LO.gamma_gq_0(
            *args
        )  # pylint: disable=no-value-for-parameter

    check_values(_sum, input_N, known_vals)

    # gluon momentum
    def _sum(*args):
        return spf_LO.gamma_qg_0(*args) + spf_LO.gamma_gg_0(
            *args
        )  # pylint: disable=no-value-for-parameter

    check_values(_sum, input_N, known_vals)


def test_gamma_ps_0():
    input_N = [complex(1.0, 0.0)]
    known_vals = [complex(0.0, 0.0)]
    check_values(spf_LO.gamma_ps_0, input_N, known_vals)


def test_gamma_qg_0():
    input_N = [complex(1.0, 0.0)]
    known_vals = [complex(-20.0 / 3.0, 0.0)]
    check_values(spf_LO.gamma_qg_0, input_N, known_vals)


def test_gamma_gq_0():
    input_N = [complex(0.0, 1.0)]
    known_vals = [complex(4.0, -4.0) / 3.0]
    check_values(spf_LO.gamma_gq_0, input_N, known_vals)


def test_gamma_gg_0():
    input_N = [complex(0.0, 1.0)]
    known_vals = [complex(5.195725159621, 10.52008856962)]
    check_values(spf_LO.gamma_gg_0, input_N, known_vals)
