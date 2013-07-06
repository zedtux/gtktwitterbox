#!/usr/bin/env python3
from gi.repository import Gtk, GLib, Gdk
from gtktwitterbox.twitter import GtkTwitterBox

class MyWindow(Gtk.Window):

    def __init__(self):
      Gtk.Window.__init__(self, title="Hello World")
      box = Gtk.Box()
      self.add(box)
      GtkTwitterBox(box, "douaneapp", 15)

win = MyWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()

GLib.threads_init()
Gdk.threads_init()
Gdk.threads_enter()
Gtk.main()
Gdk.threads_leave()
