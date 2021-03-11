from Interfaces import ConfigOPSInterface
from MainHandler import Handler
from runCalculations import RunCalculations
import Utils
import random
import os
import gi
gi.require_version('Gtk', '3.0')
# from gi.repository import Gtk
# from concurrent.futures import ThreadPoolExecutor


class OPSHandler(Handler):
    def __init__(self, builder, handler):
        super().__init__(builder)
        self.builder = builder
        self.handler = handler
        # self._thread = ThreadPoolExecutor()
        self.config_OPS_window = builder.get_object('config_OPS_window')
        self.config_OPS_window.connect(
            'delete-event', lambda w, e: w.hide() or True)
        self.ops_config: ConfigOPSInterface

    def on_OPS_cancel_button_clicked(self, _) -> None:
        """ Handle OPS cancel button """
        self.config_OPS_window.hide()

    def on_OPS_run_button_clicked(self, _) -> None:
        if self.handler.files_ok():
            self.ops_config = {
                'XMatrix': self.handler.get_X_matrix(),
                'yvector': self.handler.get_y_vector(),
                'output_matrix': self.builder.get_object('OPS_output_matrix').get_text(),
                'output_cv': self.builder.get_object('OPS_output_cv').get_text(),
                'output_models': self.builder.get_object('OPS_output_models').get_text(),
                'varcut': self.builder.get_object('ops_varcut').get_value(),
                'corrcut': self.builder.get_object('ops_corrcut').get_value(),
                'autoscale': self.builder.get_object('ops_autoscale').get_active(),
                'lj_transform': self.builder.get_object('ops_ljtransform').get_active(),
                'autocorrcut': self.builder.get_object('ops_autocorrcut').get_value(),
                'latent_vars_ops': self.builder.get_object('ops_latent_vars_OPS').get_value(),
                'latent_vars_model': self.builder.get_object('ops_latent_vars_model').get_value(),
                'ops_window': self.builder.get_object('ops_OPS_window').get_value(),
                'ops_increment': self.builder.get_object('ops_OPS_increment').get_value(),
                'vars_percentage': self.builder.get_object('ops_vars_percentage').get_value(),
                'models_to_save': self.builder.get_object('ops_models_to_save').get_value(),
                'yrand': self.builder.get_object('ops_yrand').get_value(),
                'lno': self.builder.get_object('ops_lno').get_value(),
                'ops_type': 'f' if self.builder.get_object('ops_feed_ops').get_active() else 's'
            }

            # TODO: use date instead of random numbers
            rand = random.randint(10000, 99999)
            if not self.ops_config['output_matrix']:
                self.ops_config['output_matrix'] = os.path.join(os.path.dirname(self.handler.get_X_matrix()),
                                                                "OPS_output_matrix_{}.csv".format(rand))
            if not self.ops_config['output_cv']:
                self.ops_config['output_cv'] = os.path.join(os.path.dirname(self.handler.get_X_matrix()),
                                                            "OPS_output_CV_{}.csv".format(rand))
            if not self.ops_config['output_models']:
                self.ops_config['output_models'] = os.path.join(os.path.dirname(self.handler.get_X_matrix()),
                                                                "OPS_output_models_{}.json".format(rand))

            # TODO: implement multithreading
            RunCalculations.runOPS(self.ops_config)
            # self._thread.submit(RunCalculations.runOPS, self.ops_config)

            # If everything is ok, current matrix will be the filtered one.
            if os.path.isfile(self.ops_config['output_matrix']):
                self.handler.set_X_matrix(self.ops_config['output_matrix'])
                self.draw_matrices('matrix')
        else:
            print("Please, go to File > Open... before run a calculation.")
