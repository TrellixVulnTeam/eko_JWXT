# -*- coding: utf-8 -*-
r"""
The write-up of the matching conditions is given in
:doc:`Matching Conditions </theory/Matching>`.

"""

import numpy as np

from .. import basis_rotation as br
from .. import constants


def pids_from_intrinsic_evol(label, nf, normalize):
    r"""
    Obtain the list of pids with their corresponding weight, that are contributing to ``evol``

    The normalization of the weights is only needed for the output rotation:

    - if we want to build e.g. the singlet in the initial state we simply have to sum
      to obtain :math:`S = u + \bar u + d + \bar d + \ldots`
    - if we want to rotate back in the output we have to *normalize* the weights:
      e.g. in nf=3 :math:`u = \frac 1 6 S + \frac 1 6 V + \ldots`

    The normalization can only happen here since we're actively cutting out some
    flavor (according to ``nf``).

    Parameters
    ----------
        evol : str
            evolution label
        nf : int
            maximum number of light flavors
        normalize : bool
            normalize output

    Returns
    -------
        m : list
    """
    try:
        evol_idx = br.evol_basis.index(label)
        is_evol = True
    except ValueError:
        is_evol = False
    if is_evol:
        weights = br.rotate_flavor_to_evolution[evol_idx].copy()
        for j, pid in enumerate(br.flavor_basis_pids):
            if nf < abs(pid) <= 6:
                weights[j] = 0
    else:
        weights = rotate_pm_to_flavor(label)
    # normalize?
    if normalize:
        norm = weights @ weights
        weights = weights / norm
    return weights


def get_range(evol_labels, is_qed=False):
    """
    Determine the number of light and heavy flavors participating in the input and output.

    Here, we assume that the T distributions (e.g. T15) appears *always*
    before the corresponding V distribution (e.g. V15).

    Returns
    -------
        nf_in : int
            number of light flavors in the input
        nf_out : int
            number of light flavors in the output
    """
    nf_in = 3
    nf_out = 3

    def update(label, is_qed=False):
        nf = 3
        if label[0] == "T":
            if not is_qed:
                nf = round(np.sqrt(int(label[1:]) + 1))
            else:
                if label[1:] == "d3":
                    nf = 3
                elif label[1:] == "u3":
                    nf = 4
                elif label[1:] == "d8":
                    nf = 5
                elif label[1:] == "u8":
                    nf = 6
                else:
                    raise ValueError(f"{label[1:]} is not possible")
        return nf

    for op in evol_labels:
        nf_in = max(update(op.input, is_qed), nf_in)
        nf_out = max(update(op.target, is_qed), nf_out)

    return nf_in, nf_out


def rotate_pm_to_flavor(label):
    """
    Rotate from +- basis to flavor basis.

    Parameters
    ----------
        label : str
            label

    Returns
    -------
        l : list(float)
            list of weights
    """
    # g and ph are unaltered
    if label in ["g", "ph"]:
        return br.rotate_flavor_to_evolution[br.evol_basis.index(label)].copy()
    # no it has to be a quark with + or - appended
    if label[0] not in br.quark_names or label[1] not in ["+", "-"]:
        raise ValueError(f"Invalid pm label: {label}")
    l = np.zeros(len(br.flavor_basis_pids))
    idx = br.flavor_basis_names.index(label[0])
    pid = br.flavor_basis_pids[idx]
    l[idx] = 1
    # + is +, - is -
    if label[1] == "+":
        l[br.flavor_basis_pids.index(-pid)] = 1
    else:
        l[br.flavor_basis_pids.index(-pid)] = -1
    return l


def rotate_matching(nf, is_qed=False, inverse=False):
    """
    Rotation between matching basis (with e.g. S,g,...V8 and c+,c-) and new true evolution basis
    (with S,g,...V8,T15,V15).

    Parameters
    ----------
        nf : int
            number of active flavors in the higher patch: to activate T15, nf=4
        inverse : bool
            use inverse conditions?

    Returns
    -------
        l : dict
            mapping in dot notation between the bases
    """
    # the gluon and the photon do not care about new quarks
    l = {"g.g": 1.0, "ph.ph": 1.0}
    # already active distributions
    q = br.quark_names[nf - 1]
    if not is_qed:
        for k in range(2, nf):  # nf is the upper, so excluded
            n = k**2 - 1
            l[f"V{n}.V{n}"] = 1.0
            l[f"T{n}.T{n}"] = 1.0
        # the new contributions
        n = nf**2 - 1  # nf is pointing upwards
        for (tot, oth, qpm) in (("S", f"T{n}", f"{q}+"), ("V", f"V{n}", f"{q}-")):
            if inverse:
                l[f"{tot}.{tot}"] = (nf - 1.0) / nf
                l[f"{tot}.{oth}"] = 1.0 / nf
                l[f"{qpm}.{tot}"] = 1.0 / nf
                l[f"{qpm}.{oth}"] = -1.0 / nf
            else:
                l[f"{tot}.{tot}"] = 1.0
                l[f"{tot}.{qpm}"] = 1.0
                l[f"{oth}.{tot}"] = 1.0
                l[f"{oth}.{qpm}"] = -(nf - 1.0)
    else:
        name = {3: "d3", 4: "u3", 5: "d8", 6: "u8"}
        for k in range(3, nf):
            l[f"V{name[k]}.V{name[k]}"] = 1.0
            l[f"T{name[k]}.T{name[k]}"] = 1.0
        for (tot, totdelta, oth, qpm) in (
            ("S", "Sdelta", f"T{name[nf]}", f"{q}+"),
            ("V", "Vdelta", f"V{name[nf]}", f"{q}-"),
        ):
            a = a(nf)
            b = b(nf)
            c = c(nf)
            d = d(nf)
            if inverse:
                den = c - a - b * d
                l[f"{tot}.{tot}"] = (c - b * d) / den
                l[f"{tot}.{totdelta}"] = b / den
                l[f"{tot}.{oth}"] = -1 / den
                l[f"{totdelta}.{tot}"] = a * d / den
                l[f"{totdelta}.{totdelta}"] = (c - a) / den
                l[f"{totdelta}.{oth}"] = -d / den
                l[f"{qpm}.{tot}"] = -a / den
                l[f"{qpm}.{totdelta}"] = -b / den
                l[f"{qpm}.{oth}"] = 1 / den
            else:
                l[f"{tot}.{tot}"] = 1.0
                l[f"{tot}.{totdelta}"] = 0.0
                l[f"{tot}.{qpm}"] = 1.0
                l[f"{totdelta}.{tot}"] = 0.0
                l[f"{totdelta}.{totdelta}"] = 1.0
                l[f"{totdelta}.{qpm}"] = d
                l[f"{oth}.{tot}"] = a
                l[f"{oth}.{totdelta}"] = b
                l[f"{oth}.{qpm}"] = c
    # also higher quarks do not care
    for k in range(nf + 1, 6 + 1):
        q = br.quark_names[k - 1]
        for sgn in "+-":
            l[f"{q}{sgn}.{q}{sgn}"] = 1.0
    return l


def rotate_matching_inverse(nf, is_qed=False):
    return rotate_matching(nf, is_qed, True)


def a(nf):
    if nf in [4, 6]:  # heavy flavor is up-like
        return constants.uplike_flavors(nf - 1) / (nf - 1)
    elif nf in [3, 5]:  # heavy flavor is down-like
        nd = (nf - 1) - constants.uplike_flavors(nf - 1)
        return nd / (nf - 1)


def b(nf):
    nu_frac_nf = constants.uplike_flavors(nf - 1) / (nf - 1)
    if nf in [4, 6]:  # heavy flavor is up-like
        return nu_frac_nf
    elif nf in [3, 5]:  # heavy flavor is down-like
        return -nu_frac_nf


def c(nf):
    if nf in [4, 6]:  # heavy flavor is up-like
        return -1
    elif nf in [3, 5]:  # heavy flavor is down-like
        return -2


def d(nf):
    if nf in [4, 6]:  # heavy flavor is up-like
        nu = constants.uplike_flavors(nf - 1)
        nd = (nf - 1) - nu
        return nd / nu
    elif nf in [3, 5]:  # heavy flavor is down-like
        return -1


def pids_from_intrinsic_unified_evol(label, nf, normalize):
    r"""
    Obtain the list of pids with their corresponding weight, that are contributing to intrinsic
    unified evolution.

    Parameters
    ----------
        evol : str
            evolution label
        nf : int
            maximum number of light flavors
        normalize : bool
            normalize output

    Returns
    -------
        m : list
    """
    if label in ["ph", "g", "S", "V"]:
        return pids_from_intrinsic_evol(label, nf, normalize)
    if label[0] in br.quark_names[3:]:
        weights = rotate_pm_to_flavor(label)
    else:
        weights = np.array([0.0] * len(br.flavor_basis_pids))
        mapping = {
            "d3": {1: 1.0, 3: -1.0},  # T3d = d+ - s+
            "d8": {1: 1.0, 3: 1.0, 5: -2.0},  # T8d = d+ + s+ - 2b+
            "u3": {2: 1.0, 4: -1.0},  # T3u = u+ - c+
            "u8": {2: 1.0, 4: 1.0, 6: -2.0},  # T8u = u+ + c+ - 2t+
            "delta": {
                3: {2: 2.0, 1: -1.0, 3: -1.0},  # Sdelta = 2u+ - d+ -s+
                4: {2: 1.0, 4: 1.0, 1: -1.0, 3: -1.0},  # Sdelta = u+ + c+ - d+ - s+
                5: {
                    2: 3.0 / 2.0,
                    4: 3.0 / 2.0,
                    1: -1.0,
                    3: -1.0,
                    5: -1.0,
                },  # Sdelta = 3/2u+ + 3/2c+ - d+ - s+ - b+
                6: {
                    2: 1.0,
                    4: 1.0,
                    6: 1.0,
                    1: -1.0,
                    3: -1.0,
                    5: -1.0,
                },  # Sdelta = u+ + c+ + t+ - d+ -s+ - b+
            },
        }
        cur_map = mapping[label[1:]]
        if label[1:] == "delta":
            cur_map = cur_map[nf]
        for q, w in cur_map.items():
            weights[br.flavor_basis_pids.index(q)] = w
            weights[br.flavor_basis_pids.index(-q)] = (
                -1 if label[0] == "V" else 1.0
            ) * w

    # normalize?
    if normalize:
        norm = weights @ weights
        weights = weights / norm
    return weights
