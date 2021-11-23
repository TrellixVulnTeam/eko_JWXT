# -*- coding: utf-8 -*-
import pytest

from ekobox import gen_theory as g_t

from . import utils


def test_gen_theory_card():
    theory = g_t.gen_theory_card("FFNS", 0, 1.0)
    assert theory["FNS"] == "FFNS"
    assert theory["PTO"] == 0
    assert theory["Q0"] == 1.0
    assert theory["mt"] == 173.07
    up_err = {"Prova": "Prova", "FNS": "VFNS"}
    with pytest.raises(ValueError):
        theory = g_t.gen_theory_card("FFNS", 0, 1.0, update=up_err)
    up = {"mb": 132.3, "FNS": "VFNS"}
    theory = g_t.gen_theory_card("FFNS", 0, 1.0, update=up)
    assert theory["FNS"] == "VFNS"
    assert theory["mb"] == 132.3


def test_dump_load_theory_card(tmp_path):
    with utils.cd(tmp_path):
        theory = g_t.gen_theory_card("FFNS", 2, 12.3, dump=True, name="debug_theory")
        g_t.dump_theory_card("debug_theory_two", theory)
        theory_loaded = g_t.load_theory_card("debug_theory.yaml")
        theory_two_loaded = g_t.load_theory_card("debug_theory_two.yaml")
        for key in theory.keys():
            assert theory[key] == theory_loaded[key] == theory_two_loaded[key]
