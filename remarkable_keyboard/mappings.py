import logging
from pynput.keyboard import Key
from pynput.mouse import Button
from pynput._util.xorg import X11Error
from sortedcontainers import SortedDict

log = logging.getLogger(__name__)

class Mapping(object):
    def __init__(self, m, k):
        self.m = m
        self.k = k

    def action(self, key, release=True, reset_modifiers=True):
        """Returns action function to be called on a touch"""
        def action():
            # FIXME: upstream pynput bug, caps_lock raises exception if mapped to mod key
            try:
                self.k.press(key)
                if release:
                    self.k.release(key)
                if reset_modifiers:
                    self.k.release(Key.shift)
                    self.k.release(Key.ctrl)
                    self.k.release(Key.alt)
                    self.k.release(Key.shift_r)
                    self.k.release(Key.ctrl_r)
                    self.k.release(Key.alt_r)
            except X11Error:
                log.error(f"X11Error for key {key}")

        return action

    def call_action(self, x, y):
        """Look up coordinate in table and call action"""
        regions = self.regions()
        row_index = regions.bisect(y)
        # FIXME: should be a cleaner way to limit row_index to valid indices
        row_index = row_index if row_index < len(regions) else len(regions) - 1
        row = regions[regions.keys()[row_index]]
        col_index = row.bisect(x)
        # FIXME: should be a cleaner way to limit col_index to valid indices
        col_index = col_index if col_index < len(row) else len(row) - 1
        # call function
        row[row.keys()[col_index]]()

class ExampleMapping(Mapping):
    """Example mapping

           +--- x
           |
           |  +-------------------+-+   ---
           y  |         |         |o|    |
              |    a    |    b    | |    |
              |---------+---------|o|  1404
              |         |         | |    |
              |    c    |    d    |o|    |
              +-------------------+-+   ---

              |-------1872--------|

    Coordinates defined in terms of image size: 1872 x 1404
    """
    def regions(self):
        return SortedDict({
            1404 // 2: SortedDict({
                1872 // 2: lambda: self.k.type('a'),
                1872: lambda: self.k.type('b')
            }),
            1404: SortedDict({
                1872 // 2: lambda: self.k.type('c'),
                1872: lambda: self.k.type('d')
            })
        })


class KeyboardMapping(Mapping):

    def regions(self):
        return SortedDict({
            260: SortedDict({
                1499: lambda: self.m.click(Button.left),
                1872: lambda: self.m.scroll(0, 1)
            }),
            519: SortedDict({
                1499: lambda: self.m.click(Button.left),
                1872: lambda: self.m.scroll(0, -1)
            }),
            779: SortedDict({
                1499: lambda: self.m.click(Button.left),
                1872: lambda: self.m.click(Button.right)
            }),
            903: SortedDict({
                126: self.action('`'),
                251: self.action('1'),
                376: self.action('2'),
                500: self.action('3'),
                625: self.action('4'),
                750: self.action('5'),
                874: self.action('6'),
                1000: self.action('7'),
                1125: self.action('8'),
                1249: self.action('9'),
                1374: self.action('0'),
                1499: self.action('-'),
                1623: self.action('='),
                1872: self.action(Key.backspace)
            }),
            1028: SortedDict({
                188: self.action(Key.tab),
                314: self.action('q'),
                438: self.action('w'),
                563: self.action('e'),
                688: self.action('r'),
                813: self.action('t'),
                937: self.action('y'),
                1062: self.action('u'),
                1187: self.action('i'),
                1312: self.action('o'),
                1436: self.action('p'),
                1561: self.action('{'),
                1686: self.action('}'),
                1872: self.action('|')
            }),
            1153: SortedDict({
                220: self.action(Key.caps_lock, release=False),
                345: self.action('a'),
                470: self.action('s'),
                594: self.action('d'),
                719: self.action('f'),
                844: self.action('g'),
                968: self.action('h'),
                1093: self.action('j'),
                1218: self.action('k'),
                1343: self.action('l'),
                1468: self.action(';'),
                1598: self.action('\''),
                1872: self.action(Key.enter)
            }),
            1278: SortedDict({
                282: self.action(Key.shift, release=False, reset_modifiers=False),
                407: self.action('z'),
                531: self.action('x'),
                657: self.action('c'),
                781: self.action('v'),
                906: self.action('b'),
                1031: self.action('n'),
                1155: self.action('m'),
                1280: self.action(','),
                1405: self.action('.'),
                1530: self.action('/'),
                1872: self.action(Key.shift_r, release=False, reset_modifiers=False)
            }),
            1404: SortedDict({
                188: self.action(Key.ctrl, release=False, reset_modifiers=False),
                313: self.action(Key.cmd),
                500: self.action(Key.alt, release=False, reset_modifiers=False),
                1250: self.action(Key.space),
                1374: self.action(Key.esc),
                1499: self.action(Key.left),
                1623: self.action(Key.down),
                1747: self.action(Key.up),
                1872: self.action(Key.right)
            }),
        })
