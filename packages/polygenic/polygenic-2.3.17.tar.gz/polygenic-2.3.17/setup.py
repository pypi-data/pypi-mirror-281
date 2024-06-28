#! /usr/bin/python
# -*- coding: utf-8 -*-

import setuptools
from typing import List
from setuptools import setup, find_packages

PACKAGE_VERSION = '2.3.17'

def write_version_py(filename='polygenic/version.py'):
    cnt = """
# THIS FILE IS GENERATED FROM SETUP.PY
__version__ = '{}'
"""
    with open(filename, 'w') as f:
        f.write(cnt.format(PACKAGE_VERSION))

write_version_py()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="polygenic",
    version=PACKAGE_VERSION,
    author="Marcin Piechota, Wojciech Galan",
    author_email="piechota@intelliseq.com",
    description="Polygenic score toolkit",
    #long_description=long_description,
    #long_description_content_type="text/reStructuredText",
    url="https://github.com/marpiech/polygenic",
    packages=setuptools.find_packages(include=['polygenic','polygenic.core','polygenic.data','polygenic.error','polygenic.rsidx','polygenic.lib','polygenic.tools','polygenic.tools.data','polygenic.model']),
    package_data={'polygenic': ['*.cfg'], 'polygenic': ['resources/chromsizes/*.sizes']},
    license="Intelliseq dual licenses this package. For commercial use, please contact [contact @ intelliseq.com](mailto:contact@intelliseq.com). For non-commercial use, this license permits use of the software only by government agencies, schools, universities, non-profit organizations or individuals on projects that do not receive external funding other than government research grants and contracts. Any other use requires a commercial license. For the full license, please see [LICENSE.md](https://github.com/intelliseq/polygenic/blob/master/LICENSE.md), in this source repository.",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: Free for non-commercial use',
        'Programming Language :: Python :: 3',
        'Operating System :: Unix',
        'Operating System :: MacOS',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    install_requires=[
        'numpy',
        'scipy',
        'progressbar2',
        'python-utils',
        'pysam',
        'pytabix',
        'pandas',
        'plotly',
        'kaleido',
        'DotMap',
        'pyyaml',
        'tqdm',
        'plotnine',
        'kaleido',
        'polars',
        'importlib-resources',
        'logdecorator',
        'pyarrow'
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'polygenic=polygenic.pgstk:main',
            'polygenictk=polygenic.pgstk:main',
            'pgstk=polygenic.pgstk:main'
        ],
    },
    test_suite='nose.collector',
    tests_require=['nose>=1.0'],
    setup_requires=['nose>=1.0'],
)
