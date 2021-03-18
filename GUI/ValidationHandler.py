import logging
from MainHandler import Handler
from runCalculations import RunCalculations
import random
import pandas
import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class ValidationHandler(Handler):
    def __init__(self, builder, handler):
        super().__init__(builder)
        self.builder = builder
        self.handler = handler
        self.builder.get_object('config_cv_window').connect(
            'delete-event', lambda w, e: w.hide() or True)
        self.builder.get_object('config_yrlno_window').connect(
            'delete-event', lambda w, e: w.hide() or True)

    def on_cv_run_button_clicked(self, _) -> None:
        if not self.handler.get_X_matrix() or not self.handler.get_y_vector():
            logging.error("Load matrix/vector first.")
            return
        auto = self.builder.get_object("cv_autonLV").get_active()
        nLV = None if auto else self.builder.get_object(
            "cross_validation_nLV").get_value()
        filename = self.builder.get_object("cv_output").get_text()

        logging.debug("Calling RunCalculations.")
        RunCalculations.runCrossValidation(
            self.handler.get_X_matrix(), self.handler.get_y_vector(), filename, nLV)

    def on_yrlno_run_button_clicked(self, _) -> None:
        if not self.handler.get_X_matrix() or not self.handler.get_y_vector():
            logging.error("Please open matrix and vector first.")
            return

        RunCalculations.run_yrlno(
            X_path=self.handler.get_X_matrix(),
            y_path=self.handler.get_y_vector(),
            pop_path=self.builder.get_object("yrlno_input_pop").get_text(),
            Q2_path=self.builder.get_object("yrlno_input_q2").get_text(),
            output_vars=self.builder.get_object(
                "yrlno_output_vars").get_text() or None,
            output_params=self.builder.get_object(
                "yrlno_output_params").get_text() or None,
            yr_cut=self.builder.get_object("yrlno_yrand").get_value(),
            Q2_cut=self.builder.get_object("yrlno_lno").get_value(),
            lno_cut=self.builder.get_object("yrlno_q2").get_value()
        )
