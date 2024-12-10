from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QSpinBox,
    QDoubleSpinBox,
    QPushButton,
    QProgressBar,
    QLineEdit,
    QCheckBox,
    QApplication,
)


class AutocorrelationCutConfigDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Autocorrelation cut")
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        # Adjustments
        self.autocorrcut_spinbox = QDoubleSpinBox()
        self.autocorrcut_spinbox.setRange(0.1, 1.0)
        self.autocorrcut_spinbox.setValue(0.9)

        # Labels and SpinBoxes
        autocorrcut_layout = QHBoxLayout()
        autocorrcut_layout.addWidget(QLabel("Autocorrelation cut"))
        autocorrcut_layout.addWidget(self.autocorrcut_spinbox)

        layout.addLayout(autocorrcut_layout)

        # Save checkbox
        self.save_checkbox = QCheckBox("Save")
        layout.addWidget(self.save_checkbox)

        # Output file
        self.output_entry = QLineEdit()
        self.output_entry.setPlaceholderText("(absolute path)")

        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("Save as:"))
        output_layout.addWidget(self.output_entry)

        layout.addLayout(output_layout)

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
    dialog = AutocorrelationCutConfigDialog()
    dialog.exec()
