Here are some of my other patches accepted in mainline that are not related to my Nexus 5
project.

- The [tsl2583.c driver](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/drivers/iio/light/tsl2583.c)
  is one of the staging cleanups that I did and it took
  [44 patches](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/log/drivers/staging/iio/light/tsl2583.c)
  to move the driver out of staging and into mainline. A few notable patches from that work:

  - [371894f5d1a0 ("iio: tsl2583: add runtime power management support")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=371894f5d1a00cd6c03aab0beb9789b474ea46b0)
  - [0b6b361e161d ("staging: iio: tsl2583: move from a global to a per device lux table")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=0b6b361e161db7e56a5f06300dabfb325060f269)
  - [b3d941550d9d ("staging: iio: tsl2583: convert to use iio_chan_spec and {read,write}_raw")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=b3d941550d9d3753ed76f09c9b1015c777f41f17)
  - [2167769aed61 ("staging: iio: tsl2583: fix issue with changes to calibscale and int_time not being set on the chip")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=2167769aed61782b7b966b9dfaac8e357fa5c516)
  - [babe444798eb ("staging: iio: tsl2583: remove redundant power off sequence in taos_chip_on()")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=babe444798ebfe02f2e870322927c7018957c7f3)
  - [143c30f4a51e ("staging: iio: tsl2583: convert illuminance0_calibscale sysfs attr to use iio_chan_spec")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=143c30f4a51ebff3474643994499468cf56240af)
  - [6ba5dee90b24 ("staging: iio: tsl2583: i2c_smbus_write_byte() / i2c_smbus_read_byte() migration")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=6ba5dee90b2483f8a78081376f56e6b65c10ea92)
  - [cade8cde796c ("staging: iio: tsl2583: remove redundant write to the control register in taos_probe()")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=cade8cde796cc330b23f62a24c93d754df62c949)
  - [f44d5c8ac399 ("staging: iio: tsl2583: move out of staging")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=f44d5c8ac3993421370fc00951abd5864ca71689)

- The [isl29028.c driver](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/drivers/iio/light/isl29028.c)
  is one of the staging cleanups that I did and it took
  [24 patches](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/log/drivers/staging/iio/light/isl29028.c)
  to move the driver out of staging and into mainline. A few notable patches from that work:

  - [e4ff6c1b41d6 ("staging: iio: isl29028: correct proximity sleep times")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=e4ff6c1b41d66e929e18a9afaa7d7d5788ff3da8)
  - [45e2852b8b27 ("staging: iio: isl29028: fix incorrect sleep time when taking initial proximity reading")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=45e2852b8b27b92fb0f1ad9c94a8edd65c5a61c8)
  - [2db5054ac28d ("staging: iio: isl29028: add runtime power management support")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=2db5054ac28d4ab2eaa6c67e2d9f61fa5ba006b8)
  - [55bf851b4ad7 ("staging: iio: isl29028: change mdelay() to msleep")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=55bf851b4ad76778ce4e591dbb79006d7107cf3d)
  - [84a76694bc17 ("staging: iio: isl29028: only set proximity sampling rate when proximity is enabled")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=84a76694bc17dd31eed84ab2fae857f18909da42)
  - [0fac96ed50d1 ("staging: iio: isl29028: only set ALS scale when ALS/IR sensing is enabled")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=0fac96ed50d1bb6a0ce8dd44b94d3643a0dc3c91)
  - [105c3de1eb41 ("staging: iio: isl29028: move out of staging")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=105c3de1eb414d17e7b9db116f076026d2767ef6)

- The [isl29018.c driver](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/drivers/iio/light/isl29018.c)
  is one of the staging cleanups that I did and it took
  [18 patches](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/log/drivers/staging/iio/light/isl29018.c)
  to move the driver out of staging and into mainline.

  - [a57504144c62 ("staging: iio: isl29018: move out of staging")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=a57504144c62404472f3cc6a7bf4ada4508d5ddc)

- Other patches

  - [40c30bbf3377 ("platform/x86: ideapad-laptop: Add Lenovo Yoga 910-13IKB to no_hw_rfkill dmi list")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=40c30bbf3377babc4d6bb16b699184236a8bfa27)
  - [f3b0deea8903 ("include: linux: iio: add IIO_ATTR_{RO, WO, RW} and IIO_DEVICE_ATTR_{RO, WO, RW} macros")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=f3b0deea89039373f0d22eafd1ff65a36e957266)
