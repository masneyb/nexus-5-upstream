This page describes the current development efforts to port the
[upstream Linux Kernel](https://www.kernel.org/) to the
[LG Nexus 5 (hammerhead) phone](https://en.wikipedia.org/wiki/Nexus_5). This work benefits
other devices that use the Qualcomm msm8974 System on Chip (SoC) such as the Fairphone 2,
OnePlus One, Samsung Galaxy S5, Sony Xperia Z1, Sony Xperia Z2 tablets, and current devices
that use some of the same IP blocks within newer Qualcomm SoCs.

The factory kernel image is based on the upstream Linux 3.4 kernel that was released in May
2012, and adds almost 2 million lines of code on top of the upstream kernel. This factory
image is abandoned and no longer receives security updates. The goal is to eventually get
all of the major components working upstream so that the phone will work with the latest
upstream kernel. These patches will eventually appear in the
[Android kernels](https://android.googlesource.com/kernel/common/) as they rebase their kernels
onto newer upstream LTS kernel releases.

## Hardware status

The following components work upstream without any additional patches: display, backlight,
touchscreen, USB, WiFi, charger, gyroscope / accelerometer, magnetometer,
temperature / humidity / barometer, proximity / ambient light sensor (ALS), serial console.

My [linux tree on GitHub](https://github.com/masneyb/linux) contains work-in-progress patches
that adds support for the GPU, modem, and vibrator. See my
[v5.5 patch series cover letter](https://github.com/masneyb/nexus-5-upstream/blob/master/out-of-tree-patches/upstream-patches/v5.5/0000-cover-letter.patch)
that gives a high-level overview of the status of those patches.

I have work in progress patches available below to get the external display over HDMI and the IOMMU
working, where the latter is the last piece that's needed to support the GPU upstream. The hardware
isn't fully working yet with these patches.

See the [TODO list](TODO.md) for information about other components and links to some out-of-tree
patches.

See the [peripheral paths page](PERIPHERAL_PATHS.md) for the location of the major peripherals
on the filesystem.

## Phone user space

I've been running [postmarketOS](https://postmarketos.org/) on the phone. Follow the instructions
on their [Nexus 5 page](https://wiki.postmarketos.org/wiki/Google_Nexus_5_(lg-hammerhead)) that
describes how to install it. Here's my [pmbootstrap.cfg](pmbootstrap.cfg) config file. Once that's
installed, see my [build-kernel](build-kernel) script for how to build and boot a custom kernel
into a postmarketOS userspace.

A serial console can be obtained through the headphone jack and requires building a custom cable
[as described on this page](UART_CABLE.md). You will want to make a cable if you plan to do any
development work.

![External GPIO Example](images/external-gpio.gif?raw=1)

See the [gpio_demoy.py script](initrd/copy-to-root-fs/usr/local/bin/gpio_demo.py) for the source
code to the GTK+ application controlling the external LEDs in the image above. The phone is running
XFCE4 and postmarketOS on an upstream Linux kernel. This
[Tiny OTG USB adapter](https://www.adafruit.com/product/2910) is used on that video.

## Upstream contribution summary

The following is a summary of my upstream Linux kernel contributions as part of this project:

- Created a new Qualcomm msm8974 interconnect driver that allows setting system bandwidth
  requirements between various network-on-chip fabrics. This is required in order to support the
  display, GPU and various other devices upstream. [Patches](#interconnect)
- Created a new On Chip Memory (OCMEM) allocator driver that allows various clients to allocate
  memory from OCMEM based on performance, latency and power requirements. This is typically used
  by the GPU, camera/video, and audio components on some Snapdragon SoCs. [Patches](#ocmem)
- Hierarchical IRQ chip support for all Qualcomm platforms (spmi-gpio and ssbi-gpio) so that
  device tree consumers can request an IRQ directly from the GPIO block rather than having to
  request an IRQ from the underlying PMIC. Contributed to the generic implementation in the
  GPIO core. [Patches](#gpio-hierarchy)
- When attempting to setup up a GPIO hog, device probing would repeatedly fail with
  -EPROBE_DEFERED errors during system boot due to a circular dependency between the GPIO and
  Pinctrl frameworks. [Patches](#gpio-hog)
- Corrected issue with the Freedreno DRM/KMS driver not working properly on old command-mode DSI
  panels, dirty framebuffer helper support, corrected msm8974 gfx3d clock, wired display into
  msm8974 device tree, corrected issues when running without an IOMMU, and silenced several
  -EPROBE_DEFER warnings. [Patches](#display)
- Created PLL driver and necessary device tree changes for external display over HDMI (work in
  progress), converted analogix-anx78xx driver to use i2c_new_dummy_device(), added necessary
  regulator node to device tree, and added support for new variants to the analogix-anx78xx
  driver. [Patches](#hdmi)
- Took over maintainership of the TAOS tsl2772 driver upstream for the proximity detection and
  ambient light sensing, performed the staging graduation, corrected equations and timings for
  the 10 hardware variants supported by the driver, got interrupt and proximity functionality
  working properly, added regulator support, and numerous cleanups to the driver.
  [Patches](#tsl2772)
- Added firmware node support to the existing lm3630a driver and corrected an issue updating the
  brightness level via sysfs. [Patches](#lm3630a)
- Added extcon support to the existing bq24190_charger driver upstream, and support for USB OTG
  to device tree. [Patches](#bq24192)
- Work in progress patches to get the vibrator supported upstream. Working with the upstream
  maintainers to see where this code should go upstream. [Patches](#vibrator)
- Work in progress patches to get the IOMMU for the display and GPU working. [Patches](#iommu)
- Cleaned up patches from other people and got them accepted upstream for the following
  components: [various I2C sensors](#various-i2c-sensors), [panel](#panel), [WiFi](#wifi),
  [touchscreen](#touchscreen), and [sdhci](#sdhci).
- Bisected bugs found in linux-next with the [regulator subsystem](#bisect-regulator) and
  the [mmc/sdhci system](#bisect-wifi).
- I have [another page](OTHER_PATCHES.md) that describes some of my other kernel work that's not
  related to this Nexus 5 project. A few highlights: 3 staging graduations in the IIO subsystem,
  runtime power management, and various other driver cleanups.

![Display](images/Nexus5-kmscube-and-fb-console.png?raw=1)

# Patches

Note that the ones with a short git SHA at the beginning are in the mainline kernel, the ones
marked *Queued* are in linux-next, and the others are labeled either *Pending* or *Needs Work*.

- <a id="interconnect"></a>Qualcomm MSM8974 interconnect driver that allows setting system bandwidth
  requirements between various network-on-chip fabrics. This is required in order to support the
  display, GPU and various other devices upstream. [Patches](#interconnect)

  - [6120e5d821c0 ("dt-bindings: interconnect: qcom: add msm8974 bindings")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=6120e5d821c0e3104ddbc2ad5dd126e0c9eb20f2)
  - [4e60a9568dc6 ("interconnect: qcom: add msm8974 driver")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=4e60a9568dc6f411d4f631fe33b5553d080b7e8c)
  - *Queued*: [ARM: dts: qcom: msm8974: add interconnect nodes](https://lore.kernel.org/lkml/20191024103140.10077-5-masneyb@onstation.org/)
  - *Queued*: [dt-bindings: drm/msm/gpu: document second interconnect](https://lore.kernel.org/lkml/20191122012645.7430-2-masneyb@onstation.org/)
  - *Queued*: [drm/msm/a3xx: set interconnect bandwidth vote](https://lore.kernel.org/lkml/20191122012645.7430-4-masneyb@onstation.org/)
  - *Queued*: [drm/msm/a4xx: set interconnect bandwidth vote](https://lore.kernel.org/lkml/20191122012645.7430-5-masneyb@onstation.org/)
  - *Queued*: [ARM: qcom_defconfig: add msm8974 interconnect support](https://lore.kernel.org/lkml/20191024103140.10077-2-masneyb@onstation.org/)

- <a id="ocmem"></a>The On Chip Memory (OCMEM) allocator allows various clients to allocate memory
  from OCMEM based on performance, latency and power requirements. This is typically used by the
  GPU, camera/video, and audio components on some Snapdragon SoCs.

  - [957fd69d396b ("dt-bindings: soc: qcom: add On Chip MEMory (OCMEM) bindings")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=957fd69d396b2cc9b74c3b31a70fe7f266aa8c16)
  - [198a72c8f9ee ("dt-bindings: display: msm: gmu: add optional ocmem property")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=198a72c8f9ee8eef24bacde6a3b3feb3b026ee04)
  - [88c1e9404f1d ("soc: qcom: add OCMEM driver")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=88c1e9404f1deee02e52d13aae3d9ee2cabd66f5)
  - [26c0b26dcd00 ("drm/msm/gpu: add ocmem init/cleanup functions")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=26c0b26dcd005d9d6de9246737177e7af821859a)
  - [bfcb7e1555ec ("soc: qcom: ocmem: add missing includes")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=bfcb7e1555ecc157cea23e35057002e3055e90a6)
  - [ARM: dts: qcom: msm8974: add ocmem node](https://lore.kernel.org/lkml/20191024103140.10077-4-masneyb@onstation.org/)
  - [b2181be1cfb8 ("ARM: qcom_defconfig: add ocmem support")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=b2181be1cfb81da3fad0f8b6994b2e714ae66876)
  - [b0a1614fb1f5 ("firmware: qcom: scm: add OCMEM lock/unlock interface")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=b0a1614fb1f58520938968ebe1f4f11bcf34839e)
  - [0434a4061471 ("firmware: qcom: scm: add support to restore secure config to qcm_scm-32")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=0434a4061471a9afc2b2061add496e58ba4bb92d)

- <a id="gpio-hierarchy"></a>Hierarchical IRQ chip support for all Qualcomm platforms (spmi-gpio and
  ssbi-gpio) so that device tree consumers can request an IRQ directly from the GPIO block rather
  than having to request an IRQ from the underlying PMIC. Contributed to the generic implementation
  in the GPIO core.

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
  - [fdd61a013a24 ("gpio: Add support for hierarchical IRQ domains")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=fdd61a013a24f2699aec1a446f0168682b6f9ec4)
  - [821c76c4c374 ("qcom: spmi-gpio: convert to hierarchical IRQ helpers in gpio core")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=821c76c4c374adf0c7a7608ee4661aa801f3c1c5)
  - [ae436fe81053 ("qcom: ssbi-gpio: convert to hierarchical IRQ helpers in gpio core")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=ae436fe81053cd6cb294214be382b545565440cc)

- <a id="gpio-hog"></a>When attempting to setup up a gpio hog, device probing would repeatedly fail
  with -EPROBE_DEFERED errors during system boot due to a circular dependency between the gpio and
  pinctrl frameworks. This fix is required in order to support USB on the Nexus 5 since one GPIO
  pin needs to be hogged high at startup on the Nexus 5.

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

- <a id="display"></a>Display is supported by the msm drm/kms driver upstream.

  - [2bab52af6fe6 ("drm/msm: add support for per-CRTC max_vblank_count on mdp5")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=2bab52af6fe68c43b327a57e5ce5fc10eefdfadf)
  - [648fdc3f6475 ("drm/msm: add dirty framebuffer helper")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=648fdc3f6475d96de287a849a31d89e79ba7669c)
  - [5a9fc531f6ec ("ARM: dts: msm8974: add display support")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=5a9fc531f6ecc987980fdd025928790c5db5f48a)
  - [489bacb29818 ("ARM: dts: qcom: msm8974-hammerhead: add support for display")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=489bacb29818865d2db63d4800f4ddff56929031)
  - [e2f597a20470 ("drm/msm: remove resv fields from msm_gem_object struct")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=e2f597a20470d7dfeca49c3d45cb8a7e46d3cf66)
  - [d67f1b6d0e0b ("drm/msm: correct attempted NULL pointer dereference in put_iova")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=d67f1b6d0e0be8240186e3cc998353e52ed6ea31)
  - [90f94660e531 ("drm/msm: correct attempted NULL pointer dereference in debugfs")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=90f94660e53189755676543954101de78c26253b)
  - [7af5cdb158f3 ("drm/msm: correct NULL pointer dereference in context_init")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=7af5cdb158f3398a3220bd2fe81cec8d2be9317c)
  - [add5bff4aa76 ("drm/msm/phy/dsi_phy: silence -EPROBE_DEFER warnings")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=add5bff4aa769108d05fbef0240000e7334a33b9)
  - [fd6c798b58e0 ("drm/msm/hdmi: silence -EPROBE_DEFER warning")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=fd6c798b58e0d6adaf336a0ddc91f127ff82a75d)
  - [ef7a5baf64ce ("ARM: qcom_defconfig: add display-related options")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=ef7a5baf64ce83c04b2ced044ded31528820fef7)
  - *Queued*: [clk: qcom: mmcc8974: move gfx3d_clk_src from the mmcc to rpm](https://lore.kernel.org/lkml/20191115123931.18919-1-masneyb@onstation.org/)
  - *Pending*: [drm/msm/mdp5: rate limit pp done timeout warnings](https://lore.kernel.org/lkml/20200118204120.1039774-1-masneyb@onstation.org/)
  - *Needs work*: [drm/msm/mdp5: enable autorefresh](https://lore.kernel.org/lkml/20191230020053.26016-2-masneyb@onstation.org/)

- <a id="hdmi"></a>An external monitor can be hooked up via the
  [Analogix 7808 HDMI bridge](https://www.analogix.com/en/system/files/ANX7808_product_brief.pdf)
  using a SlimPort cable. I'm currently using an 'Analogix Semiconductor SP6001 SlimPort Micro-USB
  to 4K HDMI Adapter'.

  - [ac242e2cfd14 ("ARM: dts: qcom: pm8941: add 5vs2 regulator node")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=ac242e2cfd14f5be99fc2e6888702d02099d2f91)
  - [2f932367d219 ("drm/bridge: analogix-anx78xx: convert to i2c_new_dummy_device")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=2f932367d219ad4ce56278035a1ee1ca03c48308)
  - [025910db8057 ("drm/bridge: analogix-anx78xx: add support for 7808 addresses")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=025910db8057f60d2d2aa11002f7751e3eb66588)
  - [2fb658a603ba ("dt-bindings: drm/bridge: analogix-anx78xx: add new variants")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=2fb658a603bab4e41834a4f32475bbea9c01cf46)
  - [0273831882c5 ("drm/bridge: analogix-anx78xx: add new variants")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=0273831882c5215f49628dcb3cb567b67cd7af39)
  - [2708e876272d ("drm/bridge: analogix-anx78xx: silence -EPROBE_DEFER warnings")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=2708e876272d89bbbff811d12834adbeef85f022)
  - *Queued*: [ARM: qcom_defconfig: add anx78xx HDMI bridge support](https://lore.kernel.org/lkml/20191024103140.10077-3-masneyb@onstation.org/)
  - *Needs work*: [drm/bridge: analogix-anx78xx: add support for avdd33 regulator](https://lore.kernel.org/lkml/20191007014509.25180-2-masneyb@onstation.org/)
  - *Needs work*: [drm/msm/hdmi: add msm8974 PLL support](https://lore.kernel.org/lkml/20191007014509.25180-3-masneyb@onstation.org/)
  - *Needs work*: [ARM: dts: qcom: msm8974: add HDMI nodes](https://lore.kernel.org/lkml/20191007014509.25180-5-masneyb@onstation.org/)
  - *Needs work*: [ARM: dts: qcom: msm8974-hammerhead: add support for external display](https://lore.kernel.org/lkml/20191007014509.25180-6-masneyb@onstation.org/)

- <a id="tsl2772"></a>The phone contains an
  [Avago APDS 9930](https://docs.broadcom.com/docs/AV02-3190EN) proximity / ambient light sensor
  (ALS), which is register compatible with the
  [TAOS tsl2772 sensor](https://ams.com/documents/20143/36005/TSL2772_DS000181_2-00.pdf). By mere
  coincidence, the
  [tsl2772.c driver](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/drivers/iio/light/tsl2772.c)
  is one of the staging cleanups that I did and it took
  [74 patches](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/log/drivers/staging/iio/light/tsl2x7x.c)
  to move that driver out of staging and into mainline. A few notable patches from that work:

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
  - [17b62779cbe4 ("dt-bindings: iio: tsl2772: convert bindings to YAML format")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=17b62779cbe40773e10a83af000e51c29b764575)

- <a id="lm3630a"></a>The phone contains a [TI lm3630a](https://www.ti.com/product/LM3630A) for the
  LCD backlight.

  - [d3f48ec0954c ("backlight: lm3630a: return 0 on success in update_status functions")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=d3f48ec0954c6aac736ab21c34a35d7554409112)
  - [32fcb75c66a0 ("dt-bindings: backlight: add lm3630a bindings")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=32fcb75c66a0cb66db9ec4f777f864675e5aebb2)
  - [8fbce8efe15c ("backlight: lm3630a: add firmware node support")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=8fbce8efe15cd2ca7a4947bc814f890dbe4e43d7)
  - [ef4db28c1f45 ("dt-bindings: backlight: lm3630a: correct schema validation")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=ef4db28c1f45cda6989bc8a8e45294894786d947)
  - [030b6d48ebfb ("ARM: dts: qcom: msm8974-hammerhead: add support for backlight")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=030b6d48ebfb8d45f397aa13da712210c9803042)

- <a id="bq24192"></a>The phone contains a [BQ24192](http://www.ti.com/lit/pdf/slusaw5) for the
  charger, system power path management, and for USB OTG support. This requires the GPIO hogging
  patches on this page.

  - [161a2135e082 ("power: supply: bq24190_charger: add extcon support for USB OTG")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=161a2135e08274a6fa9742e1c020d8138d0032a1)
  - [8e49c0b4bbe9 ("dt-bindings: power: supply: bq24190_charger: add bq24192 and usb-otg-vbus")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=8e49c0b4bbe9482a26e8ad26a99ee99b806f6ac4)
  - [5ea67bb0b090 ("power: supply: bq24190_charger: add support for bq24192 variant")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=5ea67bb0b090033750a91325448dbee1d5b58b01)
  - [74d09c927cb6 ("power: supply: bq24190_charger: add of_match for usb-otg-vbus regulator")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=74d09c927cb69bd10c63e0c6dd3d1c71709ee7ea)
  - [fb143fcbb9ad ("ARM: dts: qcom: msm8974-hammerhead: add USB OTG support")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=fb143fcbb9ad361004f2818e9dcb52b2556bfec1)
  - [817bbbb7749d ("ARM: qcom_defconfig: add support for USB networking")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=817bbbb7749decb99262dc3bb1569a579eea5ba8)

  ![USB OTG](images/usb-otg.png?raw=1)

- <a id="vibrator"></a>Add support for clock-based vibrator devices where the speed can be
  controlled by changing the duty cycle. Use
  [rumble-test.c](https://git.collabora.com/cgit/user/sre/rumble-test.git/plain/rumble-test.c) to
  test the driver.

  - [0f681d09e66e ("Input: add new vibrator driver for various MSM SOCs")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=0f681d09e66ea6833e6173180ff3892e9026ab71)
  - *Needs work*: [clk: qcom: add support for setting the duty cycle](https://lore.kernel.org/lkml/20191205002503.13088-2-masneyb@onstation.org/)
  - *Needs work*: [dt-bindings: Input: drop msm-vibrator in favor of clk-vibrator](https://lore.kernel.org/lkml/20191205002503.13088-3-masneyb@onstation.org/)
  - *Needs work*: [Input: drop msm-vibrator in favor of clk-vibrator driver](https://lore.kernel.org/lkml/20191205002503.13088-4-masneyb@onstation.org/)
  - *Needs work*: [dt-bindings: Input: introduce new clock vibrator bindings](https://lore.kernel.org/lkml/20191205002503.13088-5-masneyb@onstation.org/)
  - *Needs work*: [Input: introduce new clock vibrator driver](https://lore.kernel.org/lkml/20191205002503.13088-6-masneyb@onstation.org/)
  - *Needs work*: [ARM: qcom_defconfig: drop msm-vibrator in favor of clk-vibrator driver](https://lore.kernel.org/lkml/20191205002503.13088-7-masneyb@onstation.org/)
  - *Needs work*: [ARM: dts: qcom: msm8974-hammerhead: add support for vibrator](https://lore.kernel.org/lkml/20191205002503.13088-8-masneyb@onstation.org/)

- <a id="iommu"></a>Work in progress patches to get the IOMMU working.

  - *Needs work*: [iommu/qcom: fix NULL pointer dereference during probe deferral](https://lore.kernel.org/lkml/20200104002024.37335-1-masneyb@onstation.org/)
  - *Needs work*: [ARM: dts: qcom: msm8974: add mdp5 iommu support](https://lore.kernel.org/lkml/20200109002606.35653-1-masneyb@onstation.org/)

- <a id="various-i2c-sensors"></a>The
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

- <a id="panel"></a>The panel is supported by the simple-panel driver upstream.

  - [9e0b597534b4 ("dt-bindings: drm/panel: simple: add lg,acx467akm-7 panel")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=9e0b597534b4c065e2c083c7478d6f3175088fdd)
  - [debcd8f954be ("drm/panel: simple: add lg,acx467akm-7 panel")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=debcd8f954be2b1f643e76b2400bc7c3d12b4594)

- <a id="wifi"></a>WiFi - The phone has a
  [Broadcom (now Cypress) 4339](http://www.cypress.com/file/298016/download) for wireless.

  - [ec4c6c57af57 ("ARM: dts: qcom: msm8974-hammerhead: add WiFi support")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=ec4c6c57af576e10c70547b782db04eb3602f5f4)
  - <a id="bisect-wifi"></a>[Bisected an issue in 5.2rc1](https://lore.kernel.org/lkml/20190524111053.12228-1-masneyb@onstation.org/)
    that caused WiFi to stop working. This issue was fixed by the patch
    [89f3c365f3e1 ("mmc: sdhci: Fix SDIO IRQ thread deadlock")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=89f3c365f3e113d087f105c3acbbb5a71eee84e3).

- <a id="touchscreen"></a>Touchscreen is supported by the Synaptics RMI4 driver.

  - [48100d10c93f ("ARM: dts: qcom: msm8974-hammerhead: add touchscreen support")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=48100d10c93fe3df6e1f4ea77888985d054f25d8)

- <a id="sdhci"></a>Flash memory

  - [03864e57770a ("ARM: dts: qcom: msm8974-hammerhead: increase load on l20 for sdhci")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=03864e57770a9541e7ff3990bacf2d9a2fffcd5d) -
    Corrects an issue where the phone would not boot properly when starting to read from the flash
    memory.
  - <a id="bisect-regulator"></a>[Bisected an issue in linux-next](https://lore.kernel.org/lkml/20181125093750.GA28055@basecamp/)
    related to a change in the regulator framework that caused the the phone to no longer boot. The
    issue was resolved by commit
    [fa94e48e13a1a ("regulator: core: Apply system load even if no consumer loads"](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=fa94e48e13a1).

- [acd92c5a1149 ("ARM: qcom_defconfig: add options for LG Nexus 5 phone")](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=acd92c5a11493bdf137aba6e21e865331d7d90d7)

## Other resources

- [TODO list](TODO.md) for upstreaming the various major components.
- My [linux branches](https://github.com/masneyb/linux/branches) that include some of my in progress
  and out-of-tree patches.
- A full teardown of the Nexus 5 is
  [available on ifixit](https://www.ifixit.com/Teardown/Nexus+5+Teardown/19016).
- [Downstream MSM 3.4 kernel sources](https://github.com/AICP/kernel_lge_hammerhead) with additions
   from the community. Use hammerhead_defconfig when building this kernel.
- [postmarketOS](https://postmarketos.org/) for the
  [Nexus 5](https://wiki.postmarketos.org/wiki/Google_Nexus_5_(lg-hammerhead))
- [Sep 2019: Linaro Connect San Diego: Status update on Qualcomm upstreaming](https://connect.linaro.org/resources/san19/san19-119/)
- [Aug 2019: Mainline status update for the Nexus 5 phone (qcom msm8974 SoC)](https://lkml.org/lkml/2019/8/4/164)
- [June 2019: Two years of postmarketOS](https://postmarketos.org/blog/2019/06/23/two-years/) blog post.

## Contact

Brian Masney: [Email](mailto:masneyb@onstation.org), [Linked In](https://www.linkedin.com/in/brian-masney/), [GitHub](https://github.com/masneyb)
