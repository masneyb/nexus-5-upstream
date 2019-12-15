rumble()
{
	echo "Sending rumble $1"
	/usr/local/bin/rumble-test /dev/input/by-path/platform-vibrator-event $1
}

rumble 0x0000
rumble 0x1111
rumble 0x2222
rumble 0x3333
rumble 0x4444
rumble 0x5555
rumble 0x6666
rumble 0x7777
rumble 0x8888
rumble 0x9999
rumble 0xaaaa
rumble 0xbbbb
rumble 0xcccc
rumble 0xdddd
rumble 0xeeee
rumble 0xffff
