import logging
from ValidationHandler import ValidationHandler
from FilterHandler import FilterHandler
from OPSHandler import OPSHandler
from GAHandler import GAHandler
from MainHandler import Handler
from HandlerFinder import HandlerFinder
from gi.repository import Gtk
import gi

gi.require_version('Gtk', '3.0')


# Uncomment the following lines to see all console logs.
# logging.basicConfig(level=logging.DEBUG)


builder: Gtk.Builder = Gtk.Builder()
builder.add_from_file('./Views/main.glade')
builder.add_from_file('./Views/ga.glade')
builder.add_from_file('./Views/ops.glade')
builder.add_from_file('./Views/about.glade')
builder.add_from_file('./Views/varcut.glade')
builder.add_from_file('./Views/corrcut.glade')
builder.add_from_file('./Views/autocorrcut.glade')
builder.add_from_file('./Views/cross_validation.glade')
builder.add_from_file('./Views/yrlno.glade')

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
