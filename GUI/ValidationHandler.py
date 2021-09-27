import logging
from Constants import DEBUG_MODE
from MainHandler import Handler
from qsarmodelingpy.Interfaces import ConfigExtValInterface
from runCalculations import RunCalculations
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
        self.builder.get_object('config_extval_window').connect(
            'delete-event', lambda w, e: w.hide() or True)
        # self.ext_val_config: ConfigExtValInterface

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
                "yrlno_output_vars").get_text(),
            output_params=self.builder.get_object(
                "yrlno_output_params").get_text(),
            yr_cut=self.builder.get_object("yrlno_yrand").get_value(),
            Q2_cut=self.builder.get_object("yrlno_lno").get_value(),
            lno_cut=self.builder.get_object("yrlno_q2").get_value()
        )

    def on_extval_run_button_clicked(self, _) -> None:
        if not self.handler.files_ok():
            logging.error("Please, open the files in File > Open...")
            raise FileNotFoundError("Please, open the files in File > Open...")

        # Choose defaults to output files
        X_name = os.path.splitext(
            os.path.basename(self.handler.get_X_matrix()))[0]
        basename = os.path.join(os.path.dirname(self.handler.get_X_matrix()),
                                f'{X_name}')
        default_outputs = {
            'output_extval':  f"{basename}_extval.csv",
            'output_cv':  f"{basename}_cv_extval.csv",
            'output_X_train':  f"{basename}_X_train_extval.csv",
            'output_y_train':  f"{basename}_y_train_extval.csv",
            'output_X_test':  f"{basename}_X_test_extval.csv",
            'output_y_test':  f"{basename}_y_test_extval.csv",
        }

        self.ext_val_config: ConfigExtValInterface = {
            'XMatrix': self.handler.get_X_matrix(),
            'yvector': self.handler.get_y_vector(),
            'test_set': self.builder.get_object('extval_test_set').get_text(),
            'latent_vars_model': self.builder.get_object('extval_vars_model').get_value() or None,
            'extval_type': self.builder.get_object('extval_type').get_active_id(),
            'output_extval': self.builder.get_object('extval_output_extval').get_text() or default_outputs["output_extval"],
            'output_cv': self.builder.get_object('extval_output_cv').get_text() or default_outputs["output_cv"],
            'output_X_train': self.builder.get_object('extval_output_X_train').get_text() or default_outputs["output_X_train"],
            'output_y_train': self.builder.get_object('extval_output_y_train').get_text() or default_outputs["output_y_train"],
            'output_X_test': self.builder.get_object('extval_output_X_test').get_text() or default_outputs["output_X_test"],
            'output_y_test': self.builder.get_object('extval_output_y_test').get_text() or default_outputs["output_y_test"],
            'autoscale': self.builder.get_object('extval_autoscale').get_active(),
            'lj_transform': self.builder.get_object('extval_ljtransform').get_active(),
        }

        RunCalculations.runExternalValidation(self.ext_val_config)
        logging.info("Done.")
