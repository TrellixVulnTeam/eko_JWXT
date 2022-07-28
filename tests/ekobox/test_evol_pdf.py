# -*- coding: utf-8 -*-

from banana import toy

import eko
import eko.output.legacy as out
from ekobox import evol_pdf as ev_p
from ekobox import operators_card as oc
from ekobox import theory_card as tc

op = oc.generate(
    [100.0],
    update={
        "interpolation_xgrid": [0.1, 0.5, 1.0],
        "interpolation_polynomial_degree": 1,
    },
)
theory = tc.generate(0, 1.65)


def test_evolve_pdfs_run(fake_lhapdf, cd):
    n = "test_evolve_pdfs_run"
    mytmp = fake_lhapdf / "install"
    mytmp.mkdir()
    store_path = mytmp / "test.tar"
    with cd(mytmp):
        ev_p.evolve_pdfs(
            [toy.mkPDF("", 0)], theory, op, install=True, name=n, store_path=store_path
        )
    p = fake_lhapdf / n
    assert p.exists()
    # check dumped eko
    assert store_path.exists()
    assert store_path.is_file()
    out.load_tar(store_path)


def test_evolve_pdfs_dump_path(fake_lhapdf, cd):
    n = "test_evolve_pdfs_dump_path"
    peko = fake_lhapdf / ev_p.ekofileid(theory, op)
    out.dump_tar(eko.run_dglap(theory, op), peko)
    assert peko.exists()
    with cd(fake_lhapdf):
        ev_p.evolve_pdfs([toy.mkPDF("", 0)], theory, op, name=n, path=fake_lhapdf)
    p = fake_lhapdf / n
    assert p.exists()


def test_evolve_pdfs_dump_file(fake_lhapdf, cd):
    n = "test_evolve_pdfs_dump_file"
    peko = fake_lhapdf / ev_p.ekofileid(theory, op)
    out.dump_tar(eko.run_dglap(theory, op), peko)
    assert peko.exists()
    with cd(fake_lhapdf):
        ev_p.evolve_pdfs([toy.mkPDF("", 0)], theory, op, name=n, path=peko)
    p = fake_lhapdf / n
    assert p.exists()
