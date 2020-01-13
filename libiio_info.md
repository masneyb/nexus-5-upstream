Here's the relevant output of the
[iio_info command](https://github.com/analogdevicesinc/libiio/blob/master/tests/iio_info.c)
from the [libiio](https://github.com/analogdevicesinc/libiio) project that shows what values
are available upstream from the various i2c sensors.

## tsl2772

    iio:device0: apds9930
      4 channels found:
        illuminance0:  (input)
        4 channel-specific attributes found:
          attr  0: calibrate ERROR: Permission denied (-13)
          attr  1: input value: 38
          attr  2: lux_table value: 52000,96824,38792,67132,0,0
          attr  3: target_input value: 150
        intensity0:  (input)
        6 channel-specific attributes found:
          attr  0: calibbias value: 1000
          attr  1: calibscale value: 1
          attr  2: calibscale_available value: 1 8 16 120
          attr  3: integration_time value: 0.002730
          attr  4: integration_time_available value: [0.002730 0.002730 0.699000]
          attr  5: raw value: 2
        proximity0:  (input)
        4 channel-specific attributes found:
          attr  0: calibrate ERROR: Permission denied (-13)
          attr  1: calibscale value: 1
          attr  2: calibscale_available value: 1 2 4 8
          attr  3: raw value: 10
        intensity1:  (input)
        1 channel-specific attributes found:
          attr  0: raw value: 0

## mpu6515

    iio:device1: mpu6515 (buffer capable)
      9 channels found:
        accel_x:  (input, index: 0, format: be:S16/16>>0)
        6 channel-specific attributes found:
          attr  0: calibbias value: -3854
          attr  1: matrix value: 0, 0, 0; 0, 0, 0; 0, 0, 0
          attr  2: mount_matrix value: 1, 0, 0; 0, 1, 0; 0, 0, 1
          attr  3: raw value: -858
          attr  4: scale value: 0.000598
          attr  5: scale_available value: 0.000598 0.001196 0.002392 0.004785
        accel_y:  (input, index: 1, format: be:S16/16>>0)
        6 channel-specific attributes found:
          attr  0: calibbias value: 17
          attr  1: matrix value: 0, 0, 0; 0, 0, 0; 0, 0, 0
          attr  2: mount_matrix value: 1, 0, 0; 0, 1, 0; 0, 0, 1
          attr  3: raw value: 452
          attr  4: scale value: 0.000598
          attr  5: scale_available value: 0.000598 0.001196 0.002392 0.004785
        accel_z:  (input, index: 2, format: be:S16/16>>0)
        6 channel-specific attributes found:
          attr  0: calibbias value: 10752
          attr  1: matrix value: 0, 0, 0; 0, 0, 0; 0, 0, 0
          attr  2: mount_matrix value: 1, 0, 0; 0, 1, 0; 0, 0, 1
          attr  3: raw value: -15791
          attr  4: scale value: 0.000598
          attr  5: scale_available value: 0.000598 0.001196 0.002392 0.004785
        anglvel_x:  (input, index: 3, format: be:S16/16>>0)
        5 channel-specific attributes found:
          attr  0: calibbias value: 0
          attr  1: mount_matrix value: 1, 0, 0; 0, 1, 0; 0, 0, 1
          attr  2: raw value: 45
          attr  3: scale value: 0.001064724
          attr  4: scale_available value: 0.000133090 0.000266181 0.000532362 0.001064724
        anglvel_y:  (input, index: 4, format: be:S16/16>>0)
        5 channel-specific attributes found:
          attr  0: calibbias value: 0
          attr  1: mount_matrix value: 1, 0, 0; 0, 1, 0; 0, 0, 1
          attr  2: raw value: -24
          attr  3: scale value: 0.001064724
          attr  4: scale_available value: 0.000133090 0.000266181 0.000532362 0.001064724
        anglvel_z:  (input, index: 5, format: be:S16/16>>0)
        5 channel-specific attributes found:
          attr  0: calibbias value: 0
          attr  1: mount_matrix value: 1, 0, 0; 0, 1, 0; 0, 0, 1
          attr  2: raw value: -13
          attr  3: scale value: 0.001064724
          attr  4: scale_available value: 0.000133090 0.000266181 0.000532362 0.001064724
        timestamp:  (input, index: 6, format: le:S64/64>>0)
        temp:  (input)
        3 channel-specific attributes found:
          attr  0: offset value: 7011
          attr  1: raw value: 4095
          attr  2: scale value: 2.995178
        gyro:  (input)
        1 channel-specific attributes found:
          attr  0: matrix value: 0, 0, 0; 0, 0, 0; 0, 0, 0
      3 device-specific attributes found:
          attr  0: current_timestamp_clock value: realtime
          attr  1: sampling_frequency value: 50
          attr  2: sampling_frequency_available value: 10 20 50 100 200 500
      2 buffer-specific attributes found:
          attr  0: data_available value: 0
          attr  1: watermark value: 1
      Current trigger: trigger0(mpu6515-dev1)

## pm8941-iadc

    iio:device2: fc4cf000.spmi:pm8941@0:iadc@3600
      2 channels found:
        current1:  (input)
        2 channel-specific attributes found:
          attr  0: raw value: 36
          attr  1: scale value: 0.001000
        current0:  (input)
        2 channel-specific attributes found:
          attr  0: raw value: 37
          attr  1: scale value: 0.001000

## ak8963

    iio:device3: ak8963 (buffer capable)
      5 channels found:
        magn_x:  (input, index: 0, format: le:S16/16>>0)
        2 channel-specific attributes found:
          attr  0: raw value: 89
          attr  1: scale value: 0.006773
        magn_y:  (input, index: 1, format: le:S16/16>>0)
        2 channel-specific attributes found:
          attr  0: raw value: -1
          attr  1: scale value: 0.006796
        magn_z:  (input, index: 2, format: le:S16/16>>0)
        2 channel-specific attributes found:
          attr  0: raw value: -492
          attr  1: scale value: 0.006609
        timestamp:  (input, index: 3, format: le:S64/64>>0)
        mount:  (input)
        1 channel-specific attributes found:
          attr  0: matrix value: 1, 0, 0; 0, 1, 0; 0, 0, 1
      1 device-specific attributes found:
          attr  0: current_timestamp_clock value: realtime
      2 buffer-specific attributes found:
          attr  0: data_available value: 0
          attr  1: watermark value: 1

## pm8941-vadc

    iio:device4: fc4cf000.spmi:pm8941@0:vadc@3100
      7 channels found:
        voltage6:  (input)
        1 channel-specific attributes found:
          attr  0: raw value: 39277
        voltage10:  (input)
        2 channel-specific attributes found:
          attr  0: input value: 1249902
          attr  1: raw value: 37545
        voltage14:  (input)
        2 channel-specific attributes found:
          attr  0: input value: 0
          attr  1: raw value: 24696
        voltage15:  (input)
        2 channel-specific attributes found:
          attr  0: input value: 1782317
          attr  1: raw value: 43008
        temp8:  (input)
        2 channel-specific attributes found:
          attr  0: input value: 33551
          attr  1: raw value: 31014
        voltage9:  (input)
        2 channel-specific attributes found:
          attr  0: input value: 624611
          attr  1: raw value: 31128
        voltage48:  (input)
        1 channel-specific attributes found:
          attr  0: raw value: 32148

## bmp280

    iio:device5: bmp280
      2 channels found:
        temp:  (input)
        3 channel-specific attributes found:
          attr  0: input value: 33590
          attr  1: oversampling_ratio value: 2
          attr  2: oversampling_ratio_available value: 1 2 4 8 16
        pressure:  (input)
        3 channel-specific attributes found:
          attr  0: input value: 96.978394531
          attr  1: oversampling_ratio value: 16
          attr  2: oversampling_ratio_available value: 1 2 4 8 16

[Back to main page](README.md)
