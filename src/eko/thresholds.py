# -*- coding: utf-8 -*-
r"""
This module holds the classes that define the flavor number schemes (FNS).

Run card parameters:

.. include:: /code/IO-tabs/ThresholdConfig.rst
"""
import logging
import numbers

import numpy as np

logger = logging.getLogger(__name__)


class Area:
    """
    Sets up a single threhold area with a fixed configuration.

    Parameters
    ----------
        q2_min : float
            lower bound of the area
        q2_max : float
            upper bound of the area
        q2_0 : float
            reference point of the area (can be anywhere in the area)
        nf : float
            number of flavours in the area
    """

    def __init__(self, q2_min, q2_max, q2_0, nf):
        self.q2_min = q2_min
        self.q2_max = q2_max
        self.nf = nf
        self.has_q2_0 = False
        # Now check which is the q2_ref for this area
        if q2_0 > q2_max:
            self.q2_ref = q2_max
        elif q2_0 < q2_min:
            self.q2_ref = q2_min
        else:
            self.has_q2_0 = True
            self.q2_ref = q2_0

    def q2_towards(self, q2):
        """
        Return q2_min or q2_max depending on whether
        we are going towards the max or the min or q2
        if we are alreay in the correct area

        Parameters
        ----------
            q2 : float
                reference point

        Returns
        -------
            q2_next : float
                the closest point to q2 that is within the area
        """
        if q2 > self.q2_max:
            return self.q2_max
        elif q2 < self.q2_min:
            return self.q2_min
        else:
            return q2

    def __gt__(self, target_area):
        """Compares q2 of areas"""
        return self.q2_min >= target_area.q2_max

    def __lt__(self, target_area):
        """Compares q2 of areas"""
        return self.q2_max <= target_area.q2_min

    def __call__(self, q2):
        """
        Checks whether q2 is contained in the area

        Parameters
        ----------
            q2 : float
                testing point

        Returns
        -------
            contained : bool
                is point contained?
        """
        return self.q2_min <= q2 <= self.q2_max


class ThresholdsConfig:
    """
    The threshold class holds information about the thresholds any
    Q2 has to pass in order to get there from a given q2_ref and scheme.

    Parameters
    ----------
        q2_ref : float
            Reference q^2
        scheme: str
            Choice of scheme
        threshold_list: list
            List of q^2 thresholds should the scheme accept it
        nf: int
            Number of flavors for the FFNS
    """

    def __init__(self, q2_ref, scheme, *, threshold_list=None, nf=None):
        # Initial values
        self.q2_ref = q2_ref
        self.scheme = scheme
        self._areas = []
        self._area_walls = []
        self._area_ref = 0
        self.max_nf = None
        self.min_nf = None

        if scheme == "FFNS":
            if nf is None:
                raise ValueError("No value for nf in the FFNS was received")
            if threshold_list is not None:
                raise ValueError("The FFNS does not accept any thresholds")
            self._areas = [Area(0, np.inf, self.q2_ref, nf)]
            self.max_nf = nf
            self.min_nf = nf
            logger.info("Fixed flavor number scheme with %d flavors", nf)
        elif scheme in ["ZM-VFNS", "FONLL-A", "FONLL-A'"]:
            if scheme not in ["FONLL-A"] and nf is not None:
                logger.warning(
                    "The VFNS configures its own value for nf, ignoring input nf=%d",
                    nf,
                )
            if threshold_list is None:
                raise ValueError(
                    "The VFN scheme was selected but no thresholds were given"
                )
            self._setup_vfns(threshold_list, nf)
            logger.info("Variable flavor number scheme (%s)", scheme)
        else:
            raise NotImplementedError(f"The scheme {scheme} is not implemented")

    @classmethod
    def from_dict(cls, theory_card):
        """
        Create the object from the run card.

        Parameters
        ----------
            theory_card : dict
                run card with the keys given at the head of the :mod:`module <eko.thresholds>`

        Returns
        -------
            cls : ThresholdConfig
                created object
        """
        FNS = theory_card["FNS"]
        q2_ref = pow(theory_card["Q0"], 2)
        if FNS == "FFNS":
            return cls(q2_ref, FNS, threshold_list=None, nf=theory_card["NfFF"])
        # the threshold value does not necessarily coincide with the mass
        def thres(pid):
            heavy_flavors = "cbt"
            flavor = heavy_flavors[pid - 4]
            return pow(theory_card[f"m{flavor}"] * theory_card[f"k{flavor}Thr"], 2)
        if FNS in ["FONLL-A"]:
            nf = theory_card["NfFF"]
            if nf <= 3:
                raise ValueError("NfFF should point to the heavy quark! i.e. NfFF>3")
            threshold_list = [thres(nf)]
            return cls(q2_ref, FNS, threshold_list=threshold_list, nf=nf-1)
        # setup VFNS
        threshold_list = [thres(q) for q in range(4, 6 + 1)]
        return cls(q2_ref, FNS, threshold_list=threshold_list)

    @property
    def nf_ref(self):
        """ Number of flavours in the reference area """
        return self._areas[self._area_ref].nf

    def nf_range(self):
        """
        Iterate number of flavours, including min_nf *and* max_nf

        Yields
        ------
            nf : int
                number of flavour
        """
        return range(self.min_nf, self.max_nf + 1)

    def _setup_vfns(self, threshold_list, nf=None):
        """
        Receives a list of thresholds and sets up the vfns scheme

        Parameters
        ----------
            threshold_list: list
                List of q^2 thresholds
        """
        if nf is None:
            nf = 3
        # Force sorting
        self._area_walls = sorted(threshold_list)
        # Generate areas
        self._areas = []
        q2_min = 0
        q2_ref = self.q2_ref
        self.min_nf = nf
        for i, q2_max in enumerate(self._area_walls + [np.inf]):
            nf = self.min_nf + i
            new_area = Area(q2_min, q2_max, q2_ref, nf)
            if new_area.has_q2_0:
                self._area_ref = i
            self._areas.append(new_area)
            q2_min = q2_max
        self.max_nf = nf

    def get_path_from_q2_ref(self, q2):
        """
        Get the Area path from q2_ref to q2.

        Parameters
        ----------
            q2: float
                Target value of q2

        Returns
        -------
            area_path: list
                List of Areas to go through in order to get from q2_ref
                to q2. The first one is the one containg q2_ref while the
                last one contains q2
        """
        current_area = self.get_areas_idx(q2)[0]
        if current_area < self._area_ref:
            rc = -1
        else:
            rc = 1
        area_path = [
            self._areas[i] for i in range(self._area_ref, current_area + rc, rc)
        ]
        return area_path

    def get_areas_idx(self, q2arr):
        """
        Returns the index of the area in which each value of q2arr falls.

        Parameters
        ----------
            q2arr: np.array
                array of values of q2

        Returns
        -------
            areas_idx: list
                list with the indices of the corresponding areas for q2arr
        """
        # Ensure q2arr is an array
        if isinstance(q2arr, numbers.Number):
            q2arr = np.array([q2arr])
        # Check in which area is every q2
        areas_idx = np.digitize(q2arr, self._area_walls)
        return areas_idx

    def get_areas(self, q2arr):
        """
        Returns the Areas in which each value of q2arr falls

        Parameters
        ----------
            q2arr: np.array
                array of values of q2

        Returns
        -------
            areas: list
                list with the areas for q2arr
        """
        idx = self.get_areas_idx(q2arr)
        area_list = np.array(self._areas)[idx]
        return list(area_list)
