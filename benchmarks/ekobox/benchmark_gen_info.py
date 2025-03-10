# -*- coding: utf-8 -*-
import math

import numpy as np
import pytest

from ekobox import gen_info as g_i
from ekobox import gen_op as g_o
from ekobox import gen_theory as g_t


@pytest.mark.isolated
def benchmark_create_info_file():
    op = g_o.gen_op_card([10, 100])
    theory = g_t.gen_theory_card(1, 10.0, update={"alphas": 0.2})
    info = g_i.create_info_file(
        theory, op, 4, info_update={"SetDesc": "Prova", "NewArg": 15.3, "MTop": 1.0}
    )
    assert info["AlphaS_MZ"] == 0.2
    assert info["SetDesc"] == "Prova"
    assert info["NewArg"] == 15.3
    assert info["NumMembers"] == 4
    assert info["MTop"] == theory["mt"]
    np.testing.assert_allclose(info["QMin"], math.sqrt(op["Q2grid"][0]), rtol=1e-5)
    assert info["XMin"] == op["interpolation_xgrid"][0]
    assert info["XMax"] == op["interpolation_xgrid"][-1] == 1.0
