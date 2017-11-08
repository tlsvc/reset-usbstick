#!/usr/bin/python3

from subprocess import Popen,PIPE
import re
import os
import sys
import argparse

#def get_
testserial = "AA6271022J4000001492"

def get_properties(path):# {{{
    cmd = "udevadm info --query=property --path=%s" % path
    handle = Popen(cmd.split(),stdout=PIPE)
    text = handle.stdout.read().decode().strip("\n")
    lines = text.split("\n")
    iterable = (l.split("=") for l in lines)
    return dict(iterable)
# }}}
def find_block_devices():# {{{
    folder = "/sys/block"
    patterns = ["^sd[a-z]+$","^mmcblk[a-z]+$"]
    block_devices = []
    devices = os.listdir(folder)
    for dev in devices:
        for p in patterns:
            m = re.match(p,dev)
            if m:
                s = m.group(0)
                block_devices.append(os.path.join(folder,s))
    return block_devices
# }}}
def find_block_device_by_attr(attr,value,block_devices):# {{{
    matching_devices = []
    for dev in block_devices:
        prop = get_properties(dev)
        try:
            v = prop[attr]
        except KeyError: # attribute does not exist -> choose other one!
            return -1
        if v == value:
            matching_devices.append(dev)
        else:
            pass
    return matching_devices
            # }}}
def show_block_device_with_attributes(attrs,block_devices):# {{{
    for dev in block_devices:
        prop = get_properties(dev)
        print("%s:" % dev)
        for a in attrs:
            try:
                v = prop[a]
                print("%s=%s" % (a,v))
            except KeyError: # attribute does not exist -> choose other one!
                print("Attribute %s not available." % a)
        print()
    return
# }}}

def get_sdx(devname_input):# {{{
    l = devname_input.split("/")
    #...
    return l[-1]
# }}}
def delete_blockdev(blockdev):# {{{
    try:
        fh = open(os.path.join(blockdev,"device/delete"),"w")
    except PermissionError:
        print("Error: no permission to delete block device %s" % blockdev)
        sys.exit(42)
    except:
        print("Error: deleting block device %s" % blockdev)
        sys.exit(2)
    fh.write("1")
    fh.close()
    return
# }}}
def rescan_lhost(lhost):# {{{
    try:
        fh = open(os.path.join("/sys/class/scsi_host/",lhost,"scan"),"w")
    except PermissionError:
        print("Error: no permission to rescan scsi_host %s" % lhost)
        sys.exit(42)
    except:
        print("Error: rescanning scsi_host %s", lhost)
        sys.exit(3)
    fh.write("- - -")
    fh.close()
    return
# }}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Reset block devices like USB-Sticks, without reconnecting it physically.')
    parser.add_argument("-s","--by-serial-number",
                        dest = "serial_number",
                        help = "use serial number to specify the device")
    parser.add_argument("-d","--by-device-name",
                        dest = "device_name",
                        help = "use device name (like sdx) to specify the device")
    parser.add_argument("-l","--list-serial-numbers",
                        action ="store_true",
                        help="list all block devices with corresponding serial numbers")
    args = parser.parse_args()

    block_devices = find_block_devices()
    if args.serial_number:
        matches = find_block_device_by_attr("ID_SERIAL_SHORT", args.serial_number, block_devices)
        if len(matches) == 0:
            print("No matching device.")
            sys.exit(42)
        if len(matches) == 1:
            match = matches[0]

            link = os.readlink(match)
            m = re.match(".*(host\d+).*",link)
            lhost = m.group(1)
            delete_blockdev(match)
            rescan_lhost(lhost)

    elif args.device_name:
        sdx = get_sdx(args.device_name)
        match = "/sys/block/%s" % sdx

        try:
            link = os.readlink(match)
        except FileNotFoundError:
            print("No matching device.")
            sys.exit(42)

        m = re.match(".*(host\d+).*",link)
        lhost = m.group(1)
        delete_blockdev(match)
        rescan_lhost(lhost)

    elif args.list_serial_numbers:
        show_block_device_with_attributes(["ID_SERIAL_SHORT"],block_devices)

    else:
        parser.print_help()







