#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2020 Brian Masney <masneyb@onstation.org>
#
# GTK+ demo application that shows toggling GPIO pins via a MCP2221 breakboard board over USB
# (https://www.adafruit.com/product/4471) to demonstrate how an older phone, such as the Nexus 5,
# can be used can be used to control external hardware for prototyping purposes.
#
# Install the required dependencies on Alpine Linux with:
#
#    apk add eudev-dev gtk+3.0 libusb-dev linux-headers py3-gobject3 python3 python3-dev
#    pip3 install hidapi adafruit-blinka
#
# To run:
#
#    BLINKA_MCP2221=1 GDK_SCALE=6 ./gpio_demo.py

import board
import digitalio
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gtk

DEMO_TIMER_MS = 500

MAX_GPIOS = 4
GPIO_PIN_RANGE = range(0, MAX_GPIOS)
GPIO_PIN_CONSTANTS = [board.G0, board.G1, board.G2, board.G3]
GPIO_PINS = []

class GpioWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="GPIO Demo")
        self.set_border_width(10)

        vbox = Gtk.VBox(spacing=6)
        self.add(vbox)

        buttons = []
        for pin in GPIO_PIN_RANGE:
            button = Gtk.ToggleButton(label="GPIO %d" % (pin))
            button.connect("toggled", self.gpio_button_toggled, pin)
            vbox.pack_start(button, True, True, 0)
            buttons.append(button)

        auto_checkbox = Gtk.CheckButton(label="Automatic")
        auto_checkbox.connect("toggled", self.auto_checkbox_toggled, buttons)
        vbox.pack_start(auto_checkbox, True, True, 0)

    def gpio_button_toggled(self, button, pin):
        set_gpio_state(pin, button.get_active())

    def auto_checkbox_toggled(self, checkbox, buttons):
        if checkbox.get_active():
            GLib.timeout_add(DEMO_TIMER_MS, self.timeout, (checkbox, buttons))

    def timeout(self, data):
        (checkbox, buttons) = data
        if not checkbox.get_active():
            return

        # When in automatic mode, shift the value of all the GPIO pins by one. If all of the pins
        # are off, then turn the first one on. If all pins are on, then turn the first pin off.

        num_active = 0
        button_states = [None] * MAX_GPIOS
        for idx, button in enumerate(buttons):
            num_active += button.get_active()
            button_states[(idx + 1) % MAX_GPIOS] = button.get_active()

        if num_active == 0:
            button_states[0] = True
        elif num_active == MAX_GPIOS:
            button_states[0] = False

        for idx, button in enumerate(buttons):
            button.set_active(button_states[idx])

        GLib.timeout_add(DEMO_TIMER_MS, self.timeout, (checkbox, buttons))

def init_gpio():
    # Ensure that all of the GPIO pins are set to low on startup.
    for pin in GPIO_PIN_RANGE:
        gpio = digitalio.DigitalInOut(GPIO_PIN_CONSTANTS[pin])
        gpio.direction = digitalio.Direction.OUTPUT
        GPIO_PINS.append(gpio)

        set_gpio_state(pin, False)

def set_gpio_state(pin, active):
    GPIO_PINS[pin].value = active

init_gpio()
WIN = GpioWindow()
WIN.connect("destroy", Gtk.main_quit)
WIN.show_all()
Gtk.main()
