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

    def on_cv_run_button_clicked(self, _) -> None:
        if not self.X_matrix or not self.y_vector:
            return

        auto = self.builder.get_object("cv_autonLV").get_active()
        nLV = None if auto else self.builder.get_object("cross_validation_nLV").get_value()
        filename = self.builder.get_object("cv_output").get_text()

        RunCalculations.runCrossValidation(self.X_matrix, self.y_vector, filename, nLV)

    def on_yrlno_run_button_clicked(self, _) -> None:
        if not self.X_matrix or not self.y_vector:
            return

        RunCalculations.run_yrlno(
            X_path=self.X_matrix,
            y_path=self.y_vector,
            pop_path=self.builder.get_object("yrlno_input_pop").get_text(),
            Q2_path=self.builder.get_object("yrlno_input_q2").get_text(),
            output_vars=self.builder.get_object("yrlno_output_vars").get_text() or None,
            output_params=self.builder.get_object("yrlno_output_params").get_text() or None,
            yr_cut=self.builder.get_object("yrlno_yrand").get_value(),
            Q2_cut=self.builder.get_object("yrlno_lno").get_value(),
            lno_cut=self.builder.get_object("yrlno_q2_crit").get_value()
        )
