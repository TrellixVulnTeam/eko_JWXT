# -*- coding: utf-8 -*-

from click.testing import CliRunner

from ekobox.genpdf.cli import cli


def test_genpdf_CLI_messages():
    runner = CliRunner()
    result = runner.invoke(cli, ["generate"])
    assert "Error: Missing argument 'NAME'." in result.output
    result = runner.invoke(cli, ["install"])
    assert "Error: Missing argument 'NAME'." in result.output
    result = runner.invoke(cli, ["generate", "TestEmptyLabels"])
    assert result.exception and "Labels must contain at least one element" in str(
        result.exception
    )
    result = runner.invoke(cli, ["generate", "--help"])
    assert "-p, --parent-pdf-set TEXT" in result.output
    assert "-m, --members" in result.output
    assert "-i, --install" in result.output


def test_genpdf_CLI(fake_lhapdf, cd):
    n = "test_genpdf_CLI"
    runner = CliRunner()
    result = None
    with cd(fake_lhapdf):
        result = runner.invoke(cli, ["generate", n, "21"])
    assert result is not None
    assert result.exception is None
    p = fake_lhapdf / n
    assert p.exists()
    pi = p / f"{n}.info"
    assert pi.exists()
    pm = p / f"{n}_0000.dat"
    assert pm.exists()
