# -*- coding: utf-8 -*-
"""
This module contains the definitions of the different basis used, i.e.:

- flavor basis::

    22  -6  -5  -4  -3  -2  -1   21  1   2   3   4   5   6
    gm  tb  bb  cb  sb  ub  db   g   d   u   s   c   b   t

- QCD Evolution basis::

    0   1   2   3   4   5   6   7   8   9  10  11  12  13
    gm  S   g   V   V3  V8 V15 V24 V35  T3 T8  T15 T24 T35

"""

import copy

import numpy as np

flavor_basis_pids = [22] + list(range(-6, -1 + 1)) + [21] + list(range(1, 6 + 1))

evol_basis = [
    "ph",
    "S",
    "g",
    "V",
    "V3",
    "V8",
    "V15",
    "V24",
    "V35",
    "T3",
    "T8",
    "T15",
    "T24",
    "T35",
]

# Tranformation from physical basis to QCD evolution basis
rotate_flavor_to_evolution = np.array(
    [
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, -1, -1, -1, -1, -1, -1, 0, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, -0, -1, 1, 0, -1, 1, 0, -0, 0, 0],
        [0, 0, 0, 0, 2, -1, -1, 0, 1, 1, -2, -0, 0, 0],
        [0, 0, 0, 3, -1, -1, -1, 0, 1, 1, 1, -3, 0, 0],
        [0, 0, 4, -1, -1, -1, -1, 0, 1, 1, 1, 1, -4, 0],
        [0, 5, -1, -1, -1, -1, -1, 0, 1, 1, 1, 1, 1, -5],
        [0, 0, 0, -0, 0, 1, -1, 0, -1, 1, 0, -0, 0, 0],
        [0, 0, 0, -0, -2, 1, 1, 0, 1, 1, -2, -0, 0, 0],
        [0, 0, 0, -3, 1, 1, 1, 0, 1, 1, 1, -3, 0, 0],
        [0, 0, -4, 1, 1, 1, 1, 0, 1, 1, 1, 1, -4, 0],
        [0, -5, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, -5],
    ]
)

# inverse transformation
rotate_evolution_to_flavor = np.linalg.inv(rotate_flavor_to_evolution)


def generate_input_from_lhapdf(lhapdf, Q2init):
    """
    Rotate lhapdf-like input object from flavor space to evolution space

    Parameters
    ----------
        lhapdf : object
            lhapdf-like input object (i.e. an object with xfxQ2)
        Q2init : float
            input scale

    Returns
    -------
        input_dict : dict
            a mapping evolution element to callable
    """
    input_dict = {}
    for j, evol in enumerate(evol_basis):

        def f(x, j=j):
            """factory function"""
            evol_map = rotate_flavor_to_evolution[j]
            flavor_list = np.array(
                [lhapdf.xfxQ2(pid, x, Q2init) / x for pid in flavor_basis_pids]
            )
            return evol_map @ flavor_list

        input_dict[evol] = f
    return input_dict

def fill_trivial_dists(old_evols):
    """
    Insert trivial evolutions basis elements.

    Parameters
    ----------
        old_evols : dict
            :class:`eko.evolution_operator.PhysicalOperator`-like dictionary

    Returns
    -------
        evols : dict
            updated dictionary
        trivial_dists : list
            inserted elements
    """
    evols = copy.deepcopy(old_evols)
    trivial_dists = []
    for evol in evol_basis:
        # only rotate in quark distributions
        if evol == "g":
            continue
        # are the target distributions there?
        if evol in ["S", "V"]:
            if evol not in evols:
                raise KeyError(f"No {evol} distribution available")
            continue
        # PDF is set?
        if evol in evols:
            continue
        # insert empty photon
        if evol == "ph":
            evols[evol] = np.zeros(len(evols["S"]))
        # insert trivial value
        elif evol[0] == "V":
            evols[evol] = evols["V"]
        elif evol[0] == "T":
            evols[evol] = evols["S"]
        # register for later use
        trivial_dists.append(evol)
    return evols, trivial_dists

def rotate_output(in_evols):
    """
    Rotate lists in evolution basis back to flavor basis.

    Parameters
    ----------
        in_evols : dict
            :class:`eko.evolution_operator.PhysicalOperator`-like dictionary

    Returns
    -------
        out : dict
            rotated dictionary
    """
    # prepare
    evols, trivial_dists = fill_trivial_dists(in_evols)
    evol_list = np.array([evols[evol] for evol in evol_basis])
    final_quark_pid = 6
    final_valence_pid = 6
    for q in range(6,3,-1):
        if f"T{q*q-1}" in trivial_dists:
            final_quark_pid -= 1
            # assume Vxx too vanish
            final_valence_pid -= 1
            continue
        if f"V{q*q-1}" in trivial_dists:
            final_valence_pid -= 1
    # rotate
    out = {}
    for j, pid in enumerate(flavor_basis_pids):
        # skip empty quarks
        if (6 >= pid > final_quark_pid) or (-6 <= pid < -final_valence_pid):
            continue
        # skip photon
        if pid == 22 and "ph" in trivial_dists:
            continue
        flavor_map = rotate_evolution_to_flavor[j]
        out[pid] = flavor_map @ evol_list
    # recover the bared distributions, e.g. tbar = t
    for q in range(-final_quark_pid,-final_valence_pid):
        out[q] = out[-q]
    return out
