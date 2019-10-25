# -*- coding: utf-8 -*-
# Test interpolation
from numpy.polynomial import Chebyshev
from numpy.testing import assert_allclose, assert_almost_equal
import numpy as np
import scipy.integrate as integrate


from eko import t_float, t_complex
from eko.interpolation import (
    get_xgrid_linear_at_id,
    get_xgrid_linear_at_log,
    get_xgrid_Chebyshev_at_id,
    get_xgrid_Chebyshev_at_log,
    get_Lagrange_interpolators_x,
    get_Lagrange_interpolators_N,
    get_Lagrange_interpolators_log_x,
    get_Lagrange_interpolators_log_N,
)

# for the numeric comparision to work, keep in mind that in Python3 the default precision is
# np.float64

# Checking utilities
def check_is_tfloat(function, grid_size=3, xmin=0.0, xmax=1.0):
    """ Checks all members of the return value of function are of type t_float """
    result = function(grid_size, xmin, xmax)
    for i in result:
        assert isinstance(i, t_float)
    return result


def check_xgrid(function, grid, grid_size=3, xmin=0.0, xmax=1.0):
    """ Checks the grid that function returns correspond to `grid` """
    result = function(grid_size, xmin, xmax)
    assert_allclose(result, grid)
    return result


def check_interpolator(function, points, values, xmin=0.0, j=3):
    arr = np.linspace(xmin, 1, 5)
    for x, val in zip(points, values):
        result = function(x, arr, j)
        assert_almost_equal(result, val, decimal=4)


def _Mellin_transform(f, N):  # TODO move to utilities
    """straight implementation of the Mellin transform"""

    def integrand(x):
        xton = pow(x, N - 1) * f(x)
        return xton

    r, re = integrate.quad(lambda x: np.real(integrand(x)), 0, 1)
    i, ie = integrate.quad(lambda x: np.imag(integrand(x)), 0, 1)
    result = t_complex(complex(r, i))
    error = t_complex(complex(re, ie))
    return result, error


def check_is_interpolator(inter_x, xgrid):
    """ Check whether the function `inter_x` is indeed an interpolator """
    values = [1e-4, 1e-2, 0.2, 0.4, 0.6, 0.8]
    for v in values:
        one = 0.0
        # Check it sums to one
        for j in range(len(xgrid)):
            one += inter_x(v, xgrid, j)
        assert_almost_equal(one, 1.0)

    # polynoms need to be "orthogonal" at grid points
    for j, x in enumerate(xgrid):
        one = inter_x(x, xgrid, j)
        assert_almost_equal(one, 1.0)

        for k, y in enumerate(xgrid):
            if j == k:
                continue
            zero = inter_x(y, xgrid, j)
            assert_almost_equal(zero, 0.0)


def check_correspondence_interpolators(inter_x, inter_N, xgrid):
    """ Check the correspondece between x and N space of the interpolators
    inter_x and inter_N"""
    ngrid = [complex(1.0), complex(1.0 + 1j), t_complex(0.5 - 2j)]
    for j in range(len(xgrid)):
        for N in ngrid:
            result_N = inter_N(N, xgrid, j)
            result_x = _Mellin_transform(lambda x: inter_x(x, xgrid, j), N)
            assert_almost_equal(result_x[0], result_N)


# TEST functions
def test_get_xgrid_linear_at_id():
    """test linear@id grids"""
    grid_result = np.array([0.0, 0.5, 1.0])
    check_xgrid(get_xgrid_linear_at_id, grid_result)
    check_is_tfloat(get_xgrid_linear_at_id)


def test_get_xgrid_Chebyshev_at_id():
    """test get_xgrid_Chebyshev_at_id"""
    for n in [3, 5, 7]:
        check_is_tfloat(get_xgrid_Chebyshev_at_id, grid_size=n)
        # test that grid points correspond indeed to nodes of the polynomial
        cheb_n = Chebyshev(np.append(np.zeros(n), 1), domain=[0, 1])
        check_xgrid(get_xgrid_Chebyshev_at_id, cheb_n.roots(), grid_size=n)


def test_get_xgrid_linear_at_log10():
    """test linear@log10 grids"""
    grid_result = np.array([1e-2, 1e-1, 1.0])
    check_is_tfloat(get_xgrid_linear_at_log, xmin=1e-2)
    check_xgrid(get_xgrid_linear_at_log, grid_result, xmin=1e-2)


def test_get_xgrid_Chebyshev_at_log():
    xmin = 1e-2
    for n in [3, 5, 7]:
        check_is_tfloat(get_xgrid_Chebyshev_at_log, grid_size=n, xmin=xmin)
        cheb_n = Chebyshev(np.append(np.zeros(n), 1), domain=[0, 1])
        exp_arg = np.log(xmin) - cheb_n.roots() * np.log(xmin)
        nodes = np.exp(exp_arg)
        check_xgrid(get_xgrid_Chebyshev_at_log, nodes, grid_size=n, xmin=xmin)


def test_get_Lagrange_interpolators_x():
    # TODO: this assumes implementation at f61b238602db5a43f1945fb015dbc88cdfee0dd0 is ok
    # try some external way?
    points = [0.3]
    values = [-504 / 5625]
    check_interpolator(get_Lagrange_interpolators_x, points, values)
    check_is_interpolator(get_Lagrange_interpolators_x, [0.0, 0.5, 1.0])


def test_get_Lagrange_interpolators_N():
    # TODO: this assumes implementation at f61b238602db5a43f1945fb015dbc88cdfee0dd0 is ok
    # try some external way?
    points = [complex(0.5, 0.5)]
    values = [complex(0.381839, -0.1408880)]
    check_interpolator(get_Lagrange_interpolators_N, points, values)


def test_correspondence_lagrange_xN():
    """test correspondence of interpolators in x- and N-space"""
    check_correspondence_interpolators(
        get_Lagrange_interpolators_x, get_Lagrange_interpolators_N, [0.0, 0.5, 1.0]
    )


def test_get_Lagrange_interpolators_log_x():
    # TODO: this assumes implementation at f61b238602db5a43f1945fb015dbc88cdfee0dd0 is ok
    # try some external way?
    points = [0.3]
    values = [-0.6199271485409041]
    check_interpolator(get_Lagrange_interpolators_log_x, points, values, xmin=1e-2)
    check_is_interpolator(get_Lagrange_interpolators_log_x, [1e-4, 1e-2, 1.0])


def test_get_Lagrange_interpolators_log_N():
    # TODO: this assumes implementation at f61b238602db5a43f1945fb015dbc88cdfee0dd0 is ok
    # try some external way?
    points = [complex(0.5, 0.5)]
    values = [complex(-42.24104240911104, -120.36554908750743)]
    check_interpolator(get_Lagrange_interpolators_log_N, points, values, xmin=1e-2)


def test_correspondence_lagrange_log_xN():
    check_correspondence_interpolators(
        get_Lagrange_interpolators_log_x,
        get_Lagrange_interpolators_log_N,
        [1e-4, 1e-2, 1.0],
    )


# TODO What function is this testing?
# if the answer is "_Mellin_transform" this
# means Mellin_transform is
# a function that should be in a "utilities" module instead
#
# def test__Mellin_transform():
#     """prevent circular reasoning"""
#     f = lambda x: x
#     g = lambda N: 1.0 / (N + 1.0)
#     for N in [1.0, 1.0 + 1j, 0.5 - 2j]:
#         e = g(N)
#         a = _Mellin_transform(f, N)
#         assert_almost_equal(e, a[0])
#         assert_almost_equal(0.0, a[1])
