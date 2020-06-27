# Nexus 5 UART Cable

A serial console can be obtained from the phone through the headphone jack and requires building
a custom cable that converts between the different voltage levels found on the PC and the
phone.

![Nexus 5 UART Cable](images/Nexus5-UART-Cable.jpg?raw=1)

## Parts list

- [USB to TTL Serial Cable](https://www.sparkfun.com/products/12977)
- [SparkFun Solder-able Breadboard - Mini](https://www.sparkfun.com/products/12702)
- [SparkFun TRRS 3.5mm Jack Breakout](https://www.sparkfun.com/products/11570)
- [Audio Cable TRRS - 1ft](https://www.sparkfun.com/products/14163)
- 3 x 1K resistors to make a
  [voltage divider](https://learn.sparkfun.com/tutorials/voltage-dividers/all) to convert the
  3.3V TX output from the USB serial cable to 1.8V for the RX pin on the phone.
- [3.3V 250mA Linear Voltage Regulator - L4931-3.3 TO-92](https://www.adafruit.com/product/2166) to
  convert the 5-5.2V from the PC to a fixed 3.3V.
- 2 x 10 uF capacitors for the input and output on the voltage regulator.

## Pin mapping and voltages

USB        |                   | Headphone
-----------|-------------------|------------------
RX         |                   | TIP (TX 1.8V)
TX (3.3V)  | Voltage Divider   | Ring 1 (RX 1.8V)
GND        |                   | Ring 2
5V         | Voltage Regulator | Sleeve (3.3V)

Version 1 of my cable used a voltage divider for the 3.3V on the sleeve of the headphone jack, however
I moved to the 3.3V voltage regulator because the USB-C on my laptop puts out 5.2V, and the USB-A
puts out 5.0V. The phone expects close to 3.3V on the sleeve pin in order to enable the serial console
on startup and this slight voltage difference was enough to cause the serial console to not work.

## Booting the phone

With the phone off, plug the cable in, and start the phone with the volume-down and power buttons
pressed simultaneously to boot into the phone's bootloader. The following messages will come through
over the serial cable:

    welcome to hammerhead bootloader
    [10] Power on reason 10
    [10] DDR: elpida
    [110] Loaded IMGDATA at 0x11000000
    [110] Display Init: Start
    [190] MDP GDSC already enabled
    [190] bpp 24
    [230] Config MIPI_CMD_PANEL.
    [230] display panel: ORISE
    [230] display panel: Default setting
    [360] Turn on MIPI_CMD_PANEL.
    [410] Display Init: Done
    [410] cable type from shared memory: 8
    [410] vibe
    [610] USB init ept @ 0xf96b000
    [630] secured device: 1
    [630] fastboot_init()
    [680] splash: fastboot_op
     FASTBOOT MODE
     PRODUCT_NAME - hammerhead
     VARIANT - hammerhead D820(E) 16GB
     HW VERSION - rev_11
     BOOTLOADER VERSION - HHZ20h
     BASEBAND VERSION - M8974A-2.0.50.2.29
     CARRIER INFO - None
     SERIAL NUMBER - XXX
     SIGNING - production
     SECURE BOOT - enabled
     LOCK STATE - unlocked
    [790] splash: start
    [1820] Fastboot mode started
    [1820] udc_start()
    [2190] -- reset --
    [2190] -- portchange --
    [2270] -- reset --
    [2270] -- portchange --
    [2360] fastboot: processing commands

You can use the minicom package to access the serial console. Here's my ~/.minirc.dfl file:

    pu port             /dev/ttyUSB0
    pu rtscts           No

[Back to main page](README.md)
