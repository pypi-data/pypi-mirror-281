#python setup.py sdist bdist_wheel
#twine upload --skip-existing dist/*
#twine upload --skip-existing --repository testpypi dist/*

from setuptools import setup, find_packages

with open('README.md', mode='r') as file:
    description = file.read()

setup(
    name = 'imperial_materials_simulation',
    version = '0.0.1',
    description = 'Molecular simulation tool made for the undergraduate materials science and engineering theory and simulation module at Imperial College London',
    author = 'Ayham Al-Saffar',
    url = 'https://github.com/AyhamSaffar/imperial_materials_simulation',
    packages = find_packages(),
    python_requires = '~=3.10',
    install_requires = [
        'ipykernel',
        'ipympl',
        'ipywidgets',
        'matplotlib',
        'numba>=0.60.0',
        'numpy',
        'pandas',
        'py3dmol',
        'scipy',
    ],
    long_description = description,
    long_description_content_type = 'text/markdown',
    )