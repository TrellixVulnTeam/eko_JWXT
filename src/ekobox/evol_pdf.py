# -*- coding: utf-8 -*-
import pathlib

import eko
from eko import basis_rotation as br
from ekomark import apply

from . import gen_info, genpdf


def evolve_pdfs(
    initial_PDF_list,
    theory_card,
    operators_card,
    path=None,
    store_path=None,
    targetgrid=None,
    install=False,
    name="Evolved_PDF",
    info_update=None,
):
    """
    This function evolves an initial_PDF using a theory card and an operator card
    and dump the evolved PDF in lhapdf format

    Parameters
    ----------
        initial_PDF_list : list(lhapdf object)
            list of PDF members to be evolved

        theory_card : dict
            theory card

        operators_card : dict
            operators card

        path : str
            path to cached eko output (if "None" it will be recomputed)

        store_path : str
            path where the eko is stored (if "None" will not be saved)

        targetgrid : list(float)
            target x-grid (if different from input x-grid)

        install : bool
            set whether to install evolved PDF to lhapdf directory

        name : str
            set name of evolved PDF

        info_update : dict
            dict of info to add or update to default info file

    """
    eko_output = None
    if path is not None:
        my_path = pathlib.Path(path)
        if my_path.is_dir():
            ops_id = f"o{operators_card['hash'][:6]}_t{theory_card['hash'][:6]}.tar"
            ops_id_path = pathlib.Path(ops_id)
            outpath = my_path / ops_id_path.relative_to(ops_id_path.anchor)
            eko_output = eko.output.Output.load_tar(outpath)
        else:
            eko_output = eko.output.Output.load_tar(my_path)
    else:
        eko_output = eko.run_dglap(theory_card, operators_card)
        if store_path is not None:
            eko_output.dump_tar(store_path)

    evolved_PDF_list = []
    for initial_PDF in initial_PDF_list:
        evolved_PDF_list.append(apply.apply_pdf(eko_output, initial_PDF, targetgrid))

    if targetgrid is None:
        targetgrid = operators_card["interpolation_xgrid"]
    if info_update is None:
        info_update = {}
    info_update["XMin"] = targetgrid[0]
    info_update["XMax"] = targetgrid[-1]
    info = gen_info.create_info_file(
        theory_card,
        operators_card,
        len(evolved_PDF_list),
        info_update=info_update,
    )
    all_member_blocks = []
    for evolved_PDF in evolved_PDF_list:
        all_blocks = []
        block = genpdf.generate_block(
            lambda pid, x, Q2, evolved_PDF=evolved_PDF: targetgrid[targetgrid.index(x)]
            * evolved_PDF[Q2]["pdfs"][pid][targetgrid.index(x)],
            xgrid=targetgrid,
            Q2grid=operators_card["Q2grid"],
            pids=br.flavor_basis_pids,
        )
        # all_blocks will be useful in case there will be necessity to dump many blocks
        # for a single member
        all_blocks.append(block)
        all_member_blocks.append(all_blocks)

    genpdf.export.dump_set(name, info, all_member_blocks)

    if install:
        genpdf.install_pdf(name)


def gen_out(theory_card, op_card, path=None):
    """
    Generates EKO output from theory and operators cards and, if requested,
    dumps it in tar format

    Parameters
    ----------
        theory_card : dict
            theory card
        op_card : dict
            operators card
        path : str
            path of dumped output (if "None" output is not dumped)

    Returns
    -------
        : eko.output.Output
            eko output
    """
    eko_output = eko.run_dglap(theory_card, op_card)
    if path is not None:
        ops_id = f"o{op_card['hash'][:6]}_t{theory_card['hash'][:6]}"
        path = f"{path}/{ops_id}.tar"
        eko_output.dump_tar(path)
    return eko_output
