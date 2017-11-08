# reset-usbstick
Reset your USB-Stick (or other block device) without reconnecting it physically.

Therefore the block device is deleted using the **sysfs**. After that, the
corresponding **scsi** host is doing a rescan.

Note, that this procedure does not perform a *Power-On-Reset*, the usb power 
supply can not be disconnected unless the usb device is disconnected 
physically. However, the device is rediscovered by
the Linux kernel after such a **soft** reset, i.e. in many cases, where one 
would need to pull the device from the usb connector, and reconnect it, the
same effect can be achieved by this script.

To specify the block device, either use its serial number (**-s xyz123**) or 
use its device name given by the linux kernel (**-d /dev/sdx**). You can list 
all serial numbers for connected block devices (**-l**).

 usage: reset-usbstick.py [-h] [-s SERIAL_NUMBER] [-d DEVICE_NAME] [-l]

arguments:
*  -h, --help            show this help message and exit
*  -s SERIAL_NUMBER, --by-serial-number SERIAL_NUMBER use serial number to specify the device
*  -d DEVICE_NAME, --by-device-name DEVICE_NAME use device name (like sdx) to specify the device
*  -l, --list-serial-numbers list all block devices with corresponding serial numbers

