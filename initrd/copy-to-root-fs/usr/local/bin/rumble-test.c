/* very simple test tool for vibrator strength
 *
 * License: LGPL 2.1
 * Copyright: Collabora Ltd.
 * Author: Sebastian Reichel <sebastian.reichel@collabora.co.uk>
 *
 */

#include <stdio.h>
#include <sys/ioctl.h>
#include <linux/input.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdlib.h>
#include <errno.h>

int main(int argc, char **argv) {
	const char * device_file_name;
	unsigned int strength;

	struct input_event event = {
		.type = EV_FF,
	};
	struct ff_effect effect = {
		.type = FF_RUMBLE,
		.id = -1,
		.u.rumble.strong_magnitude = 0x0000,
		.u.rumble.weak_magnitude = 0x0000,
		.replay.length = 5000,
		.replay.delay = 1000,
	};
	int fd, err;

	if (argc != 3) {
		fprintf(stderr, "%s /dev/input/event<num> <strength>\n", argv[0]);
		return 1;
	}

	device_file_name = argv[1];
	strength = strtol(argv[2], NULL, 0);

	fd = open(device_file_name, O_RDWR);
	if (fd == -1) {
		fprintf(stderr, "could not open %s: %d\n", device_file_name, errno);
		return 1;
	}

	effect.u.rumble.strong_magnitude = strength;

	printf("Upload rumble effect... ");
	fflush(stdout);

	err = ioctl(fd, EVIOCSFF, &effect);
	if (err == -1) {
		printf("failed\n");
		fprintf(stderr, "ioctl error: %d\n", errno);
		return 1;
	}
	printf("id=%d\n", effect.id);

	event.code = effect.id;
	event.value = 1;

	err = write(fd, (const void*) &event, sizeof(event));
	if (err == -1) {
		fprintf(stderr, "failed to start rumble effect (err=%d)\n", errno);
		return 1;
	}

	sleep(5);

	event.value = 0;

	err = write(fd, (const void*) &event, sizeof(event));
	if (err == -1) {
		fprintf(stderr, "failed to stop rumble effect (err=%d)\n", errno);
		return 1;
	}

	return 0;
}

