from setuptools import setup, find_packages
setup(
name='HVImpactScore',
version='1.0.0',
author='Stephen Marinsek',
author_email='smarins1@jhu.edu',
description='Similarity scoring method for hypervelocity impact simulations using smoothed particle hydrodynamics.',
packages=find_packages(),
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',
],
python_requires='>=3.6',
)