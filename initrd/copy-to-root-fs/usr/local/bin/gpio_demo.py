#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2020 Brian Masney <masneyb@onstation.org>
#
# GTK+ demo application that shows toggling GPIO pins over USB.
#
# Install the required dependencies on Alpine Linux with:
#
#    apk add gtk+3.0 py3-gobject3 python3
#
# If you are running this on a phone and want to make the program larger, then run it with:
#
#     GDK_SCALE=6 ./gpio_demo.py

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gtk

DEMO_TIMER_MS = 750
MAX_GPIOS = 4

class GpioWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="GPIO Demo")
        self.set_border_width(10)

        vbox = Gtk.VBox(spacing=6)
        self.add(vbox)

        buttons = []
        for gpio in range(1, MAX_GPIOS + 1):
            button = Gtk.ToggleButton(label="GPIO %d" % (gpio))
            button.connect("toggled", self.gpio_button_toggled, gpio)
            vbox.pack_start(button, True, True, 0)
            buttons.append(button)

        check = Gtk.CheckButton(label="Demo")
        check.connect("toggled", self.demo_checkbox_toggled, buttons)
        vbox.pack_start(check, True, True, 0)

    def gpio_button_toggled(self, button, gpio):
        set_gpio_state(gpio, button.get_active())

    def demo_checkbox_toggled(self, checkbox, buttons):
        if checkbox.get_active():
            GLib.timeout_add(DEMO_TIMER_MS, self.timeout, (checkbox, buttons, 0))

    def timeout(self, data):
        (checkbox, buttons, active_gpio) = data
        if not checkbox.get_active():
            return

        for idx, button in enumerate(buttons):
            button.set_active(idx == active_gpio)

        active_gpio = (active_gpio + 1) % MAX_GPIOS
        GLib.timeout_add(DEMO_TIMER_MS, self.timeout, (checkbox, buttons, active_gpio))

def init_gpio():
    # Ensure that all of the GPIO pins are set to low on startup.
    for gpio in range(1, MAX_GPIOS + 1):
        set_gpio_state(gpio, 0)

def set_gpio_state(gpio_number, active):
    print('GPIO %s = %d' % (gpio_number, active))
    # FIXME - add hardware control code here

init_gpio()
WIN = GpioWindow()
WIN.connect("destroy", Gtk.main_quit)
WIN.show_all()
Gtk.main()
