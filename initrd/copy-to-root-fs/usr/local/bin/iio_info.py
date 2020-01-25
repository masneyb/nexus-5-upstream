#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2020 Brian Masney <masneyb@onstation.org>
#
# Reads some of the relevant IIO attributes that's found on the Nexus 5 phone. Example output:
#
#     lg-hammerhead:/# /usr/local/bin/iio_info.py 
#     apds9930 - /sys/bus/iio/devices/iio:device0
#             in_illuminance0_input = 76
#             in_proximity0_raw = 9
#     mpu6515 - /sys/bus/iio/devices/iio:device1
#             in_accel_x_raw = -10029
#             in_accel_y_raw = 4843
#             in_accel_z_raw = -11650
#             in_anglvel_x_raw = 34
#             in_anglvel_y_raw = -10
#             in_anglvel_z_raw = -29
#     ak8963 - /sys/bus/iio/devices/iio:device4
#             in_magn_x_raw = 162
#             in_magn_y_raw = -22
#             in_magn_z_raw = -508
#     bmp280 - /sys/bus/iio/devices/iio:device5
#             in_pressure_input = 95.915601562
#             in_temp_input = 26380

import os
import pathlib

IIO_DIR = "/sys/bus/iio/devices"
DEV_ATTRS = {
    'ak8963': ['in_magn_x_raw', 'in_magn_y_raw', 'in_magn_z_raw'],
    'apds9930': ['in_illuminance0_input', 'in_proximity0_raw'],
    'bmp280': ['in_pressure_input', 'in_temp_input'],
    'mpu6515': ['in_accel_x_raw', 'in_accel_y_raw', 'in_accel_z_raw',
                'in_anglvel_x_raw', 'in_anglvel_y_raw', 'in_anglvel_z_raw']
}

def get_iio_devices():
    devices = []

    iio_devices = os.listdir(IIO_DIR)
    iio_devices.sort()
    for iio_device in iio_devices:
        if not iio_device.startswith("iio:device"):
            continue

        name_path = pathlib.Path("%s/%s/name" % (IIO_DIR, iio_device))
        name = name_path.read_text().replace('\n', '')
        devices.append((name, iio_device))

    return devices

def show_device(iio_device):
    if iio_device[0] not in DEV_ATTRS:
        return

    print("%s - %s/%s" % (iio_device[0], IIO_DIR, iio_device[1]))
    for attr in DEV_ATTRS[iio_device[0]]:
        attr_path = pathlib.Path("%s/%s/%s" % (IIO_DIR, iio_device[1], attr))
        attr_val = attr_path.read_text().replace('\n', '')
        print("\t%s = %s" % (attr, attr_val))

for device in get_iio_devices():
    show_device(device)
