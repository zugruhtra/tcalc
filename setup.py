import setuptools

from tcalc import (
        __description__,
        __version__,
        __author__,
        __author_email__
        )

entry_points = {
        'console_scripts': [
            'tcalc=tcalc.cli:main'
            ]
        }


with open("README.rst", "r") as fp:
    long_description = fp.read()


setuptools.setup(
        name="tcalc",
        version=__version__,
        author=__author__,
        author_email=__author_email__,
        description=__description__,
        entry_points=entry_points,
        long_description=long_description,
        long_description_content_type="text/x-rst",
        url="https://github.com/zugruhtra/tcalc",
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
            ],
        )

