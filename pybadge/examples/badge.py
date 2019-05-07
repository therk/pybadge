from micropython import const
import board
import busio
import time
import digitalio
import gamepad
import struct


_GAMMA = (b"\x00\x01\x02\x03\x05\x08\x0c\x10\x18\x20\x36\x4f\x60\x7f\xbf\xff")
_FONT = (
        b'\xff\xff\xff\xff\xff\xff\xf3\xf3\xf7\xfb\xf3\xff\xcc\xdd\xee\xff\xff'
        b'\xff\xdd\x80\xdd\x80\xdd\xff\xf7\x81\xe4\xc6\xd0\xf7\xcc\xdb\xf3\xf9'
        b'\xcc\xff\xf6\xcdc\xdcf\xff\xf3\xf7\xfe\xff\xff\xff\xf6\xfd\xfc\xfd'
        b'\xf6\xff\xe7\xdf\xcf\xdf\xe7\xff\xff\xd9\xe2\xd9\xff\xff\xff\xf3\xc0'
        b'\xf3\xff\xff\xff\xff\xff\xf3\xf7\xfe\xff\xff\x80\xff\xff\xff\xff\xff'
        b'\xff\xff\xf3\xff\xcf\xdb\xf3\xf9\xfc\xff\xd2\xcd\xc8\xdc\xe1\xff\xf7'
        b'\xf1\xf3\xf3\xe2\xff\xe1\xce\xe3\xfd\xc0\xff\xe1\xce\xe3\xce\xe1\xff'
        b'\xf3\xf9\xdc\xc0\xcf\xff\xc0\xfc\xe4\xcf\xe1\xff\xd2\xfc\xe1\xcc\xe2'
        b'\xff\xc0\xdb\xf3\xf9\xfc\xff\xe2\xcc\xe2\xcc\xe2\xff\xe2\xcc\xd2\xcf'
        b'\xe1\xff\xff\xf3\xff\xf3\xff\xff\xff\xf3\xff\xf3\xf7\xfe\xcf\xf3\xfc'
        b'\xf3\xcf\xff\xff\xc0\xff\xc0\xff\xff\xfc\xf3\xcf\xf3\xfc\xff\xe1\xcf'
        b'\xe3\xfb\xf3\xff\xe2\xcd\xc4\xd4\xbd\xd2\xe2\xdd\xcc\xc4\xcc\xff\xe4'
        b'\xcc\xe4\xcc\xe4\xff\xe2\xcd\xfc\xcd\xe2\xff\xe4\xdc\xcc\xdc\xe4\xff'
        b'\xd0\xfc\xf4\xfc\xd0\xff\xd0\xfc\xfc\xf4\xfc\xff\xd2\xfd\xfc\x8d\xd2'
        b'\xff\xcc\xcc\xc4\xcc\xcc\xff\xd1\xf3\xf3\xf3\xd1\xff\xcb\xcf\xcf\xdc'
        b'\xe2\xff\xdc\xcc\xd8\xf4\xc8\xff\xfc\xfc\xfc\xec\xc0\xff\xdd\xc4\xc0'
        b'\xc8\xcc\xff\xcd\xd4\xd1\xc5\xdc\xff\xe2\xdd\xcc\xdd\xe2\xff\xe4\xcc'
        b'\xcc\xe4\xfc\xff\xe2\xcc\xcc\xc8\xd2\xcf\xe4\xcc\xcc\xe0\xcc\xff\xd2'
        b'\xec\xe2\xce\xe1\xff\xc0\xe2\xf3\xf3\xf3\xff\xcc\xcc\xcc\xdd\xe2\xff'
        b'\xcc\xcc\xdd\xe6\xf3\xff\xcc\xc8\xc4\xc0\xd9\xff\xcc\xd9\xe2\xd9\xcc'
        b'\xff\xcc\xdd\xe6\xf3\xf3\xff\xc0\xde\xf7\xed\xc0\xff\xd0\xfc\xfc\xfc'
        b'\xd0\xff\xfc\xf9\xf3\xdb\xcf\xff\xc1\xcf\xcf\xcf\xc1\xff\xf3\xd9\xee'
        b'\xff\xff\xff\xff\xff\xff\xff\x80\xff\xfc\xf7\xef\xff\xff\xff\xff\xd2'
        b'\xcd\xcc\x86\xff\xfc\xe4\xdc\xcc\xe4\xff\xff\xd2\xfd\xbc\xc6\xff\xcf'
        b'\xc6\xcd\xcc\x86\xff\xff\xd6\xcd\xb1\xd2\xff\xcb\xb7\xc1\xf3\xf3\xf6'
        b'\xff\xe2\xcc\xd2\xdf\xe1\xfc\xe4\xdc\xcc\xcc\xff\xf3\xfb\xf1\xb3\xdb'
        b'\xff\xcf\xef\xc7\xcf\xdd\xe2\xfd\xec\xd8\xf4\xcc\xff\xf6\xf3\xf3\xf3'
        b'\xdb\xff\xff\xd9\xc4\xc8\xcc\xff\xff\xe4\xdd\xcc\xcc\xff\xff\xe2\xcc'
        b'\xcc\xe2\xff\xff\xe4\xdc\xcc\xe4\xfc\xff\xc6\xcd\xcc\xc6\xcf\xff\xc9'
        b'\xf4\xfc\xfc\xff\xff\xd2\xf8\xcb\xe1\xff\xf3\xd1\xf3\xb3\xdb\xff\xff'
        b'\xcc\xcc\xcd\x82\xff\xff\xcc\xdd\xe6\xf3\xff\xff\xcc\xc8\xd1\xd9\xff'
        b'\xff\xcc\xe6\xe6\xcc\xff\xff\xdc\xcd\xd2\xcf\xe1\xff\xc0\xdb\xf9\xc0'
        b'\xff\xd3\xf3\xf9\xf3\xd3\xff\xf3\xf3\xf7\xf3\xf3\xff\xf1\xf3\xdb\xf3'
        b'\xf1\xff\xbfr\x8d\xfe\xff\xfff\x99f\x99f\x99')


K_X = const(0x01)
K_DOWN = const(0x02)
K_LEFT = const(0x04)
K_RIGHT = const(0x08)
K_UP = const(0x10)
K_O = const(0x20)
K_S = const(0x40)
K_Z = const(0x80)

_i2c = None
_page = None
_buffer = bytearray(17)
_ROWS = b'\x05\x06\x04\x07\x03\x08\x09\x02\x0a\x01\x00'
_COLS = (b'\x06\x07\x05\x03\x01\x04\x02'
         b'\x0f\x10\x0e\x0c\x0a\x0d\x0b')


def brightness(level):
    level = min(255, max(0, level * 16 + 16))
    _matrix_write(0x03, 0x01, level)


def show(pix):
    buffer = pix.buffer
    width = pix.width
    _matrix_write(0x01, 0x00)
    for y, row in enumerate(_ROWS):
        for x, col in enumerate(_COLS):
            _buffer[col] = _GAMMA[min(15, max(0, buffer[x + y * width]))]
        _buffer[0] = row * 16
        _i2c.writeto(0x50, _buffer)


def tick(delay):
    global _tick

    _tick += delay
    time.sleep(max(0, _tick - time.monotonic()))


class Pix:
    def __init__(self, width=14, height=11, buffer=None):
        if buffer is None:
            buffer = bytearray(width * height)
        self.buffer = buffer
        self.width = width
        self.height = height

    @classmethod
    def from_text(cls, string, color=None, bgcolor=0, colors=None):
        width = 4 * len(string)
        pix = cls(width, 6)
        buffer = pix.buffer
        font = memoryview(_FONT)
        if colors is None:
            if color is None:
                colors = (15, 8, 2, bgcolor)
            else:
                colors = (color, color, bgcolor, bgcolor)
        x = 0
        for c in string:
            index = ord(c) - 0x20
            if not 0 <= index <= 95:
                continue
            row = 0
            for byte in font[index * 6:index * 6 + 6]:
                for col in range(4):
                    buffer[x + col + row * width] = colors[byte & 0x03]
                    byte >>= 2
                row += 1
            x += 4
        return pix

    @classmethod
    def from_string(cls, string):
        lines = string.strip().split('\n')
        width = max(len(l) for l in lines)
        pix = cls(width, len(lines))
        buffer = pix.buffer
        for y, line in enumerate(lines):
            index = y * width
            for c in line:
                buffer[index] = int(c, 16)
                index += 1
        return pix

    def pixel(self, x, y, color=None):
        if not 0 <= x < self.width or not 0 <= y < self.height:
            return 0
        if color is None:
            return self.buffer[x + y * self.width]
        self.buffer[x + y * self.width] = int(color)

    def box(self, color, x=0, y=0, width=None, height=None):
        x = min(max(x, 0), self.width - 1)
        y = min(max(y, 0), self.height - 1)
        width = max(0, min(width or self.width, self.width - x))
        height = max(0, min(height or self.height, self.height - y))
        for y in range(y, y + height):
            index = y * self.width + x
            for i in range(width):
                self.buffer[index] = color
                index += 1

    def blit(self, source, dx=0, dy=0, x=0, y=0,
             width=None, height=None, key=None):
        if dx < 0:
            x -= dx
            dx = 0
        if x < 0:
            dx -= x
            x = 0
        if dy < 0:
            y -= dy
            dy = 0
        if y < 0:
            dy -= y
            y = 0
        width = min(min(width or source.width, source.width - x),
                    self.width - dx)
        height = min(min(height or source.height, source.height - y),
                     self.height - dy)
        source_buffer = memoryview(source.buffer)
        self_buffer = self.buffer
        if key is None:
            for row in range(height):
                xx = y * source.width + x
                dxx = dy * self.width + dx
                self_buffer[dxx:dxx + width] = source_buffer[xx:xx + width]
                y += 1
                dy += 1
        else:
            for row in range(height):
                xx = y * source.width + x
                dxx = dy * self.width + dx
                for col in range(width):
                    color = source_buffer[xx]
                    if color != key:
                        self_buffer[dxx] = color
                    dxx += 1
                    xx += 1
                y += 1
                dy += 1

    def __str__(self):
        return "\n".join(
            "".join(
                hex(self.pixel(x, y))[-1]
                for x in range(self.width)
            )
            for y in range(self.height)
        )


def _matrix_write(page, register, value=None):
    global _page

    if page != _page:
        _buffer[0] = 0xfe
        _buffer[1] = 0xc5
        _i2c.writeto(0x50, _buffer, end=2)
        _buffer[0] = 0xfd
        _buffer[1] = page
        _i2c.writeto(0x50, _buffer, end=2)
        _page = page
    if value is not None:
        _buffer[0] = register
        _buffer[1] = value
        _i2c.writeto(0x50, _buffer, end=2)


def _accel_write(register, value):
    _buffer[0] = register
    _buffer[1] = value
    _i2c.writeto(0x18, _buffer, end=2)


def accel():
    _buffer[0] = 0xa8
    _i2c.writeto(0x18, _buffer, end=1, stop=False)
    _i2c.readfrom_into(0x18, _buffer, end=6)
    x, y, z = struct.unpack_from('<hhh', _buffer)
    return x, -y, -z


def init():
    global _i2c, _tick, _page, keys

    if _i2c is not None:
        return

    _i2c = busio.I2C(sda=board.SDA, scl=board.SCL, frequency=600000)
    _i2c.try_lock()
    _tick = time.monotonic()

    _matrix_write(0x03, 0x00, 0x03)
    _matrix_write(0x00, 0x00)
    _i2c.writeto(0x50, b'\x00\x7f\xfe\x7f\xfe\x7f\xfe\x7f\xfe\x7f\xfe'
                 b'\x7f\xfe\x7f\xfe\x7f\xfe\x7f\xfe\x7f\xfe\x7f\xfe')

    #_accel_write(0x24, 0x80)  # reboot
    #time.sleep(0.005)
    _accel_write(0x20, 0x37)  # enable, data rate 400Hz
    _accel_write(0x23, 0x88)  # HiRes & BDU
    _accel_write(0x1f, 0x80)  # ADCs

    keys = gamepad.GamePad(
        digitalio.DigitalInOut(board.X),
        digitalio.DigitalInOut(board.DOWN),
        digitalio.DigitalInOut(board.LEFT),
        digitalio.DigitalInOut(board.RIGHT),
        digitalio.DigitalInOut(board.UP),
        digitalio.DigitalInOut(board.O),
        digitalio.DigitalInOut(board.S),
        digitalio.DigitalInOut(board.Z),
    ).get_pressed

    brightness(7)
