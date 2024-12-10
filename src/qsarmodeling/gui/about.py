from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QApplication
from PySide6.QtCore import Qt


class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About QSARModelingPy Alpha")
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        # Program information
        program_label = QLabel(
            "QSARModelingPy Alpha\nVersion: 0.1\nAlpha test version of QSARModelingPy\n\nWebsite: https://doi.org/10.1590/S0100-40422013000400013"
        )
        program_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(program_label)

        # Close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication([])
    dialog = AboutDialog()
    dialog.exec()
