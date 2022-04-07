# -*- coding: utf-8 -*-
import logging
import os
import pathlib
import tempfile
import typing
from dataclasses import dataclass, fields
from typing import Dict, Literal, Optional

import numpy as np

from .. import basis_rotation as br
from .. import interpolation
from .. import version as vmod

logger = logging.getLogger(__name__)


class DictLike:
    def __init__(self, **kwargs):
        pass

    @classmethod
    def from_dict(cls, dictionary):
        return cls(**dictionary)

    @property
    def raw(self):
        dictionary = {}
        for field in fields(self):
            value = getattr(self, field.name)

            # replace numpy arrays with lists
            if isinstance(value, np.ndarray):
                value = value.tolist()
            # replace numpy scalars with python ones
            elif isinstance(value, float):
                value = float(value)

            dictionary[field.name] = value

        return dictionary


@dataclass
class Operator(DictLike):
    alphas: float
    operator: np.ndarray
    error: Optional[np.ndarray] = None


@dataclass
class Debug(DictLike):
    skip_singlet: bool = False
    skip_non_singlet: bool = False


@dataclass
class Configs(DictLike):
    ev_op_max_order: int
    ev_op_iterations: int
    interpolation_polynomial_degree: int
    interpolation_is_log: bool
    backward_inversion: Literal["exact", "expanded"]
    n_integration_cores: int = 1


@dataclass
class Rotations(DictLike):
    targetgrid: Optional[np.ndarray] = None
    inputgrid: Optional[np.ndarray] = None
    targetpids: Optional[np.ndarray] = None
    inputpids: Optional[np.ndarray] = None

    @classmethod
    def default(cls, xgrid: interpolation.XGrid, pids: np.ndarray):
        return cls(
            targetgrid=xgrid.raw, inputgrid=xgrid.raw, targetpids=pids, inputpids=pids
        )


@dataclass
class EKO:
    """
    Wrapper for the output to help with application
    to PDFs and dumping to file.
    """

    xgrid: interpolation.XGrid
    Q02: float
    _operators: Dict[float, Optional[Operator]]
    configs: Configs
    rotations: Rotations
    debug: Debug
    pids: np.ndarray = np.array(br.flavor_basis_pids)
    version: str = vmod.__version__
    data_version: str = vmod.__data_version__

    def __iter__(self):
        """Iterate operators, with minimal load.

        Pay attention, this iterator:

        - is similar to ``dict.items()``, since it returns tuples of ``(q2,
          operator)``
        - is not a read-only operation from the point of view of the in-memory
          object (since the final result after iteration is no operator loaded)
        - but it is a read-only operation from the point of view of the
          permanent object on-disk

        Yields
        ------
        tuple
            couples of ``(q2, operator)``, loaded immediately before, unloaded
            immediately after

        """
        for q2 in self.Q2grid:
            yield q2, self[q2]
            del self[q2]

    def __contains__(self, q2: float) -> bool:
        return q2 in self._operators

    def __getitem__(self, q2: float):
        # TODO: autoload
        return self._operators[q2]

    def __setitem__(self, q2: float, op: Operator):
        # TODO: autodump
        if isinstance(op, dict):
            op = Operator.from_dict(op)
        if not isinstance(op, Operator):
            raise ValueError("Only operators can be stored.")
        self._operators[q2] = op

    def __delitem__(self, q2: float):
        """Drop operator from memory.

        This method only drops the operator from memory, and it's not expected
        to do anything else.

        Autosave is done on set, and explicit saves are performed by the
        computation functions.

        If a further explicit save is required, repeat explicit assignment::

            eko[q2] = eko[q2]

        This is only useful if the operator has been mutated in place, that in
        general should be avoided, since the operator should only be the result
        of a full computation or a library manipulation.


        Parameters
        ----------
        q2 : float
            the value of :math:`Q^2` for which the corresponding operator
            should be dropped

        """
        self._operators[q2] = None

    def items(self):
        return self._operators.items()

    @property
    def Q2grid(self):
        return np.array(list(self._operators))

    def approx(self, q2, rtol=1e-6, atol=1e-10) -> Optional[float]:
        q2s = self.Q2grid
        close = q2s[np.isclose(q2, q2s, rtol=rtol, atol=atol)]

        if close.size == 1:
            return close[0]
        if close.size == 0:
            return None
        raise ValueError(f"Multiple values of Q2 have been found close to {q2}")

    @classmethod
    def from_dict(cls, runcard: dict):
        """Make structure from runcard-like dictionary.

        This constructor is made to be used with loaded runcards, in order to
        minimize the amount of code needed to init a new object (you just to
        load the runcard and call this function).

        Note
        ----
        An object is initialized with no rotations, since the role of rotations
        is to keep the current state of the output object after manipulations
        happened.
        Since a new object is here in the process of being created, no rotation
        has to be logged.

        Parameters
        ----------
        runcard : dict
            a dictionary containing the runcard's content

        Returns
        -------
        EKO
            the generated structure

        """
        xgrid = interpolation.XGrid(runcard["xgrid"])
        pids = runcard.get("pids", cls.pids)
        return cls(
            xgrid=xgrid,
            pids=pids,
            Q02=runcard["Q0"] ** 2,
            _operators={q2: None for q2 in runcard["Q2grid"]},
            configs=Configs.from_dict(runcard["configs"]),
            rotations=Rotations.default(xgrid, pids),
            debug=Debug.from_dict(runcard.get("debug", {})),
        )

    @classmethod
    def load(cls, path):
        return cls(
            xgrid=None,
            Q02=None,
            _operators={q2: None for q2 in ()},
            configs=None,
            rotations=None,
            debug=None,
        )

    @property
    def raw(self):
        return dict(
            xgrid=self.xgrid.tolist(),
            Q0=float(np.sqrt(self.Q02)),
            Q2grid=self.Q2grid,
            configs=self.configs.raw,
            rotations=self.rotations.raw,
            debug=self.debug.raw,
        )

    def close(self):
        for q2 in self.Q2grid:
            del self[q2]

    def __del__(self):
        self.close()
