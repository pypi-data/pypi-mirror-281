# -*- coding: utf-8 -*-
# Python-Template
# Project by https://github.com/rix1337

import setuptools

from rix_template.providers.version import get_version

try:
    with open('README.md', encoding='utf-8') as f:
        long_description = f.read()
except:
    import io

    long_description = io.open('README.md', encoding='utf-8').read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    name="rix_template",
    version=get_version(),
    author="rix1337",
    author_email="",
    description="Full template for python web projects with Docker, GitHub Actions, PyPI, and more.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rix1337/Python-Template",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=required,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'rix_template = rix_template.run:main',
        ],
    },
)
