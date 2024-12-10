from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QDoubleSpinBox,
    QPushButton,
    QLineEdit,
    QCheckBox,
)


class CorrelationCutConfigDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Correlation cut")
        self.setGeometry(100, 100, 350, 200)

        layout = QVBoxLayout()

        # Adjustments
        self.corrcut_spinbox = QDoubleSpinBox()
        self.corrcut_spinbox.setRange(0.1, 1.0)
        self.corrcut_spinbox.setValue(0.3)

        # Labels and SpinBoxes
        corrcut_layout = QHBoxLayout()
        corrcut_layout.addWidget(QLabel("Correlation cut"))
        corrcut_layout.addWidget(self.corrcut_spinbox)

        layout.addLayout(corrcut_layout)

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
    dialog = CorrelationCutConfigDialog()
    dialog.exec()
