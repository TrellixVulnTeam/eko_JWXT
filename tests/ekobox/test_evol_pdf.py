# -*- coding: utf-8 -*-

import numpy as np

import eko.output.legacy
from ekobox import evol_pdf as ev_p
from ekobox import gen_op as g_o
from ekobox import gen_theory as g_t


def test_gen_and_dump_out(tmp_path):
    op = g_o.gen_op_card(
        [100.0],
        update={
            "xgrid": [0.1, 0.5, 1.0],
            "configs": {"interpolation_polynomial_degree": 1},
        },
    )
    theory = g_t.gen_theory_card(0, 1.0)

    out = ev_p.gen_out(theory, op, path=tmp_path)

    ops_id = f"o{op['hash'][:6]}_t{theory['hash'][:6]}"
    outpath = f"{tmp_path}/{ops_id}.tar"
    loaded_out = eko.output.legacy.load_tar(outpath)
    assert out.xgrid.tolist() == loaded_out.xgrid.tolist()
    for el, loaded_el in zip(out[100.0].operator, loaded_out[100.0].operator):
        np.testing.assert_allclose(
            el,
            loaded_el,
        )
