import sys
from loguru import logger

# from qsarmodeling.gui.ValidationHandler import ValidationHandler
# from qsarmodeling.gui.FilterHandler import FilterHandler
# from qsarmodeling.gui.OPSHandler import OPSHandler
# from qsarmodeling.gui.GAHandler import GAHandler
# from qsarmodeling.gui.MainHandler import Handler
# from qsarmodeling.gui.HandlerFinder import HandlerFinder
# from qsarmodeling.gui.ResultsHandler import ResultsHandler
# from qsarmodeling.gui.Utils import cleanup_temporary_directory, __DIR__

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMenu,
    QMenuBar,
    QFileDialog,
    QLabel,
    QVBoxLayout,
    QWidget,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QSARModelingPy Alpha")
        self.setGeometry(100, 100, 700, 500)

        # Menu bar
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        # File menu
        file_menu = QMenu("File", self)
        menu_bar.addMenu(file_menu)

        open_action = QAction("Open...", self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

        # Welcome label
        welcome_label = QLabel(
            "Welcome to QSARModelingPy Alpha\n\nTo begin, go to File > Open... and open both matrix and vector.\n\nTo generate a model using either OPS or GA, go to Generate and choose the method.\n\nTo perform validation, filter or prediction, use the corresponding menu.",
            self,
        )
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(welcome_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def open_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        file_dialog.setNameFilters(["CSV files (*.csv)", "Text files (*.txt)"])
        if file_dialog.exec():
            file_paths = file_dialog.selectedFiles()
            # Handle file paths


def main():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    else:
        logger.warning(
            "QApplication instance already exists. Reusing the existing instance."
        )

    window = MainWindow()
    window.show()
    app.exec_()

    ## Cleanup temporary directory when the GUI is closed
    # cleanup_temporary_directory()


if __name__ == "__main__":
    main()
