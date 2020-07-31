# QSARModelingPy

QSAR Modeling is an open source computational package to generate and validate QSAR models.

## Using

QSARModelingPy is divided in three differents approaches: you can execute it headless (in command line), in a Jupyter Notebook or in a Graphical User Interface. It's also possible use QSARModeling as Python Package through [PyPI](https://pypi.org/project/qsarmodelingpy/).

Whatever method of your choice, start installing [Anaconda](https://www.anaconda.com/products/individual) (or [Minicoda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/)).

1. Make sure the `conda` command is accessible in your shell.

2. Clone the repository:

```sh
$ git clone git@github.com:hellmrf/QSARModelingPy.git

$ cd ./QSARModelingPy
```

3. Create a new environment using `environment.yml`:

```sh
$ conda env create -f environment.yml
```

4. Activate the new environment:

```sh
$ conda activate QSARModelingPy
```

> Please, note that you _must_ activate your virtual environment each time your terminal has been restarted. You'll get a visual clue that it's active by looking for `(QSARModelingPy)` at beginning of your shell line.

### Using in command line

You're ready. Enter the right directory and do what you need.

```sh
(QSARModelingPy) $ cd ./command_line
```

### Using in Jupyter Notebook

Enter `jupyter` directory and run jupyter notebook:

```sh
(QSARModelingPy) $ cd ./jupyter
(QSARModelingPy) $ jupyter notebook
```

Execute `QSARModelingNotebook.ipynb` and you're ready.

### Using with the Graphical User Interface (GUI)

First of all, you'll need to install adwaita icons. For linux, run:

```sh
(QSARModelingPy) $ sudo apt install adwaita-icon-theme-full
```

See [this](https://stackoverflow.com/questions/26738025/gtk-icon-missing-when-running-in-ms-windows) for Windows.

Enter `GUI` directory and run the following:.

```sh
(QSARModelingPy) $ cd ./GUI

(QSARModelingPy) $ python main.py
```
