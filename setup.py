from setuptools import setup, find_packages

LONG_DESCRIPTION = \
    'A set of five classes that simplify the use of Python ' \
    'to interact with Solidity smart contracts on a Ganache ' \
    'Ethereum blockchain. The classes allow developers to:  ' \
    'easily get details of the blockchain; deploy contracts ' \
    'onto the blockchain; run contract transactions; call ' \
    'contract functions; get values for contract public state ' \
    'variables; use filters to retrieve specific events; and ' \
    'get details on a transaction outcome.'

setup(
    name='simpleth',
    version='0.1.0',
    author='Stephen Newell',
    author_email='<snewell4@gmail.com>',
    description='Simplified Ethereum for Python',
    long_description=LONG_DESCRIPTION,
    url='https://github.com/snewell4/simpleth',
    packages=find_packages(),
    python_requires='>=3.8',    # adds Type.Final
    install_requires=[
        'web3.py>=5.23.0'       # adds maxPriorityFeePerGas
        ],
    keywords='blockchain, ganache, Solidity, ethereum, smart-contract',
    include_package_data=True,  # see manifest.ini
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: Microsoft :: Windows',
        'Topic :: Other/Nonlisted Topic'
        ]
    )
