#!/bin/env python
# Evan Widloski - 2019-02-23
# Use reMarkable as mouse input

import argparse
import logging
import os
import sys
import struct
from getpass import getpass
import paramiko
from screeninfo import get_monitors
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController
from remarkable_mouse.remarkable_mouse import open_eventfile
from remarkable_keyboard.mappings import KeyboardMapping


# evdev codes
e_type_abs = 3
e_code_finger_xpos = 53
e_code_finger_ypos = 54
e_code_finger_pressure = 58
e_code_finger_touch = 57
e_value_finger_up = -1

# resolution of reMarkable touchscreen
finger_width = 1023
finger_height = 767

# resolution of reMarkable display
image_width = 1872
image_height = 1404

mouse = MouseController()
keyboard = KeyboardController()

# table of image coordinates and actions
mapping = KeyboardMapping(mouse, keyboard)

log = logging.getLogger(__name__)

# remap finger coordinates to standard basis
def map_finger(x, y, orig_width, orig_height, map_width, map_height):
    """Map touchscreen coordinates to new axes


    reMarkable is assumed to be laying horizontally on left edge.

    Finger coordinate axes      Mapped coordinate axes
     x ---+                     +--- x
          |                     |
          |                     |
          y                     y


    Coordinates are mapped so that the entire desktop screen fits onto reMarkable


           Monitor wider than reMarkable    Monitor narrower than remarkable

       ---    +-------------------+-+          +-------------------+-+
        |     |                   |o|          |   MMMMMMMMMMMMM   |o|
        |     |MMMMMMMMMMMMMMMMMMM| |          |   MMMMMMMMMMMMM   | |
      height  |MMMMMMMMMMMMMMMMMMM|o|          |   MMMMMMMMMMMMM   |o|
        |     |MMMMMMMMMMMMMMMMMMM| |          |   MMMMMMMMMMMMM   | |
        |     |                   |o|          |   MMMMMMMMMMMMM   |o|
       ---    +-------------------+-+          +-------------------+-+

              |----- width -------|

                             M = monitor mapped area
    """

    x = orig_width - x

    ratio_width, ratio_height = map_width / orig_width, map_height / orig_height
    scaling = ratio_width if ratio_width > ratio_height else ratio_height

    return (
        scaling * (x - (orig_width - map_width / scaling) / 2),
        scaling * (y - (orig_height - map_height / scaling) / 2)
    )


def read_tablet(args):
    """Loop forever and map evdev events to mouse"""

    last_x = last_y = None
    start_x = start_y = x = y = 0
    moves = 0

    monitor = get_monitors()[0]
    log.debug('Chose monitor: {}'.format(monitor))

    stdout = open_eventfile(args, file='/dev/input/event1')

    while True:
        _, _, e_type, e_code, e_value = struct.unpack('2IHHi', stdout.read(16))

        if e_type == e_type_abs:

            # handle x direction (rotated)
            if e_code == e_code_finger_ypos:
                log.debug(f'{e_value}')
                x = e_value
                monitor_x, monitor_y = map_finger(
                    x, y,
                    finger_width, finger_height,
                    monitor.width, monitor.height
                )
                # use relative movement instead of absolute position
                # (like a trackpad)
                if last_x is not None:
                    mouse.move(monitor_x - last_x, 0)
                    moves += 1
                else:
                    start_x = x
                last_x = monitor_x

            # handle y direction (rotated)
            elif e_code == e_code_finger_xpos:
                log.debug(f'\t{e_value}')
                y = e_value
                monitor_x, monitor_y = map_finger(
                    x, y,
                    finger_width, finger_height,
                    monitor.width, monitor.height
                )
                # use relative movement instead of absolute position
                # (like a trackpad)
                if last_y is not None:
                    mouse.move(0, monitor_y - last_y)
                    moves += 1
                else:
                    start_y = y
                last_y = monitor_y

            # handle pressure
            elif e_code == e_code_finger_pressure:
                log.debug(f'\t\t{e_value}')
                pass

            # handle finger lift
            elif e_code == e_code_finger_touch:
                if e_value == e_value_finger_up:
                    log.debug('\t\t\tfinger up')
                    last_x = None
                    last_y = None
                    log.debug(f"start position: {start_x} {start_y}")
                    # FIXME: I have no freaking idea why, but the keyboard lags slightly unless
                    # we print something to console here
                    print(' \r', end='')
                    # if the mouse hasn't moved much since the last finger lift, assume it was a touch
                    if moves < 8:
                        log.debug(f"touch, moves:{moves}")
                        image_x, image_y = map_finger(
                            start_x, start_y,
                            finger_width, finger_height,
                            image_width, image_height
                        )
                        mapping.call_action(image_x, image_y)
                    else:
                        log.debug(f"drag, moves:{moves}")

                    moves = 0

def main():

    try:
        parser = argparse.ArgumentParser(description="use reMarkable tablet as wireless mouse and keyboard")
        parser.add_argument('--debug', action='store_true', default=False, help="enable debug messages")
        parser.add_argument('--key', type=str, metavar='PATH', help="ssh private key")
        parser.add_argument('--password', default=None, type=str, help="ssh password")
        parser.add_argument('--address', default='10.11.99.1', type=str, help="device address")

        args = parser.parse_args()

        if args.debug:
            print('Debugging enabled...')
            logging.getLogger('').setLevel(logging.DEBUG)
            log.setLevel(logging.DEBUG)

        read_tablet(args)
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
