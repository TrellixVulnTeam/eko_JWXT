# -*- coding: utf-8 -*-
import os
import pathlib
import shutil
import sys
from contextlib import contextmanager

import numpy as np
import pytest


@pytest.fixture
def cd():
    # thanks https://stackoverflow.com/questions/431684/how-do-i-change-the-working-directory-in-python/24176022#24176022
    @contextmanager
    def wrapped(newdir):
        prevdir = os.getcwd()
        os.chdir(os.path.expanduser(newdir))
        try:
            yield
        finally:
            os.chdir(prevdir)

    return wrapped


class FakePDF:
    def hasFlavor(self, pid):
        return pid == 1

    def xfxQ2(self, _pid, x, _q2):
        return x


@pytest.fixture
def fake_pdf():
    return FakePDF()


class FakeOutput:
    shape = (2, 2)

    def mkO(self):
        ma, mae = np.random.rand(2, *self.shape)
        return ma, mae

    def mk_g(self, q2s, lpids, lx):
        Q2grid = {}
        for q2 in q2s:
            Q2grid[q2] = {
                "operator": np.random.rand(lpids, lx, lpids, lx),
                "error": np.random.rand(lpids, lx, lpids, lx),
                "alphas": np.random.rand(),
            }
        return Q2grid

    def fake_output(self):
        # build data
        xgrid = np.array([0.5, 1.0])
        interpolation_polynomial_degree = 1
        interpolation_is_log = False
        pids = [0, 1]
        q2_ref = 1
        q2_out = 2
        Q2grid = self.mk_g([q2_out], len(pids), len(xgrid))
        d = dict(
            xgrid=xgrid,
            rotations=dict(
                targetgrid=xgrid,
                inputgrid=xgrid,
                inputpids=pids,
                targetpids=pids,
            ),
            Q0=np.sqrt(q2_ref),
            couplings=dict(),
            configs=dict(
                ev_op_max_order=1,
                ev_op_iterations=1,
                interpolation_polynomial_degree=interpolation_polynomial_degree,
                interpolation_is_log=interpolation_is_log,
                backward_inversion="exact",
            ),
            Q2grid=Q2grid,
        )
        return d


@pytest.fixture
def fake_factory():
    return FakeOutput()


@pytest.fixture
def fake_output():
    return FakeOutput().fake_output()


@pytest.fixture
def fake_lhapdf(tmp_path):
    def lhapdf_paths():
        return [tmp_path]

    # Thanks https://stackoverflow.com/questions/43162722/mocking-a-module-import-in-pytest
    module = type(sys)("lhapdf")
    module.paths = lhapdf_paths
    sys.modules["lhapdf"] = module

    yield tmp_path


fakepdf = pathlib.Path(__file__).parents[1] / "benchmarks" / "ekobox" / "fakepdf"


def copy_lhapdf(fake_lhapdf, n):
    src = fakepdf / n
    dst = fake_lhapdf / n
    shutil.copytree(src, dst)
    yield n
    shutil.rmtree(dst)


@pytest.fixture
def fake_ct14(fake_lhapdf):
    yield from copy_lhapdf(fake_lhapdf, "myCT14llo_NF3")


@pytest.fixture
def fake_nn31(fake_lhapdf):
    yield from copy_lhapdf(fake_lhapdf, "myNNPDF31_nlo_as_0118")


@pytest.fixture
def fake_mstw(fake_lhapdf):
    yield from copy_lhapdf(fake_lhapdf, "myMSTW2008nlo90cl")
