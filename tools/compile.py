#!
"""
Compile Solidity contract source file(s) for use by simpleth.

Uses the Solidity compiler with ``options`` to compile the ``contract``
to create and write the specified artifact files to the ``out_dir`` directory.

With the defaults, the result makes the contract ready to be used by
the simpleth classes. The newly compiled contract can be loaded onto
the Ganache blockchain by doing a Contract().deploy().

The default location of ``solc.exe``, the Solidity compiler, is
in a subdirectory to the current working directory named, ``solc``.
A full path default to this directory can be set in the
environment variable, ``SIMPLETH_SOLC_DIR``.


**USAGE**

.. code-block:: none

   compile.py [-c <compiler>] [-O <options>] [-o <out_dir>] <contract> [<contract> ...]


**EXAMPLES**

.. code-block:: none

   compile.py HelloWorld2.solc
   compile.py -c ..\\solc\\solc.exe HelloWorld2.sol
   compile.py -o . HelloWorld2.sol
   compile.py -O "--abi --overwrite" HelloWorld2.sol
   compile.py -c ..\\solc\\solc.exe -o . -O "--abi --overwrite" HelloWorld1.sol HelloWorld2.sol


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


**MODULES**
"""
import os
from argparse import ArgumentParser

import simpleth

SOLC_DIR_ENV_VAR: str = 'SIMPLETH_SOLC_DIR'
"""Environment variable name for filepath to directory holding compiler"""
SOLC_DIR_DEFAULT: str = '.'
"""If environment variable not set, look for compiler in current working
directory"""
SOLC_FILENAME: str = 'solc.exe'
"""Filename for Solidity compiler"""


def main():
    """Compile Solidity contract source file(s) for use by simpleth"""

    artifact_dir: str = os.environ.get(
        simpleth.ARTIFACTS_DIR_ENV_VAR,
        simpleth.ARTIFACTS_DIR_DEFAULT
        )
    solc_dir: str = os.environ.get(
        SOLC_DIR_ENV_VAR,
        SOLC_DIR_DEFAULT
        )

    parser = ArgumentParser(
        description='Compile Solidity contract source file(s) for use by simpleth'
        )

    parser.add_argument(
        '-c', '--compiler',
        action='store',
        default=f'{solc_dir}\\{SOLC_FILENAME}',
        help='solc compiler\ndefault: %(default)s'
        )

    parser.add_argument(
        '-O', '--options',
        action='store',
        default=(
            '--no-color '  # disable color output
            '--abi '  # output contract ABI file
            '--bin '  # output contract binary file
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
        default=artifact_dir,
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
#        print(f' DEBUG\n compiler={args.compiler}\n out={args.out_dir}\n options={args.options}\n file={file}\n')
        os.system(command)


if __name__ == '__main__':
    main()
