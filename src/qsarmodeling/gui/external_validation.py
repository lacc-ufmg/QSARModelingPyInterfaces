
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QDoubleSpinBox, QPushButton, QProgressBar, QLineEdit, QComboBox

class ExternalValidationConfigDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("External Validation")
        self.setGeometry(100, 100, 800, 500)
        
        layout = QVBoxLayout()
        
        # Adjustments
        self.var_model_spinbox = QSpinBox()
        self.var_model_spinbox.setRange(1, 99999)
        
        # Labels and SpinBoxes
        var_model_layout = QHBoxLayout()
        var_model_layout.addWidget(QLabel("Number of latent variables in the model"))
        var_model_layout.addWidget(self.var_model_spinbox)
        
        layout.addLayout(var_model_layout)
        
        # Test set selection
        self.test_set_entry = QLineEdit()
        self.test_set_entry.setPlaceholderText("1, 5, 12, 17, 22, 35, 42")
        
        test_set_layout = QHBoxLayout()
        test_set_layout.addWidget(QLabel("Test set"))
        test_set_layout.addWidget(self.test_set_entry)
        
        layout.addLayout(test_set_layout)
        
        # Type of test set selection
        self.type_combobox = QComboBox()
        self.type_combobox.addItems(["Manual Selection", "Kennard-Stone Selection"])
        
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Type of test set selection"))
        type_layout.addWidget(self.type_combobox)
        
        layout.addLayout(type_layout)
        
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
    dialog = ExternalValidationConfigDialog()
    dialog.exec()