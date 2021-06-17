# -*- coding: utf-8 -*-
"""
    Tests for the threshold class
"""
import pytest
import numpy as np

from eko.thresholds import ThresholdsAtlas, PathSegment


class TestPathSegment:
    def test_tuple(self):
        p = PathSegment(0, 1, 3)
        assert p.tuple == (0, 1, 3)
        # is hashable?
        d = dict()
        d[p.tuple] = 1
        assert d[p.tuple] == 1

    def test_repr(self):
        p = PathSegment(0, 1, 3)
        s = str(p)
        assert s.index("0") > 0
        assert s.index("3") > 0
        assert s.index("3") > 0


class TestThresholdsConfig:
    def test_init(self):
        # 3 thr
        tc3 = ThresholdsAtlas([1, 2, 3])
        assert tc3.area_walls == [0, 1, 2, 3, np.inf]
        # 2 thr
        tc2 = ThresholdsAtlas([0, 2, 3])
        assert tc2.area_walls == [0, 0, 2, 3, np.inf]

        # errors
        with pytest.raises(ValueError):
            ThresholdsAtlas([1.0, 0.0])

    def test_build_area_walls(self):
        for k in range(3, 6 + 1):
            walls = ThresholdsAtlas.build_area_walls([1, 2, 3], [1, 2, 3], k)
            assert len(walls) == k - 3

        with pytest.raises(ValueError):
            ThresholdsAtlas.build_area_walls([1, 2], [1, 2, 3], 4)
        with pytest.raises(ValueError):
            ThresholdsAtlas.build_area_walls([1, 2, 3], [1, 2], 4)
        with pytest.raises(ValueError):
            ThresholdsAtlas.build_area_walls([1, 2], [1, 2], 4)

    def test_from_dict(self):
        tc = ThresholdsAtlas.from_dict(
            {
                "mc": 1.0,
                "mb": 4.0,
                "mt": 100.0,
                "kcThr": 1,
                "kbThr": 2.0,
                "ktThr": np.inf,
                "Q0": 1.0,
                "MaxNfPdf": 6,
            }
        )
        assert tc.area_walls[1:-1] == [1.0, 64.0, np.inf]
        assert tc.q2_ref == 1.0

    def test_ffns(self):
        tc3 = ThresholdsAtlas.ffns(3)
        assert tc3.area_walls == [0] + [np.inf]
        tc4 = ThresholdsAtlas.ffns(4)
        assert tc4.area_walls == [0] * 2 + [np.inf]
        assert len(tc4.path(q2_to=2.0, q2_from=3.0)) == 1

    def test_path_3thr(self):
        tc = ThresholdsAtlas([1, 2, 3], 0.5)
        p1 = tc.path(0.7)
        assert len(p1) == 1
        assert p1[0].q2_from == 0.5
        assert p1[0].q2_to == 0.7
        assert p1[0].nf == 3

        p2 = tc.path(1.5, q2_from=2.5)
        assert len(p2) == 2
        assert p2[0].nf == 5
        assert p2[1].nf == 4

    def test_path_3thr_backward(self):
        tc = ThresholdsAtlas([1, 2, 3], 2.5)
        p1 = tc.path(0.7)
        assert len(p1) == 3
        assert p1[0].tuple == (2.5, 2.0, 5)
        assert p1[1].tuple == (2.0, 1.0, 4)
        assert p1[2].tuple == (1.0, 0.7, 3)

    def test_path_3thr_on_threshold(self):
        tc = ThresholdsAtlas([1, 2, 3], 0.5)
        # on the right of mc
        p3 = tc.path(1.0, nf_to=4)
        assert len(p3) == 2
        assert p3[0].nf == 3
        assert p3[1].tuple == (1.0, 1.0, 4)
        # on the left of mc
        p4 = tc.path(1.0, nf_to=3)
        assert len(p4) == 1
        assert p4[0].nf == 3
        # on the left of mt, across mb
        p5 = tc.path(1.5, q2_from=3.0, nf_from=5)
        assert len(p5) == 2
        assert p5[0].nf == 5
        assert p5[1].nf == 4

    def test_path_3thr_weird(self):
        tc = ThresholdsAtlas([1, 2, 3], 0.5)
        # the whole distance underground
        p6 = tc.path(3.5, nf_to=3)
        assert len(p6) == 1
        assert p6[0].tuple == (0.5, 3.5, 3)
        q2_from = 3.5
        q2_to = 0.7
        #                   0
        #      1 <-----------
        #      ---> 2
        #   3 < -----
        #      |    |    |
        p7 = tc.path(q2_to=q2_to, nf_to=5, q2_from=q2_from, nf_from=3)
        assert len(p7) == 3
        assert p7[0].nf == 3
        assert p7[1].nf == 4
        assert p7[2].nf == 5
        assert p7[0].q2_from == q2_from
        assert p7[2].q2_to == q2_to
        #                   0
        #      1 <-----------
        #      ---> 2 -> 3
        #   4 < ---------
        #      |    |    |
        p8 = tc.path(q2_to=q2_to, nf_to=6, q2_from=q2_from, nf_from=3)
        assert len(p8) == 4
        assert p8[0].nf == 3
        assert p8[1].nf == 4
        assert p8[2].nf == 5
        assert p8[3].nf == 6
        assert p8[0].q2_from == q2_from
        assert p8[3].q2_to == q2_to

    def test_nf(self):
        nf4 = ThresholdsAtlas.ffns(4)
        for q2 in [1.0, 1e1, 1e2, 1e3, 1e4]:
            assert nf4.nf(q2) == 4
        ta = ThresholdsAtlas([1, 2, 3], 0.5)
        assert ta.nf(0.9) == 3
        assert ta.nf(1.1) == 4
