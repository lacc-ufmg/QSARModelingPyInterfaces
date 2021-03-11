import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="QSARModeling",
    version="0.1.1",
    author="Martins, J. P. A; Reis Filho, H. M.",
    author_email="jpam@qui.ufmg.br,helitonmrf@ufmg.br",
    description="A software for building and validating QSAR models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hellmrf/QSARModelingPyInterfaces",
    packages=setuptools.find_packages(),
    install_requires=[
        'qsarmodelingpy',
        'pygobject==3.30.5'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
