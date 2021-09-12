import numpy as np
import logging
from Constants import DEBUG_MODE
from MainHandler import Handler
# from qsarmodelingpy.Interfaces import ConfigExtValInterface
# from runCalculations import RunCalculations
# import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import matplotlib.pyplot as plt # TODO: add do dependecies


class ResultsHandler(Handler):
    def __init__(self, builder, handler):
        super().__init__(builder)
        self.builder = builder
        self.handler = handler
        self.window = self.builder.get_object('results_window')
        self.window.connect(
            'delete-event', lambda w, e: w.hide() or True)
        self.window.show_all()

        # self.ext_val_config: ConfigExtValInterface

    def on_plot(self, _) -> None:
        x = np.random.rand(5)
        y = np.random.rand(5)
        plt.plot(x, y)
        plt.show()
        logging.info("yuhuu")
