import sys
import coloredlogs
import logging
from os import path
from ValidationHandler import ValidationHandler
from FilterHandler import FilterHandler
from OPSHandler import OPSHandler
from GAHandler import GAHandler
from MainHandler import Handler
from HandlerFinder import HandlerFinder
from ResultsHandler import ResultsHandler
from Utils import cleanup_temporary_directory, get_log_file
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from Constants import DEBUG_MODE


logging_level = logging.DEBUG if DEBUG_MODE else logging.INFO
if not DEBUG_MODE:
    # redirect stderr and stdout to a temporary file
    LOG_FILE = get_log_file()
    print(f"Initialized log in {LOG_FILE}")
    sys.stdout = open(LOG_FILE, 'a')
    sys.stderr = sys.stdout

coloredlogs.install(fmt="%(filename)s:%(lineno)s %(funcName)s() %(levelname)s  %(message)s", level=logging_level)
coloredlogs.DEFAULT_FIELD_STYLES = {'filename': {'color': 'blue'}, 'lineno': {'color': 'blue'}, 'funcName': {'color': 'magenta'}, 'levelname': {'bold': True, 'color': 'black'}}

__DIR__ = getattr(sys, '_MEIPASS', path.abspath(path.dirname(__file__)))


def add_all_from_file(files: list, builder: Gtk.Builder) -> None:
    for f in files:
        builder.add_from_file(path.abspath(
            path.join(__DIR__, "Views", f)))


builder: Gtk.Builder = Gtk.Builder()
add_all_from_file([
    "main.glade",
    "about.glade",
    "ga.glade",
    "ops.glade",
    "varcut.glade",
    "corrcut.glade",
    "autocorrcut.glade",
    "cross_validation.glade",
    "yrlno.glade",
    "external_validation.glade",
    "results.glade",
], builder)


handler = Handler(builder)

""" Register handlers """
handlers = [
    handler,
    GAHandler(builder, handler),
    OPSHandler(builder, handler),
    FilterHandler(builder, handler),
    ValidationHandler(builder, handler),
    ResultsHandler(builder, handler),
]


if __name__ == '__main__':
    builder.connect_signals(HandlerFinder(handlers))
    window = builder.get_object('main_window')
    window.show_all()
    Gtk.main()
    cleanup_temporary_directory()