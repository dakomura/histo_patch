# Author: Daisuke Komura <kdais-prm@m.u-tokyo.ac.jp>
# Copyright (c) 2022 Daisuke Komura
# License: BSD 3 clause

from setuptools import setup
import histo_patch

DESCRIPTION = "histo-patch: image patch extraction from Whole Slide Images"
NAME = 'histo-patch'
AUTHOR = 'Daisuke Komura'
AUTHOR_EMAIL = 'kdais-prm@m.u-tokyo.ac.jp'
URL = 'https://github.com/dakomura/histo_patch'
LICENSE = 'BSD 3-Clause'
DOWNLOAD_URL = 'https://github.com/dakomura/histo_patch'
VERSION = histo_patch.__version__
PYTHON_REQUIRES = ">=3.6"

INSTALL_REQUIRES = [
    'matplotlib>=3.3.4',
    'seaborn>=0.11.0',
    'numpy >=1.20.3',
    'pandas>=1.2.4',
    'matplotlib>=3.3.4',
    'scipy>=1.6.3',
    'scikit-learn>=0.24.2',
]

EXTRAS_REQUIRE = {
    'tutorial': [
        'mlxtend>=0.18.0',
        'xgboost>=1.4.2',
    ]
}

PACKAGES = [
    'seaborn_analyzer'
]

CLASSIFIERS = [
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: BSD License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3 :: Only',
    'Topic :: Scientific/Engineering',
    'Topic :: Scientific/Engineering :: Visualization',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'Topic :: Multimedia :: Graphics',
    'Framework :: Matplotlib',
]

with open('README.rst', 'r') as fp:
    readme = fp.read()
with open('CONTACT.txt', 'r') as fp:
    contacts = fp.read()
long_description = readme + '\n\n' + contacts

setup(name=NAME,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      maintainer=AUTHOR,
      maintainer_email=AUTHOR_EMAIL,
      description=DESCRIPTION,
      long_description=long_description,
      license=