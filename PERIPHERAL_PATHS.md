# Device Paths

- backlight: /sys/devices/platform/soc/f9967000.i2c/i2c-2/2-0038/backlight/lcd-backlight
- touchscreen: /sys/devices/rmi4-00/input
- [gyroscope / accelerometer](libiio_info.md#mpu6515): /sys/devices/platform/soc/f9968000.i2c/i2c-2/2-0068
- [magnetometer](libiio_info.md#ak8963): /sys/devices/platform/soc/f9968000.i2c/i2c-2/i2c-3/3-000f.
- [temperature / humidity / barometer](libiio_info.md#bmp280): /sys/devices/platform/soc/f9968000.i2c/i2c-2/i2c-3/3-0076.
- [proximity / ambient light sensor (ALS)](libiio_info.md#tsl2772): /sys/devices/platform/soc/f9925000.i2c/i2c-1/1-0039.
- vibrator: /dev/input/by-path/platform-vibrator-event
- USB: usb0
- WiFi: wlan0
- charger: /sys/devices/platform/soc/f9923000.i2c/i2c-0/0-006b/power_supply/bq24190-charger
- serial port: /dev/ttyMSM0.

See the [iio_info.py script](initrd/copy-to-root-fs/usr/local/bin/iio_info.py) for an example
reading some of the IIO sensors.
[This commit](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=bce075d0ec4b6155cf4f52a7e56aa2dd3b668679)
describes how to setup an interrupt for proximity detection.

[Back to main page](README.md)
