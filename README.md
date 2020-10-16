# QSARModelingPy

QSARModelingPy is an open source computational package to generate and validate QSAR models.

**What you _can_ do with QSARModelingPy**

-   Select variables through either OPS or Genetic Algorithm
-   Dimensionality reduction:
    -   Correlation cut
    -   Variance cut
    -   Autocorrelation cut
-   Validate your models:
    -   Cross Validation
    -   y-randomization / Leave-N-out
    -   External Validation
-   Make predictions for an external set

> Some of these features are not yet fully implemented on all interfaces, being available only from command line or Jupyter.

**What QSARModelingPy is yet to implement?**

-   Descriptors extraction using different methodologies
-   Graphical outputs
-   Faster calculations
-   Batch calculations for CLI

---

QSARModelingPy is divided in three different approaches: you can execute it headless (in command line), in a Jupyter Notebook or in a Graphical User Interface.

If you don't know exactly what you want, here are a rule of thumbs:

-   If you are a chemist or physicist and just want to build and validate your models, probably you will prefer the GUI mode.
-   To run calculations remotely, in a cluster or if you just love the command line (♥), use the CLI version.
-   If you know Python and want to have more control over what the program is doing, you can use the Jupyter Notebook version.
-   If you are a programmer and want to develop a new application using QSARModelingPy's Core, take a look at the package `QSARModelingPyCore` available at [PyPI](https://pypi.org/project/qsarmodelingpy/).

## Installing

Whatever method of your choice, start installing [Anaconda](https://www.anaconda.com/products/individual) (or, if you don't need Jupyter Notebook, [Minicoda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/)). The use of `virtualenv` can be possible, but we've realized that is depends a lot of the system, so we've decided to use the `conda` approach.

> Make sure the `conda` command is accessible in your shell.

### Clone the repository

```bash
$ git clone git@github.com:hellmrf/QSARModelingPy.git

$ cd ./QSARModelingPy
```

If you don't have `git` installed, you can use the "Download ZIP" option on Github and extract it. Just make sure your terminal are within the `QSARModelingPy` (or `QSARModelingPy-master`) folder.

### Creating a new virtual environment

Now you can create a new environment using `environment.yml`. To do this, make sure you're inside the `QSARModelingPy` folder and run the following from a terminal (or prompt).

```bash
$ conda env create -f environment.yml
```

This will create a new environment called `QSARModelingPy` and install all needed dependencies.

### Activate the new environment

Just run:

```bash
$ conda activate QSARModelingPy
```

> Please, note that you _must_ activate your virtual environment each time your terminal has been restarted. You'll get a visual clue that it's active by looking for `(QSARModelingPy)` at beginning of your shell line.

## Using

### Using in command line

You're ready. Enter the right directory and do what you need.

```bash
(QSARModelingPy) $ cd ./command_line
```

### Using in Jupyter Notebook

Enter `jupyter` directory and run jupyter notebook:

```bash
(QSARModelingPy) $ cd ./jupyter
(QSARModelingPy) $ jupyter notebook
```

Execute `QSARModelingNotebook.ipynb` and you're ready.

### Using with the Graphical User Interface (GUI)

Now you have to enter the `GUI` directory and execute the program:

```bash
(QSARModelingPy) $ cd ./GUI

(QSARModelingPy) $ python main.py
```

You may notice the lack of some icons. It does not affect in any way the program, but to fix this you need to install adwaita icons. For Ubuntu Linux, run:

```bash
(QSARModelingPy) $ sudo apt install adwaita-icon-theme-full
```

See [this](https://stackoverflow.com/questions/26738025/gtk-icon-missing-when-running-in-ms-windows) for Windows and [this](https://gitlab.gnome.org/GNOME/adwaita-icon-theme) if your distro's package manager does not have this theme. It's not mandatory, however.
