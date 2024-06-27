#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ ]

test_requirements = [ ]

setup(
    author="Burak Atakan",
    author_email='burak.atakan@uni-due.de',
    python_requires='>=3.10',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    description="Modeling Carnot Batteries (Thermal Energy Storage), a Python package.",
    install_requires=requirements,
    extras_require={
        'trend':['fluid',]},
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='carbatpy',
    name='carbatpy',
    # packages=find_packages(where =['src','src.models', 'src.models.*',
    #                                'src.utils','src.helpers']),
                           # include=['carbatpy', 'carbatpy.*', 'src.*', 'tests' ]),
    package_dir={'': 'src'},
    test_suite='tests',
    tests_require=test_requirements,
    url='https://git.uni-due.de/spp-2403/td-ude/carbatpy',
    version='0.1.7',
    zip_safe=False,
)
