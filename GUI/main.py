import logging
from ValidationHandler import ValidationHandler
from FilterHandler import FilterHandler
from OPSHandler import OPSHandler
from GAHandler import GAHandler
from MainHandler import Handler
from HandlerFinder import HandlerFinder
from gi.repository import Gtk
import gi
from os import path

gi.require_version('Gtk', '3.0')


# Uncomment the following lines to see all console logs.
# logging.basicConfig(level=logging.DEBUG)

def add_all_from_file(files: list, builder: Gtk.Builder) -> None:
    for f in files:
        builder.add_from_file(path.join(path.dirname(__file__), "Views", f))


builder: Gtk.Builder = Gtk.Builder()
add_all_from_file(["main.glade", "ga.glade", "ops.glade", "about.glade", "varcut.glade",
                   "corrcut.glade", "autocorrcut.glade", "cross_validation.glade", "yrlno.glade"], builder)


handler = Handler(builder)

""" Register handlers """
handlers = [
    Handler(builder),
    GAHandler(builder, handler),
    OPSHandler(builder, handler),
    FilterHandler(builder, handler),
    ValidationHandler(builder, handler),
]


if __name__ == '__main__':
    builder.connect_signals(HandlerFinder(handlers))
    window = builder.get_object('main_window')
    window.show_all()
    Gtk.main()
