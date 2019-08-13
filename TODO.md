Here's a list in no particular order of various TODO items to get the major phone components
working upstream. Please [let me know](mailto:masneyb@onstation.org) (or send a pull request) if you
have any updates to this list. Feel free to pick up an item on this list if you're interested.

- GPU - I'm currently working on upstreaming the various bits to support the GPU upstream. See the
  [linux repository on my GitHub account](https://github.com/masneyb/linux/branches) for the
  current work in progress. Needs OCMEM driver, msm8974 Interconnect driver, and IOMMU support.
- Slimbus to support showing the phone screen on an external TV / monitor. There is now Qualcomm
  code in the
  [slimbus subsystem upstream](https://git.kernel.org/pub/scm/linux/kernel/git/qcom/linux.git/tree/drivers/slimbus).
  Does this just require adding the nodes to device tree in msm8974.dtsi?
- Front and back camera - Appears to be supported by out-of-tree patch set for the
  [Qualcomm Camera Control Interface](https://patchwork.ozlabs.org/cover/825398/). This will likely
  require the OCMEM and Interconnect support as well based on the downstream code.
- Audio - Also requires OCMEM and Interconnect support based on downstream code.
- Modem
- GPS - Patch for gpsd is in [this tree](https://github.com/andersson/gpsd/commits/master) for the
  Qualcomm PDS service support. Start gpsd with `sudo gpsd -N -D9 -F /var/run/gpsd.sock` and
  connect to it with `sudo gpsdctl add pds://any`, and test with `sudo gpsmon`.
- The rear flashlight is supported in the downstream Linux kernel with the
  [drivers/leds/leds-qpnp.c](https://github.com/AICP/kernel_lge_hammerhead/blob/n7.1/drivers/leds/leds-qpnp.c)
  driver and referred to as torch in that code. Likely requires a new driver upstream.
- The front LED appears to be supported by an out-of-tree patch with the
  [Qualcomm Light Pulse Generator (LPG) driver](https://lkml.org/lkml/2017/11/15/26).
- Battery - Appears to be supported by the
  [Maxim ModelGauge ICs gauge driver](https://lore.kernel.org/patchwork/patch/437579/). Look at the
  [PM8941 Battery Monitoring System](https://lore.kernel.org/lkml/20180614151435.6471-2-ctatlor97@gmail.com/)
  as well.
- Bluetooth - I have some work in progress patches towards this.
- CPUFreq support for msm8974. See [this message](https://lore.kernel.org/lkml/20190812152826.GA7958@centauri/)
  for more details. The referenced patch in linux-next is titled
  'cpufreq: qcom: Re-organise kryo cpufreq to use it for other nvmem based qcom socs'.

## Driver improvements

- lm3630a backlight - Move the config structures out of include/linux/platform_data since there
  are no in-tree users and require device tree instead.
- tsl2772 ALS / proximity sensor - runtime power management. I have a work in progress patch for
  this. Need to investigate how to support this when interrupt thesholds are configured.
- Check other IIO devices supported by this board to see if runtime power management is present.

[Back to main page](README.md)
