import gi

gi.require_version('Gtk', '3.0')
import os
from gi.repository import Gtk
import pandas
import random

from runCalculations import RunCalculations
from MainHandler import Handler


class ValidationHandler(Handler):
    def __init__(self, builder, handler):
        self.builder = builder
        self.handler = handler
        self.config_cv_window = self.builder.get_object('config_cv_window')
        self.config_cv_window.connect('delete-event', lambda w, e: w.hide() or True)
        self.X_matrix = self.handler.X_matrix
        self.y_vector = self.handler.y_vector

    def on_cv_run_button_clicked(self, _):
        if not self.X_matrix or not self.y_vector:
            return

        auto = self.builder.get_object("cv_autonLV").get_active()
        nLV = None if auto else self.builder.get_object("cross_validation_nLV").get_value()
        filename = self.builder.get_object("cv_output").get_text()

        RunCalculations.runCrossValidation(self.X_matrix, self.y_vector, filename, nLV)
