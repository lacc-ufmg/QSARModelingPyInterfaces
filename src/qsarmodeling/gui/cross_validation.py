
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QDoubleSpinBox, QPushButton, QProgressBar, QLineEdit

class CrossValidationConfigDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cross Validation")
        self.setGeometry(100, 100, 350, 200)
        
        layout = QVBoxLayout()
        
        # Adjustments
        self.nlv_spinbox = QSpinBox()
        self.nlv_spinbox.setRange(1, 9999999)
        
        # Labels and SpinBoxes
        nlv_layout = QHBoxLayout()
        nlv_layout.addWidget(QLabel("Number of latent variables"))
        nlv_layout.addWidget(self.nlv_spinbox)
        
        layout.addLayout(nlv_layout)
        
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
    dialog = CrossValidationConfigDialog()
    dialog.exec()