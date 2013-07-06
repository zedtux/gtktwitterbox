from gi.repository import Gtk
from gtktwitterbox.twitter import GtkTwitterBox

class MainWindow(Gtk.Window):

    def __init__(self):
      Gtk.Window.__init__(self, title="Hello World")
      GtkTwitterBox(self, "douaneapp", 15)
