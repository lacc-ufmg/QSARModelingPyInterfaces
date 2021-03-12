from gi.repository import Gtk
from Interfaces import ConfigGAInterface
from MainHandler import Handler
from runCalculations import RunCalculations
import random
import os
import gi

gi.require_version('Gtk', '3.0')


class GAHandler(Handler):
    def __init__(self, builder, handler):
        super().__init__(builder)
        self.builder = builder
        self.handler = handler
        self.config_GA_window = self.builder.get_object('config_GA_window')
        self.config_GA_window.connect(
            'delete-event', lambda w, e: w.hide() or True)
        self.ga_config: ConfigGAInterface

    def on_GA_cancel_button_clicked(self, _) -> None:
        """ Handle OPS cancel button """
        self.config_GA_window.hide()

    def on_GA_run_button_clicked(self, _) -> None:
        if self.handler.files_ok():
            self.ga_config = {
                'XMatrix': self.handler.get_X_matrix(),
                'yvector': self.handler.get_y_vector(),
                'output_matrix': self.builder.get_object('GA_output_matrix').get_text(),
                'output_cv': self.builder.get_object('GA_output_cv').get_text(),
                'output_q2': self.builder.get_object('GA_output_q2').get_text(),
                'output_selected': self.builder.get_object('GA_output_selected_variables').get_text(),
                'varcut': self.builder.get_object('ga_varcut').get_value(),
                'corrcut': self.builder.get_object('ga_corrcut').get_value(),
                'autoscale': self.builder.get_object('ga_autoscale').get_active(),
                'lj_transform': self.builder.get_object('ga_ljtransform').get_active(),
                'autocorrcut': self.builder.get_object('ga_autocorrcut').get_value(),
                'max_latent_model': self.builder.get_object('ga_max_latent_model').get_value(),
                'min_vars_model': self.builder.get_object('ga_min_vars_model').get_value(),
                'max_vars_model': self.builder.get_object('ga_max_vars_model').get_value(),
                'population_size': self.builder.get_object('ga_population_size').get_value(),
                'migration_rate': self.builder.get_object('ga_migration_rate').get_value(),
                'crossover_rate': self.builder.get_object('ga_crossover_rate').get_value(),
                'mutation_rate': self.builder.get_object('ga_mutation_rate').get_value(),
                'generations': self.builder.get_object('ga_generations').get_value(),
                'yrand': self.builder.get_object('ga_yrand').get_value(),
                'lno': self.builder.get_object('ga_lno').get_value()
            }

            rand = random.randint(10000, 99999)
            if not self.ga_config['output_matrix']:
                self.ga_config['output_matrix'] = os.path.join(os.path.dirname(self.handler.get_X_matrix()),
                                                               "GA_output_matrix_{}.csv".format(rand))
            if not self.ga_config['output_cv']:
                self.ga_config['output_cv'] = os.path.join(os.path.dirname(self.handler.get_X_matrix()),
                                                           "GA_output_CV_{}.csv".format(rand))
            if not self.ga_config['output_q2']:
                self.ga_config['output_q2'] = os.path.join(os.path.dirname(self.handler.get_X_matrix()),
                                                           "GA_output_Q2_{}.csv".format(rand))
            if not self.ga_config['output_selected']:
                self.ga_config['output_selected'] = os.path.join(os.path.dirname(self.handler.get_X_matrix()),
                                                                 "GA_output_selected_{}.csv".format(rand))

            RunCalculations.runGA(self.ga_config)

            # If everything is ok, current matrix will be the filtered one.
            if os.path.isfile(self.ga_config['output_matrix']):
                self.handler.set_X_matrix(self.ga_config['output_matrix'])
                self.draw_matrices('matrix')
        else:
            print("Please, open the files in File > Open...")
