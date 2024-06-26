# SPDX-License-Identifier: Apache-2.0
from pathlib import Path
import shutil

from tempfile import TemporaryDirectory
from click.testing import CliRunner

from neuroc.cli import scale

DATA = Path(__file__).resolve().parent / 'data'


def _prepare_folders(folder):
    '''
    Prepare an input and an output folder.

    The input folder contains 3 morphologies and a junk file
    '''
    input_folder = folder / 'input-folder'
    input_folder.mkdir()
    shutil.copy(DATA / 'neuron.asc', input_folder)
    shutil.copy(DATA / 'simple.asc', input_folder)
    shutil.copy(DATA / 'axon.asc', input_folder)
    (input_folder / 'crap.txt').touch()

    output_folder = folder / 'output-folder'
    output_folder.mkdir()

    return input_folder, output_folder


def test_cli():
    runner = CliRunner()

    with TemporaryDirectory(prefix='test-scale-file') as folder:
        folder = Path(folder)
        result = runner.invoke(scale, ['simple', 'file',
                                     '--scaling', '2.0',
                                     str(DATA / 'simple.asc'),
                                     str(folder / 'simple-scaled.asc')])
        assert result.exit_code == 0, result.exception
        assert len(list(folder.glob('*'))) == 1

    with TemporaryDirectory(prefix='test-scale-folder') as folder:
        folder = Path(folder)
        input_folder, output_folder = _prepare_folders(folder)

        result = runner.invoke(scale, ['simple', 'folder',
                                     '--scaling', '2.0',
                                     str(input_folder),
                                     str(output_folder)])
        assert result.exit_code == 0, result.exception
        assert len(list(output_folder.rglob('*'))) == 3


def test_rat_to_human():
    runner = CliRunner()

    with TemporaryDirectory(prefix='test-scale-file') as folder:
        folder = Path(folder)
        result = runner.invoke(scale, ['rat-to-human',
                                     str(DATA / 'human-cells' / 'neurondb.dat'),
                                     str(DATA / 'rat-cells' / 'neurondb.dat'),
                                     str(DATA / 'mapping.yaml'),
                                     str(folder)])
        assert result.exit_code == 0, result.exc_info
        assert len(list(folder.glob('*'))) == 5
