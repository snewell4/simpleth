#!
"""
Compile Solidity contract source file(s).

Uses the `solc.exe` compiler to compile the ``solidity_file``
with the ``options`` to create and write the specified artifact
files to the ``output`` directory.

**USAGE**
    compile.py test.sol
    compile.py *.sol
    compile.py -o "--abi --overwrite" -O ../artifact test.sol

**SEE ALSO**
From a command line do: ``solc --help`` to see compiler options.

"""
import os
from argparse import ArgumentParser, RawTextHelpFormatter

import simpleth

parser = ArgumentParser(
    description=__doc__,
    formatter_class=RawTextHelpFormatter
    )

parser.add_argument(
    '-c', '--compiler',
    action='store',
    default=(
        f'{simpleth.PROJECT_HOME}/'
        f'{simpleth.SOLC_SUBDIR}/'
        f'{simpleth.SOLC_FILENAME}'
        ),
    help='solc compiler\ndefault: %(default)s'
    )

parser.add_argument(
    '-O', '--options',
    action='store',
    default=(
        '--no-color '  # disable color output
        '--abi '  # output contract ABI file
        '--bin '  # output contract binary file
        '--bin-runtime '  # output contract runtime binary file
        '--userdoc '  # output Natspec user documentation
        '--devdoc  '  # output Natspec developer documentation
        '--overwrite '  # overwrite existing artifact files
        '--optimize'  # enable bytecode optimizer
        ),
    help='solc compiler options\ndefault: %(default)s'
    )

parser.add_argument(
    '-i', '--in_dir',
    action='store',
    default=f'{simpleth.PROJECT_HOME}/{simpleth.SOLIDITY_SOURCE_SUBDIR}',
    help='input directory for smart contract source files\ndefault: %(default)s'
    )

parser.add_argument(
    '-o', '--out_dir',
    action='store',
    default=f'{simpleth.PROJECT_HOME}/{simpleth.ARTIFACT_SUBDIR}',
    help='output directory for artifact files\ndefault: %(default)s'
    )

parser.add_argument(
    'solidity_file',
    nargs='+',
    help='Solidity smart contract file to compile'
    )

args = parser.parse_args()

for file in args.solidity_file:
    command = (
        f'{args.compiler} '
        f'-o {args.out_dir} '
        f'{args.options} '
        f'{args.in_dir}/{file}'
        )
    r = os.system(command)
