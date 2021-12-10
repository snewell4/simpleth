#!
"""
Compile Solidity contract source file(s).

Uses the Solidity ``compiler`` with ``options`` to compile the ``contract``
to create and write the specified artifact files to the ``out_dir`` directory.

**USAGE**

.. code-block:: none

   compile.py [-c ``compiler``] [-O ``options``] [-o ``out_dir``] ``contract`` [``contract``]

**EXAMPLES**

.. code-block:: none

   compile.py HelloWorld2.solc
   compile.py -c ..\solc\solc.exe HelloWorld2.sol
   compile.py -o . HelloWorld2.sol
   compile.py -O "--abi --overwrite" HelloWorld2.sol
   compile.py -c ..\solc\solc.exe -o . -O "--abi --overwrite" HelloWorld1.sol HelloWorld2.sol

**TERMINAL OUTPUT**

.. code-block:: none

   Compiler run successful. Artifact(s) can be found in directory ``out_dir``.

**ASSUMES**

The file type, `.py`, has been associated with `Python`. Otherwise, use:

.. code-block:: none

   python compile.py

**SEE ALSO**

-  To see the full help plus the default ``compiler``, ``options``,
   and ``out_dir``, from a command line do:

   .. code-block:: none

      compile.py -h

-  To see a description of compiler ``options`` and version, from a command line
   in the directory with ``compiler`` do:

   .. code-block:: none

      solc --help

"""
import os
from argparse import ArgumentParser, RawTextHelpFormatter

import simpleth

if __name__ == '__main__':
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
        '-o', '--out_dir',
        action='store',
        default=f'{simpleth.PROJECT_HOME}/{simpleth.ARTIFACT_SUBDIR}',
        help='output directory for artifact files\ndefault: %(default)s'
        )

    parser.add_argument(
        'contract',
        nargs='+',
        help='Solidity smart contract file to compile'
        )

    args = parser.parse_args()

    for file in args.contract:
        command = (
            f'{args.compiler} '
            f'-o {args.out_dir} '
            f'{args.options} '
            f'{file}'
            )
        r = os.system(command)
