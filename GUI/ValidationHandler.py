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
        self.builder.get_object('config_cv_window').connect('delete-event', lambda w, e: w.hide() or True)
        self.builder.get_object('config_yrlno_window').connect('delete-event', lambda w, e: w.hide() or True)
        self.X_matrix = self.handler.X_matrix
        self.y_vector = self.handler.y_vector

    def on_cv_run_button_clicked(self, _):
        if not self.X_matrix or not self.y_vector:
            return

        auto = self.builder.get_object("cv_autonLV").get_active()
        nLV = None if auto else self.builder.get_object("cross_validation_nLV").get_value()
        filename = self.builder.get_object("cv_output").get_text()

        RunCalculations.runCrossValidation(self.X_matrix, self.y_vector, filename, nLV)

    def on_yrlno_run_button_clicked(self, _):
        if not self.X_matrix or not self.y_vector:
            return

        # Running parameters:
        population_file = self.builder.get_object("yrlno_input_pop").get_text()
        q2_file = self.builder.get_object("yrlno_input_q2").get_text()
        output_vars = self.builder.get_object("yrlno_output_vars").get_text() or None
        output_params = self.builder.get_object("yrlno_output_params").get_text() or None

        yrand_criteria = self.builder.get_object("yrlno_yrand").get_value()
        lno_criteria = self.builder.get_object("yrlno_lno").get_value()

        RunCalculations.run_yrlno(
            self.X_matrix,
            self.y_vector,
            population_file,
            q2_file,
            yrand_criteria,
            lno_criteria
        )
