import gi

gi.require_version('Gtk', '3.0')
import os
from gi.repository import Gtk
import pandas
import random

from runCalculations import RunCalculations


class OPSHandler:
    def __init__(self, builder):
        self.builder = builder

    def on_OPS_cancel_button_clicked(self, _):
        """ Handle OPS cancel button """
        self.config_OPS_window.hide()