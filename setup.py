from setuptools import setup

setup(
    name='simpleth',
    version='0.1.29',
    author='Stephen Newell',
    author_email='<snewell4@gmail.com>',
    description='Simplified Ethereum for Python',
    long_description=open('README.rst').read(),
    long_description_content_type='text/x-rst',
    url='https://github.com/snewell4/simpleth',
    license='LICENSE.txt',
    packages=['simpleth'],
    package_dir={'simpleth': 'src/simpleth'},
    package_data={'simpleth': ['examples/event_poll.py']},
    include_package_data=True,
    python_requires='>=3.7',              # arbitrary choice
    install_requires=['web3>=5.23.0'],   # adds maxPriorityFeePerGas
    keywords='blockchain, ganache, Solidity, ethereum, smart-contract, contract',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: Microsoft :: Windows',
        'Topic :: Other/Nonlisted Topic'
        ],
    data_files=[
        ('artifacts', [
                'artifacts/HelloWorld1.abi',
                'artifacts/HelloWorld1.bin',
                'artifacts/HelloWorld2.abi',
                'artifacts/HelloWorld2.bin',
                'artifacts/HelloWorld3.abi',
                'artifacts/HelloWorld3.bin',
                'artifacts/HelloWorld4.abi',
                'artifacts/HelloWorld4.bin',
                'artifacts/Test.abi',
                'artifacts/Test.bin',
                'artifacts/TestNeverDeployed.abi',
                'artifacts/TestNeverDeployed.bin'
                ]),
        ('contracts', [
            'src/contracts/HelloWorld1.sol',
            'src/contracts/HelloWorld2.sol',
            'src/contracts/HelloWorld3.sol',
            'src/contracts/HelloWorld4.sol',
            'src/contracts/Test.sol'
            ]),
        ('examples', [
            'examples/event_poll.py',
            'examples/hello_world1.py',
            'examples/hello_world2.py',
            'examples/hello_world3.py',
            'examples/hello_world4.py'
            ])
        ]
    )
