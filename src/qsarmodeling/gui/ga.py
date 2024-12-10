from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QSpinBox,
    QDoubleSpinBox,
    QPushButton,
    QProgressBar,
)


class GAConfigDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Generate model using Genetic Algorithm")
        self.setGeometry(100, 100, 600, 500)

        layout = QVBoxLayout()

        # Adjustments
        self.varcut_spinbox = QDoubleSpinBox()
        self.varcut_spinbox.setRange(0.01, 1.0)
        self.varcut_spinbox.setValue(0.1)

        self.corrcut_spinbox = QDoubleSpinBox()
        self.corrcut_spinbox.setRange(0.01, 1.0)
        self.corrcut_spinbox.setValue(0.3)

        # Labels and SpinBoxes
        varcut_layout = QHBoxLayout()
        varcut_layout.addWidget(QLabel("Variance Cut"))
        varcut_layout.addWidget(self.varcut_spinbox)

        corrcut_layout = QHBoxLayout()
        corrcut_layout.addWidget(QLabel("Correlation Cut"))
        corrcut_layout.addWidget(self.corrcut_spinbox)

        layout.addLayout(varcut_layout)
        layout.addLayout(corrcut_layout)

        # Progress bar
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        # Buttons
        button_layout = QHBoxLayout()
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        self.run_button = QPushButton("Run")
        self.run_button.clicked.connect(self.accept)

        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.run_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication([])
    dialog = GAConfigDialog()
    dialog.exec()
