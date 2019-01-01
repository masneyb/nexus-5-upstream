This page describes the current development efforts to port the the
[upstream Linux Kernel](https://www.kernel.org/) to the
[LG Nexus 5 (hammerhead) phone](https://en.wikipedia.org/wiki/Nexus_5). The factory
kernel image is based on the upstream Linux 3.4 kernel that was released in May 2012, and adds
almost 2 million lines of code on top of the upstream kernel. This factory image is abandoned
and no longer receives security updates.

The goal is to eventually get all of the major components working upstream, including the necessary
[device tree bindings](https://elinux.org/images/f/f9/Petazzoni-device-tree-dummies_0.pdf),
so that the phone will work with the latest upstream kernel. These patches will eventually appear
in the [Android kernels](https://android.googlesource.com/kernel/common/) as they rebase their
kernels onto newer upstream LTS kernel releases.

## Device summary

This is a high-level summary of the components that currently work upstream, or where there are
outstanding patches waiting for a review. See below for further details.

- gyroscope / accelerometer: `/sys/bus/iio/devices/iio:device2`
- magnetometer: `/sys/bus/iio/devices/iio:device3`
- temperature / pressure: `/sys/bus/iio/devices/iio:device4`
- proximity / ambient light sensor (ALS): `/sys/bus/iio/devices/iio:device5`
- vibrator: `/dev/input/event2`
- USB: `usb0`
- WiFi: `wlan0`
- charger
- serial port: `/dev/ttyMSM0`. A serial console can be obtained through the headphone jack and
  requires building a custom cable [as described on this page](UART_CABLE.md).

## Outstanding patches

- gpio / pinctrl / spmi

  - [pinctrl: qcom: spmi-gpio: fix gpio-hog related boot issues](https://lore.kernel.org/lkml/20181101001149.13453-6-masneyb@onstation.org/) - Accepted for 4.21
  - [ARM: dts: qcom: msm8974: add gpio-ranges](https://lore.kernel.org/lkml/20181101001149.13453-7-masneyb@onstation.org/)
  - [spmi: pmic-arb: convert to v2 irq interfaces to support hierarchical IRQ chips](https://lore.kernel.org/lkml/20181229114755.8711-2-masneyb@onstation.org/)
  - [qcom: spmi-gpio: add support for hierarchical IRQ chip](https://lore.kernel.org/lkml/20181229114755.8711-3-masneyb@onstation.org/)
  - [ARM: dts: qcom: msm8974: add interrupt properties](https://lore.kernel.org/lkml/20181229114755.8711-4-masneyb@onstation.org/)

- Vibrator

  - [dt-bindings: Input: new bindings for MSM vibrator](https://lore.kernel.org/lkml/20181025012937.2154-2-masneyb@onstation.org/)
  - [Input: add new vibrator driver for various MSM SOCs](https://lore.kernel.org/lkml/20181025012937.2154-3-masneyb@onstation.org/)
  - [ARM: dts: qcom: msm8974-hammerhead: add device tree bindings for vibrator](https://lore.kernel.org/lkml/20181025012937.2154-4-masneyb@onstation.org/)

- USB - Requires the charger and gpio hogging patches listed on this page.

  - [ARM: dts: qcom: msm8974-hammerhead: add USB OTG support](https://lore.kernel.org/lkml/20181101001149.13453-8-masneyb@onstation.org/)

- WiFi - This phone has a [Broadcom (now Cypress) 4339](http://www.cypress.com/file/298016/download)
  for wireless.

  - [ARM: dts: qcom: msm8974-hammerhead: add WiFi support](https://lore.kernel.org/lkml/20181104215034.3677-1-masneyb@onstation.org/)

- Panel

  - [dt-bindings: drm/panel: simple: add lg,acx467akm-7 panel](https://lore.kernel.org/lkml/20181124200628.24393-1-masneyb@onstation.org/)
  - [drm/panel: simple: add lg,acx467akm-7 panel](https://lore.kernel.org/lkml/20181124200628.24393-2-masneyb@onstation.org/)

## Patches accepted in upstream kernel

- The phone contains an [Avago APDS 9930](https://docs.broadcom.com/docs/AV02-3190EN)
  proximity / ambient light sensor (ALS), which is register compatible with the
  [TAOS TSL2772 sensor](https://ams.com/eng/content/download/291503/1066377/file/TSL2772_DS000181_2-00.pdf).
  The [tsl2772.c driver](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/drivers/iio/light/tsl2772.c)
  is one of the staging cleanups that I did and it took ~70 patches to move the driver out of
  staging and into mainline. A few notable patches from that work:

  - [498efcd08114 ("staging: iio: tsl2x7x: correct integration time and lux equation")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=498efcd08114905074a644bf81f82ce5c62eac43)
  - [9861d2daaf28 ("staging: iio: tsl2x7x: correct IIO_EV_INFO_PERIOD values"](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=9861d2daaf28e7beaa0c655206c595094d47ccd8)
  - [2ab5b7245367 ("staging: iio: tsl2x7x: make proximity sensor function correctly")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=2ab5b72453672ea18a176925becc40888df435ce)
  - [19422bde046a ("staging: iio: tsl2x7x: use auto increment I2C protocol")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=19422bde046a7fa549565300d0a4c4dc1e8d585a)
  - [9e4701eaef02 ("staging: iio: tsl2x7x: correct interrupt handler trigger")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=9e4701eaef02e1192faca2d0b3529249522f6253)
  - [77b69a0e679b ("staging: iio: tsl2x7x: convert to use read_avail")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=77b69a0e679b5ca67c5a2b925c195d22dadff12d)
  - [95d22154d6bb ("staging: iio: tsl2x7x: don't setup event handlers if interrupts are not configured")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=95d22154d6bb980a80d59e500e8350d9a0e03f92)
  - [deaecbef3664 ("staging: iio: tsl2x7x: migrate *_thresh_period sysfs attributes to iio_event_spec")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=deaecbef366497c3435b573fed7991d89af9f59c)
  - [4546813a7f6b ("staging: iio: tsl2x7x: migrate in_illuminance0_integration_time sysfs attribute to iio_chan_spec")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=4546813a7f6b3dc67ac258666092b1952c4e2ea1)
  - [c06c4d793584 ("staging: iio: tsl2x7x/tsl2772: move out of staging")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=c06c4d793584b965bf5fa3fb107f6279643574e2)

  Once the staging cleanup was done, additional changes were required upstream in order to support
  the Nexus 5.

  - [94cd1113aaa0 ("iio: tsl2772: add support for reading proximity led settings from device tree")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=94cd1113aaa07762c57032e2e6212531f5308893)
  - [75de3b570b1c ("iio: tsl2772: add support for avago,apds9930")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=75de3b570b1c80f185df5289cb781e453fd64502)
  - [7c14947e4d3d ("iio: tsl2772: add support for regulator framework")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=7c14947e4d3d8585cc047b132cd1a4ac3167928c)
  - [bd9392507588 ("ARM: dts: qcom: msm8974-hammerhead: add device tree bindings for ALS / proximity")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=bd9392507588483da81337cb430531d1cb114845)
  - [1ed80a817bc4 ("dt-bindings: iio: tsl2772: add new bindings")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=1ed80a817bc42de91701cc60e58d968077359a58)
  - [28b6977e089d ("dt-bindings: iio: tsl2772: add binding for avago,apds9930")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=28b6977e089dda97f8f32ac1a6a223f59e7065f4)

- The phone contains a [BQ24192](http://www.ti.com/lit/pdf/slusaw5) for the USB charger and for
  system power path management.

  - [161a2135e082 ("power: supply: bq24190_charger: add extcon support for USB OTG")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=161a2135e08274a6fa9742e1c020d8138d0032a1)
  - [8e49c0b4bbe9 ("dt-bindings: power: supply: bq24190_charger: add bq24192 and usb-otg-vbus")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=8e49c0b4bbe9482a26e8ad26a99ee99b806f6ac4)
  - [5ea67bb0b090 ("power: supply: bq24190_charger: add support for bq24192 variant")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=5ea67bb0b090033750a91325448dbee1d5b58b01)
  - [74d09c927cb6 ("power: supply: bq24190_charger: add of_match for usb-otg-vbus regulator")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=74d09c927cb69bd10c63e0c6dd3d1c71709ee7ea)

- The
  [InvenSense mpu6515 gyroscope / accelerometer](https://www.invensense.com/wp-content/uploads/2015/02/PS-MPU-9250A-01-v1.1.pdf),
  [Asahi Kasei ak8963 magnetometer](https://www.akm.com/akm/en/file/datasheet/AK8963C.pdf), and
  [Bosch bmp280 temperature / humidity](https://ae-bst.resource.bosch.com/media/_tech/media/datasheets/BST-BMP280-DS001-19.pdf)
  only required minimal changes in order to support these devices on the phone.

  - [de8df0b9c38d ("iio: imu: mpu6050: add support for 6515 variant")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=de8df0b9c38d8f232f0df03220ff540a54eaf73d)
  - [07c12b1c007c ("iio: imu: mpu6050: add support for regulator framework")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=07c12b1c007c5c1d9c434ec9a19373ce5d87fe04)
  - [703e699dbe2c ("ARM: dts: qcom-msm8974: change invalid flag IRQ NONE to valid value")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=703e699dbe2cd106c406882f5c385485a1156cc9)
  - [fe8d81fe7d9a ("ARM: dts: qcom: msm8974-hammerhead: add device tree bindings for mpu6515")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=fe8d81fe7d9aab6a8e22c8b115eb06b7707087db)
  - [0567022c019a ("ARM: dts: qcom: msm8974-hammerhead: correct gpios property on magnetometer")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=0567022c019ad1a1d7bb980a99797f7a7a11d7d3)

- Flash memory 

  - [03864e57770a ("ARM: dts: qcom: msm8974-hammerhead: increase load on l20 for sdhci")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=03864e57770a9541e7ff3990bacf2d9a2fffcd5d) -
    Corrects an issue where the phone would not boot properly when starting to read from the flash
    memory.
  - [Bisected an issue in linux-next](https://lore.kernel.org/lkml/20181125093750.GA28055@basecamp/)
    related to a change in the regulator framework that caused the the phone to no longer boot. The
    issue was resolved by commit
    [fa94e48e13a1a ("regulator: core: Apply system load even if no consumer loads"](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=fa94e48e13a1).

## Working USB OTG

![USB OTG](images/usb-otg.png?raw=1)

## Contact

Brian Masney: [Email](mailto:masneyb@onstation.org), [Linked In](https://www.linkedin.com/in/brian-masney/), [GitHub](https://github.com/masneyb)
