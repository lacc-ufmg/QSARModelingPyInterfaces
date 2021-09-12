import os
import tempfile
import shutil
import subprocess
import time
import platform
TMP_DIRECTORY = None
LOG_FILE = None


def __initialize_temporary_file() -> str:
    global LOG_FILE
    LOG_FILE = os.path.join(get_tmp(), "qsarmodeling.log")
    open(LOG_FILE, "w").close()
    return LOG_FILE


def get_log_file() -> str:
    if LOG_FILE is None:
        return __initialize_temporary_file()
    else:
        return LOG_FILE


def get_tmp() -> str:
    global TMP_DIRECTORY
    if TMP_DIRECTORY is None:
        TMP_DIRECTORY = tempfile.mkdtemp()
    return TMP_DIRECTORY


def cleanup_temporary_directory() -> None:
    global TMP_DIRECTORY
    if TMP_DIRECTORY is not None:
        shutil.rmtree(TMP_DIRECTORY)
        TMP_DIRECTORY = None


def open_external(filepath: str) -> None:
    """Open an external file with the default software.
    Args:
        filepath (str): The file path to open
    """
    if platform.system() == 'Darwin':       # macOS
        subprocess.call(('open', filepath))
    elif platform.system() == 'Windows':    # Windows
        os.startfile(filepath)
    else:                                   # linux variants
        subprocess.call(('xdg-open', filepath))

# GUI Handlers

def set_output_matrix_as_input(self, config) -> None:
    """Sets the output matrix as input in the GUI.

    It's particularly useful at the end of a calculation, when you want that the result is shown in the GUI.
    """
    if os.path.isfile(config['output_matrix']):
        self.handler.set_X_matrix(config['output_matrix'])
        self.draw_matrices('matrix')
    if self.running_process is not None:
        self.running_process.terminate()
    self.running_process = None
