# -*- coding: utf-8 -*-
import numpy as np

from ekobox import genpdf


def test_load_info():
    info = genpdf.load.load_info_from_file("myCT14llo_NF3")
    assert "SetDesc" in info
    assert "fake" in info["SetDesc"]
    assert sorted(info["Flavors"]) == sorted([-3, -2, -1, 21, 1, 2, 3])


def test_load_data_ct14():
    blocks = genpdf.load.load_blocks_from_file("myCT14llo_NF3", 0)[1]
    assert len(blocks) == 1
    b0 = blocks[0]
    assert isinstance(b0, dict)
    assert sorted(b0.keys()) == sorted(["pids", "xgrid", "Q2grid", "data"])
    assert sorted(b0["pids"]) == sorted([-3, -2, -1, 21, 1, 2, 3])
    assert len(b0["data"].T) == 7
    np.testing.assert_allclose(b0["xgrid"][0], 1e-9)
