# QSARModelingPy

QSARModelingPy is an open-source computational package to generate and validate QSAR models.

[![PyPI](https://img.shields.io/pypi/v/qsarmodelingpy-gui)](https://pypi.org/project/qsarmodelingpy-gui/)
[![Conda](https://img.shields.io/conda/v/helitonmrf/qsarmodelingpy-gui)](https://anaconda.org/helitonmrf/qsarmodelingpy-gui)
[![Conda - Platforms](https://img.shields.io/conda/pn/helitonmrf/qsarmodelingpy-gui)](https://anaconda.org/helitonmrf/qsarmodelingpy-gui)
![Conda - License: GPL-3.0](https://img.shields.io/conda/l/helitonmrf/qsarmodelingpy-gui)

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

> Some of these features are not yet fully implemented on all interfaces.

**What QSARModelingPy is yet to implement?**

-   Descriptors extraction using different methodologies
-   Graphical outputs
-   Faster calculations
-   Batch calculations for CLI

---

QSARModelingPy is divided into three different approaches: you can execute it headless (in command line), in a Jupyter Notebook, or a Graphical User Interface.

If you don't know exactly what you need, here are a rule of thumbs:

-   If you are a chemist, physicist, or engineer and just want to build and validate your models, you will probably prefer the GUI mode.
-   To run calculations remotely, in a cluster or if you just love the command line (♥), use the CLI version. Versioning control is also possible in CLI.
-   If you know Python and want to have more control over what the program is doing, you can use the Jupyter Notebook version.
-   If you are a programmer and want to develop a new application using QSARModelingPy's Core, take a look at the package `QSARModelingPyCore` available at [PyPI](https://pypi.org/project/qsarmodelingpy/).

## Installing

### Graphical User Interface (GUI)

#### Linux: Snap
Maybe the easiest way to install QSARModelingPy on Linux is through the Snap version (for distros with `snap` support). Just run:

```sh
sudo snap install qsarmodelingpy --channel=edge/stable
```

And then run the program with `qsarmodelingpy` on the terminal, or search for `QSARModelingPy` on your launcher.

#### Cross-Platform
The recommended way of installing the GUI is with [Miniconda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/) (or Anaconda, if you already have it). If you're using Windows, you may need to use the Anaconda Prompt where we say "terminal" below.

> Make sure the `conda` command is accessible in your shell. You may need to `conda init <shell>` if you're not using the default shell. For example, if you're using zsh on Linux or Powershell on Windows, you may need to `conda init zsh` or `conda init powershell`, respectively. On Windows, you can also use the Anaconda Prompt and skip this part.

When you have `conda`, install the GUI for QSARModelingPy:
```shell
$ conda install -c helitonmrf -c conda-forge qsarmodelingpy-gui
```
> Throughout this guide, you'll see command beginning with `$`. This just indicates a shell input, and thus should not be typed.

Then run the application:
```shell
$ qsarmodelingpy
```

#### Cross-platform: Without Miniconda
<!-- There are binaries available for Linux and Windows under "Assets" on the [Releases page](https://github.com/hellmrf/QSARModelingPyInterfaces/releases). Just download, decompress and execute `qsarmodeling` (Linux) or `qsarmodeling.exe` (Windows).

> Linux users may need to `chmod +x ./qsarmodeling` before executing. -->
If, for some reason, you don't want to use Miniconda (or Anaconda), you can use `pip`. However, be aware that some of the QSARModeling dependencies don't offer pre-built packages, what basically means that pip will need to build them. Practically, it means you'll need the building apparatus.

Advantages over Miniconda approach:
- You aren't stuck inside an environment, so `qsarmodelingpy` will be available system-wide.

Disadvantages over Miniconda approach:
- You may have to install some build dependencies.

First of all, you'll need [Python 3](https://www.python.org/downloads/) installed, as well as [pip](https://pip.pypa.io/en/stable/installation/).

Then install the application running in a terminal (or command prompt):
```shell
$ pip install qsarmodelingpy-gui
```

If you got some error saying `ERROR: Command errored out with exit status 1:`, look at the message just before. It'll say what to do. On Debian/Ubuntu, you'll need to install some dependencies:
```shell
$ sudo apt install libglib2.0-dev libgirepository1.0-dev libcairo2-dev
```

On Windows, you may need [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/).

After installing the dependencies, you'll need to run `pip install qsarmodelingpy-gui` again.

After you have success installing the pip package, you can run the application with:
```shell
$ qsarmodelingpy
```


### Other interfaces

If you want to use other interfaces or, for any reason, don't want the binaries, start installing [Anaconda](https://www.anaconda.com/products/individual) (or, if you don't need Jupyter Notebook, [Minicoda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/)). The use of `virtualenv` is possible in Linux but will lead to severe problems in Windows (missing icons, missing libraries, fatal erros, civil wars...). As it depends a lot on the system, we've decided to use the `conda` approach.

> Make sure the `conda` command is accessible in your shell. You may need to `conda init <shell>` if you're not using the default shell. For example, if you're using zsh on Linux or Powershell on Windows, you may need to `conda init zsh` or `conda init powershell`, respectively.

### Clone the repository

```bash
$ git clone git@github.com:hellmrf/QSARModelingPy.git

$ cd ./QSARModelingPy
```

If you don't have `git` installed, you can use the "Download ZIP" option on Github and extract it. Just make sure your terminal is within the `QSARModelingPy` (or `QSARModelingPy-master`) folder.

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

> Please, note that you _must_ activate your virtual environment each time your terminal has been restarted. You'll get a visual clue that it's active by looking for `(QSARModelingPy)` at the beginning of your shell line. If you don't see this even after `conda activate`, check the hint above about `conda init`ializing your shell.

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

### Using the Graphical User Interface (GUI)

The following is applicable only if you _downloaded_ the code and are running directly with Python. If you're using Snap or Binaries, this is not for you.

Now you have to enter the `GUI` directory and execute the program:

```bash
(QSARModelingPy) $ python ./GUI/main.py
```

You may notice the lack of some icons. It does not affect in any way the program, but to fix that, you will need to install Adwaita icons, which is normally done by `conda` when installing dependencies. For Ubuntu Linux, run:

```bash
$ sudo apt install adwaita-icon-theme-full
```

See [this](https://stackoverflow.com/questions/26738025/gtk-icon-missing-when-running-in-ms-windows) for Windows and [this](https://gitlab.gnome.org/GNOME/adwaita-icon-theme) if your distro's package manager does not have this theme. It's not mandatory, however.
