# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 16:33:13 2024

@author: Howel Larreur
"""

from setuptools import setup, find_packages

DESCRIPTION = 'FISP: a 1D Fast Ion Spectrum Propagator for cold targets. To be published.'

setup(name='fisp',
      version='0.1',
      author='Howel Larreur',
      author_email='hwlr33@gmail.com',
      description=DESCRIPTION,
      packages=find_packages(),
      install_requires=['matplotlib', 'numpy', 'scipy', 'tqdm'],
      keywords=['simulation', 'spectrum', 'ion', 'cold target', '1D'])
