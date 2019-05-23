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

- gyroscope / accelerometer: /sys/devices/platform/soc/f9968000.i2c/i2c-2/2-0068
- magnetometer: /sys/devices/platform/soc/f9968000.i2c/i2c-2/i2c-3/3-000f
- temperature / humidity / barometer: /sys/devices/platform/soc/f9968000.i2c/i2c-2/i2c-3/3-0076
- proximity / ambient light sensor (ALS): /sys/devices/platform/soc/f9925000.i2c/i2c-1/1-0039
- vibrator: /dev/input/by-path/platform-fd8c3450.vibrator-event
- backlight: /sys/devices/platform/soc/f9967000.i2c/i2c-2/2-0038/backlight/lcd-backlight
- USB: usb0
- WiFi: wlan0
- charger
- serial port: /dev/ttyMSM0. A serial console can be obtained through the headphone jack and
  requires building a custom cable [as described on this page](UART_CABLE.md).

See the [build-kernel](build-kernel) script for how to build and boot a kernel. You'll need to
generate your own initial ramdisk.

## Outstanding patches

- Work in progress patches to get the display partially working on the device. The
  [cover letter](https://lore.kernel.org/lkml/20190509020352.14282-1-masneyb@onstation.org/) for
  this series goes into detail about the issue with the display. This requires the backlight patch
  series below.

  - [drm: msm: add dirty framebuffer helper](https://lore.kernel.org/lkml/20190509020352.14282-3-masneyb@onstation.org/)
  - [ARM: qcom_defconfig: add display-related options](https://lore.kernel.org/lkml/20190509020352.14282-4-masneyb@onstation.org/)
  - [ARM: dts: msm8974: add display support](https://lore.kernel.org/lkml/20190509020352.14282-5-masneyb@onstation.org/)
  - [ARM: dts: qcom: msm8974-hammerhead: add support for backlight](https://lore.kernel.org/lkml/20190509020352.14282-6-masneyb@onstation.org/)
  - [ARM: dts: qcom: msm8974-hammerhead: add support for display](https://lore.kernel.org/lkml/20190509020352.14282-7-masneyb@onstation.org/)

  I pushed [a branch to my GitHub](https://github.com/masneyb/linux/commits/display-works-4.17) with
  15 patches that gets the display to work properly on a 4.17 kernel. The first 10 of those patches
  are already included in newer mainline kernels and were backported.

- Vibrator

  - [ARM: dts: qcom: msm8974-hammerhead: add device tree bindings for vibrator](https://lore.kernel.org/lkml/20190516085018.2207-1-masneyb@onstation.org/)

- Backlight

  - [dt-bindings: backlight: lm3630a: correct schema validation](https://lore.kernel.org/lkml/20190520085846.22320-1-masneyb@onstation.org/)

## Queued for 5.3 merge window

- ALS / proximity

  - [dt-bindings: iio: tsl2772: convert bindings to YAML format](https://lore.kernel.org/lkml/20190425230314.26000-1-masneyb@onstation.org/)
  - [dt-bindings: iio: tsl2583: convert bindings to YAML format](https://lore.kernel.org/lkml/20190425230314.26000-2-masneyb@onstation.org/)
  - [dt-bindings: iio: isl29018: convert bindings to YAML format](https://lore.kernel.org/lkml/20190427182359.27254-1-masneyb@onstation.org/)

## Patches accepted in upstream kernel

- Hierarchical IRQ chip support for Qualcomm spmi-gpio and ssbi-gpio so that device tree consumers
  can request an IRQ directly from the GPIO block rather than having to request an IRQ from the
  underlying PMIC.

  - [697818f383fc ("dt-bindings: pinctrl: qcom-pmic-gpio: add qcom,pmi8998-gpio binding")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=697818f383fc548cdbfb1528c7067994739ace04)
  - [d7ee4d0a6731 ("pinctrl: qcom: spmi-gpio: add support for three new variants")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=d7ee4d0a67315736b402291ed48b77e701c76224)
  - [cfacef373505 ("pinctrl: qcom: spmi-gpio: hardcode IRQ counts")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=cfacef373505dce8735c562a147d14611db259b9)
  - [12a9eeaebba3 ("spmi: pmic-arb: convert to v2 irq interfaces to support hierarchical IRQ chips")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=12a9eeaebba34f4f0abe1548ecb460414e285c49)
  - [ef74f70e5a10 ("gpio: add irq domain activate/deactivate functions")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=ef74f70e5a10cc2a78cc5529e564170cabcda9af)
  - [682aefaa81e6 ("spmi: pmic-arb: disassociate old virq if hwirq mapping already exists")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=682aefaa81e6c9b76bf45391f92a2b9c6ec96a0c)
  - [ca69e2d165eb ("qcom: spmi-gpio: add support for hierarchical IRQ chip")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=ca69e2d165eb3d060cc9ad70a745e27a2cf4310b)
  - [5f540fb4821a ("ARM: dts: qcom: pm8941: add interrupt controller properties")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=5f540fb4821a5444350ab3311fff60013d755d8f)
  - [c9a0ef552894 ("ARM: dts: qcom: pma8084: add interrupt controller properties")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=c9a0ef552894ebdd6e4efc064ef10ddcb578a42f)
  - [a61326c076f2 ("arm64: dts: qcom: pm8005: add interrupt controller properties")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=a61326c076f25b7b808cccb827576808ec1cfa9d)
  - [a1738363e41a ("arm64: dts: qcom: pm8998: add interrupt controller properties")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=a1738363e41a65733a0d277d8189efa98315fdff)
  - [8cff9c8a7881 ("arm64: dts: qcom: pmi8994: add interrupt controller properties")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=8cff9c8a78810ca09fd7c4d6d5d4f86a8b113059)
  - [f14a5e6da4a5 ("arm64: dts: qcom: pmi8998: add interrupt controller properties")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=f14a5e6da4a50e78a18384faf81eef6171909d3f)
  - [e7dc6af82c28 ("spmi: pmic-arb: revert "disassociate old virq if hwirq mapping already exists"")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=e7dc6af82c284b8c79a0be5d2c9b555c3d793a3e)
  - [760a160e8b89 ("pinctrl: qcom: spmi-gpio: select IRQ_DOMAIN_HIERARCHY in Kconfig")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=760a160e8b899f5ebcab99da17feebbe40ec42f1)
  - [5c713d9394f3 ("spmi: pmic-arb: select IRQ_DOMAIN_HIERARCHY in Kconfig")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=5c713d9394f3aabb73975dbf4db3c6502dc68956)
  - [38f7ae9bdfb6 ("genirq: export irq_chip_set_wake_parent symbol")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=38f7ae9bdfb6570271c7429d8d72784465c6281e)
  - [86291029e97e ("pinctrl: qcom: ssbi-gpio: hardcode IRQ counts")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=86291029e97eaf6a9c2ed43e7968ba8cf9f9f3b7)
  - [b5c231d8c803 ("genirq: introduce irq_domain_translate_twocell")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=b5c231d8c8037f63d34199ea1667bbe1cd9f940f)
  - [3324a7c1a227 ("mfd: pm8xxx: convert to v2 irq interfaces to support hierarchical IRQ chips")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=3324a7c1a2273e502a4f3c02a021e1d15ce2c458)
  - [ee08e24c2e76 ("mfd: pm8xxx: disassociate old virq if hwirq mapping already exists")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=ee08e24c2e761e6aa3ef2c03cc2004e11fe111b3)
  - [9d2b563bc23a ("qcom: ssbi-gpio: add support for hierarchical IRQ chip")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=9d2b563bc23acfa93e7716b3396fd2f79fa8f0cd)
  - [e2f6c8881287 ("arm: dts: qcom: apq8064: add interrupt controller properties")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=e2f6c8881287cb0689408b244d1a1e651eb0f67d)
  - [a796fab2c605 ("arm: dts: qcom: msm8660: add interrupt controller properties")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=a796fab2c605d6340512c51c6c3fa1c581357993)
  - [582648f5ef14 ("arm: dts: qcom: mdm9615: add interrupt controller properties")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=582648f5ef14383c66b26834b9a98ade8b4da74c)
  - [1a25d59a5529 ("mfd: pm8xxx: revert "disassociate old virq if hwirq mapping already exists"")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=1a25d59a55292631a6c601fda5413abc297097b7)
  - [de744e01aa3a ("mfd: pm8xxx: select IRQ_DOMAIN_HIERARCHY in Kconfig")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=de744e01aa3af421470eb9725574e3cbce319053)
  - [79890c2ec486 ("qcom: ssbi-gpio: correct boundary conditions in pm8xxx_domain_translate")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=79890c2ec4860c3b715f89248c51abcc76a1fa39)

- When attempting to setup up a gpio hog, device probing would repeatedly fail with -EPROBE_DEFERED
  errors during system boot due to a circular dependency between the gpio and pinctrl frameworks.

  - [149a96047237 ("pinctrl: qcom: spmi-gpio: fix gpio-hog related boot issues")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=149a96047237574b756d872007c006acd0cc6687)
  - [7ed078557738 ("pinctrl: qcom: ssbi-gpio: fix gpio-hog related boot issues")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=7ed07855773814337b9814f1c3e866df52ebce68)
  - [cdd3d64d843a ("ARM: dts: qcom: pm8941: add gpio-ranges")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=cdd3d64d843a2a4c658a182b744bfefbd021d542)
  - [33984dd6c4bb ("ARM: dts: qcom: apq8064: add gpio-ranges")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=33984dd6c4bb89b606e38ed5810a157fe81b241c)
  - [3bc5163ebbac ("ARM: dts: qcom: mdm9615: add gpio-ranges")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=3bc5163ebbacf0f0d319f73de3d5e09a61e74f92)
  - [546f72e7ecb2 ("ARM: dts: qcom: msm8660: add gpio-ranges")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=546f72e7ecb25594a30f884da0d8ae79ad278cef)
  - [05d86a0ae83b ("ARM: dts: qcom: pma8084: add gpio-ranges")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=05d86a0ae83b62a11f74760d8edf84580beccb3e)
  - [136e9d920dc6 ("arm64: dts: qcom: pm8005: add gpio-ranges")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=136e9d920dc616f74642efaf1413f82096ddd989)
  - [99c70e728623 ("arm64: dts: qcom: pm8998: add gpio-ranges")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=99c70e7286237ea0701523555623faf6b49ce0db)
  - [21750eb93ea9 ("arm64: dts: qcom: pmi8994: add gpio-ranges")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=21750eb93ea9ebe445c922f5319c6b490f45f70d)
  - [d1fe337337ed ("arm64: dts: qcom: pmi8998: add gpio-ranges")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=d1fe337337edd37233e2fe65a43e7da6155fbec6)

- The phone contains an [Avago APDS 9930](https://docs.broadcom.com/docs/AV02-3190EN)
  proximity / ambient light sensor (ALS), which is register compatible with the
  [TAOS TSL2772 sensor](https://ams.com/documents/20143/36005/TSL2772_DS000181_2-00.pdf).
  The [tsl2772.c driver](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/drivers/iio/light/tsl2772.c)
  is one of the staging cleanups that I did and it took
  [74 patches](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/log/drivers/staging/iio/light/tsl2x7x.c)
  to move the driver out of staging and into mainline. A few notable patches from that work:

  - [498efcd08114 ("staging: iio: tsl2x7x: correct integration time and lux equation")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=498efcd08114905074a644bf81f82ce5c62eac43)
  - [9861d2daaf28 ("staging: iio: tsl2x7x: correct IIO_EV_INFO_PERIOD values"](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=9861d2daaf28e7beaa0c655206c595094d47ccd8)
  - [2ab5b7245367 ("staging: iio: tsl2x7x: make proximity sensor function correctly")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=2ab5b72453672ea18a176925becc40888df435ce)
  - [19422bde046a ("staging: iio: tsl2x7x: use auto increment I2C protocol")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=19422bde046a7fa549565300d0a4c4dc1e8d585a)
  - [9e4701eaef02 ("staging: iio: tsl2x7x: correct interrupt handler trigger")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=9e4701eaef02e1192faca2d0b3529249522f6253)
  - [77b69a0e679b ("staging: iio: tsl2x7x: convert to use read_avail")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=77b69a0e679b5ca67c5a2b925c195d22dadff12d)
  - [95d22154d6bb ("staging: iio: tsl2x7x: don't setup event handlers if interrupts are not configured")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=95d22154d6bb980a80d59e500e8350d9a0e03f92)
  - [deaecbef3664 ("staging: iio: tsl2x7x: migrate *_thresh_period sysfs attributes to iio_event_spec")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=deaecbef366497c3435b573fed7991d89af9f59c)
  - [4546813a7f6b ("staging: iio: tsl2x7x: migrate in_illuminance0_integration_time sysfs attribute to iio_chan_spec")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=4546813a7f6b3dc67ac258666092b1952c4e2ea1)
  - [a2fdb4e1a6c8 ("staging: iio: tsl2x7x: use either direction for IIO_EV_INFO_{ENABLE,PERIOD}")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=a2fdb4e1a6c8e68f95eae71724a4e071b8394a72)
  - [2f58efa96373 ("staging: iio: tsl2x7x: move integration_time* attributes to IIO_INTENSITY channel")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=2f58efa96373782a9c26203479c28a59976edfc5)
  - [bce075d0ec4b ("staging: iio: tsl2x7x: simplify tsl2x7x_prox_cal()")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=bce075d0ec4b6155cf4f52a7e56aa2dd3b668679)
  - [c06c4d793584 ("staging: iio: tsl2x7x/tsl2772: move out of staging")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=c06c4d793584b965bf5fa3fb107f6279643574e2)

  Once the staging cleanup was done, additional changes were required upstream in order to support
  the Nexus 5.

  - [94cd1113aaa0 ("iio: tsl2772: add support for reading proximity led settings from device tree")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=94cd1113aaa07762c57032e2e6212531f5308893)
  - [75de3b570b1c ("iio: tsl2772: add support for avago,apds9930")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=75de3b570b1c80f185df5289cb781e453fd64502)
  - [7c14947e4d3d ("iio: tsl2772: add support for regulator framework")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=7c14947e4d3d8585cc047b132cd1a4ac3167928c)
  - [bd9392507588 ("ARM: dts: qcom: msm8974-hammerhead: add device tree bindings for ALS / proximity")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=bd9392507588483da81337cb430531d1cb114845)
  - [1ed80a817bc4 ("dt-bindings: iio: tsl2772: add new bindings")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=1ed80a817bc42de91701cc60e58d968077359a58)
  - [28b6977e089d ("dt-bindings: iio: tsl2772: add binding for avago,apds9930")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=28b6977e089dda97f8f32ac1a6a223f59e7065f4)

- Vibrator - Use
  [rumble-test.c](https://git.collabora.com/cgit/user/sre/rumble-test.git/plain/rumble-test.c) to
  test the driver.

  - [0f681d09e66e ("Input: add new vibrator driver for various MSM SOCs")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=0f681d09e66ea6833e6173180ff3892e9026ab71)

- The phone contains a [BQ24192](http://www.ti.com/lit/pdf/slusaw5) for the USB charger and for
  system power path management.

  - [161a2135e082 ("power: supply: bq24190_charger: add extcon support for USB OTG")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=161a2135e08274a6fa9742e1c020d8138d0032a1)
  - [8e49c0b4bbe9 ("dt-bindings: power: supply: bq24190_charger: add bq24192 and usb-otg-vbus")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=8e49c0b4bbe9482a26e8ad26a99ee99b806f6ac4)
  - [5ea67bb0b090 ("power: supply: bq24190_charger: add support for bq24192 variant")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=5ea67bb0b090033750a91325448dbee1d5b58b01)
  - [74d09c927cb6 ("power: supply: bq24190_charger: add of_match for usb-otg-vbus regulator")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=74d09c927cb69bd10c63e0c6dd3d1c71709ee7ea)

- The phone contains a micro USB port that can be used for charging the battery or in USB OTG
  mode so that other USB devices can be connected to the phone. You can also setup USB networking
  between your computer and the phone. Ensure that `CONFIG_USB_ETH` is in your .config file since
  qcom_defconfig does not have this option. The USB support requires the charger and gpio hogging
  patches listed on this page.

  - [fb143fcbb9ad ("ARM: dts: qcom: msm8974-hammerhead: add USB OTG support")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=fb143fcbb9ad361004f2818e9dcb52b2556bfec1)

- The phone contains a [TI LM3630A](https://www.ti.com/product/LM3630A) for the LCD backlight.

  - [d3f48ec0954c ("backlight: lm3630a: return 0 on success in update_status functions")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=d3f48ec0954c6aac736ab21c34a35d7554409112)
  - [32fcb75c66a0 ("dt-bindings: backlight: add lm3630a bindings")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=32fcb75c66a0cb66db9ec4f777f864675e5aebb2)
  - [8fbce8efe15c ("backlight: lm3630a: add firmware node support")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=8fbce8efe15cd2ca7a4947bc814f890dbe4e43d7)

- Some small fixes for the msm drm/kms driver.

  - [e2f597a20470 ("drm/msm: remove resv fields from msm_gem_object struct")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=e2f597a20470d7dfeca49c3d45cb8a7e46d3cf66)
  - [90f94660e531 ("drm/msm: correct attempted NULL pointer dereference in debugfs")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=90f94660e53189755676543954101de78c26253b)

- The
  [InvenSense mpu6515 gyroscope / accelerometer](https://www.invensense.com/wp-content/uploads/2015/02/PS-MPU-9250A-01-v1.1.pdf),
  [Asahi Kasei ak8963 magnetometer](https://www.akm.com/akm/en/file/datasheet/AK8963C.pdf), and
  [Bosch bmp280 temperature / humidity / barometer](https://ae-bst.resource.bosch.com/media/_tech/media/datasheets/BST-BMP280-DS001-19.pdf)
  only required minimal changes in order to support these devices on the phone.

  - [de8df0b9c38d ("iio: imu: mpu6050: add support for 6515 variant")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=de8df0b9c38d8f232f0df03220ff540a54eaf73d)
  - [07c12b1c007c ("iio: imu: mpu6050: add support for regulator framework")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=07c12b1c007c5c1d9c434ec9a19373ce5d87fe04)
  - [703e699dbe2c ("ARM: dts: qcom-msm8974: change invalid flag IRQ NONE to valid value")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=703e699dbe2cd106c406882f5c385485a1156cc9)
  - [fe8d81fe7d9a ("ARM: dts: qcom: msm8974-hammerhead: add device tree bindings for mpu6515")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=fe8d81fe7d9aab6a8e22c8b115eb06b7707087db)
  - [0567022c019a ("ARM: dts: qcom: msm8974-hammerhead: correct gpios property on magnetometer")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=0567022c019ad1a1d7bb980a99797f7a7a11d7d3)
  - [d2b863baf1c7 ("iio: pressure: bmp280: remove unused options from device tree documentation")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=d2b863baf1c7d92969c2a9dcada3c6b14e5dbbc4)

- WiFi - This phone has a [Broadcom (now Cypress) 4339](http://www.cypress.com/file/298016/download)
  for wireless.

  - [ec4c6c57af57 ("ARM: dts: qcom: msm8974-hammerhead: add WiFi support")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=ec4c6c57af576e10c70547b782db04eb3602f5f4)

- Panel

  - [9e0b597534b4 ("dt-bindings: drm/panel: simple: add lg,acx467akm-7 panel")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=9e0b597534b4c065e2c083c7478d6f3175088fdd)
  - [debcd8f954be ("drm/panel: simple: add lg,acx467akm-7 panel")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=debcd8f954be2b1f643e76b2400bc7c3d12b4594)

- Flash memory 

  - [03864e57770a ("ARM: dts: qcom: msm8974-hammerhead: increase load on l20 for sdhci")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=03864e57770a9541e7ff3990bacf2d9a2fffcd5d) -
    Corrects an issue where the phone would not boot properly when starting to read from the flash
    memory.
  - [Bisected an issue in linux-next](https://lore.kernel.org/lkml/20181125093750.GA28055@basecamp/)
    related to a change in the regulator framework that caused the the phone to no longer boot. The
    issue was resolved by commit
    [fa94e48e13a1a ("regulator: core: Apply system load even if no consumer loads"](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=fa94e48e13a1).

- defconfig

  - [acd92c5a1149 ("ARM: qcom_defconfig: add options for LG Nexus 5 phone")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=acd92c5a11493bdf137aba6e21e865331d7d90d7)

- I have [another page](OTHER_PATCHES.md) that describes some of my other kernel work that's not
  related to this Nexus 5 project.

## Working USB OTG

![USB OTG](images/usb-otg.png?raw=1)

## Other resources

- A full teardown of the Nexus 5 is
  [available on ifixit](https://www.ifixit.com/Teardown/Nexus+5+Teardown/19016).
- [Downstream MSM 3.4 kernel sources](https://github.com/AICP/kernel_lge_hammerhead) with additions
   from the community. Use hammerhead_defconfig when building this kernel.
- [postmarketOS](https://postmarketos.org/) for the
  [Nexus 5](https://wiki.postmarketos.org/wiki/Google_Nexus_5_(lg-hammerhead))

## Contact

Brian Masney: [Email](mailto:masneyb@onstation.org), [Linked In](https://www.linkedin.com/in/brian-masney/), [GitHub](https://github.com/masneyb)
