
import ctypes
import fcntl

from v4l2py import raw


class MediaDeviceInfo(ctypes.Structure):
    _fields_ = [
        ("driver", ctypes.c_char * 16),
        ("model", ctypes.c_char * 32),
        ("serial", ctypes.c_char * 40),
        ("bus_info", ctypes.c_char * 32),
        ("media_version", ctypes.c_uint32),
        ("hw_revision", ctypes.c_uint32),
        ("driver_version", ctypes.c_uint32),
        ("reserved", ctypes.c_uint32 * 31),
    ]

VIDIOC_DEVICE_INFO = raw._IOWR('|', 0x00, MediaDeviceInfo)


def get_device_controls(fd):
    # original enumeration method
    media_info = MediaDeviceInfo()

    try:

        fcntl.ioctl(fd, VIDIOC_DEVICE_INFO, media_info)
        print("\t",media_info.driver)
        print("\t",media_info.model)
        print("\t",media_info.serial)
        print("\t",media_info.bus_info)
    except IOError as e:
        print(e)

for i in range(4):
    with open('/dev/media%d' % i) as file:
        print("try .. ", i)
        get_device_controls(file)
