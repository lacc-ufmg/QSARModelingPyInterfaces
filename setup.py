import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="qsarmodelingpy-gui",
    version="0.2.2",
    author="Reis Filho, H. M.; Martins, J. P. A",
    author_email="helitonmrf@ufmg.br,jpam@qui.ufmg.br",
    description="A software for building and validating QSAR models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hellmrf/QSARModelingPyInterfaces",
    packages=["qsarmodelingpy-gui"],
    package_dir={"qsarmodelingpy-gui": "GUI"},
    package_data={"qsarmodelingpy-gui": ["Views/*.glade"]},
    install_requires=[
        'qsarmodelingpy',
        'pygobject==3.30.5',
        'typing_extensions',
        'coloredlogs',
        'matplotlib',
        'tornado',
        'PyQt5',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'qsarmodelingpy = qsarmodelingpy_gui.main:main',
        ],
    },
    python_requires='>=3.6',
)
