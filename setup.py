from setuptools import setup, find_packages

setup(
    name="einkify",
    version="1.0.0",
    description="foo",
    packages=find_packages(),
    install_requires=[
        "Pillow>=9.4.0",
        "PyYAML>=6.0",
        "rarfile>=4.0",
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: X11 Applications",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.10",
    ],
    entry_points={"console_scripts": ["einkify=einkify.__main__:main"]},
)
