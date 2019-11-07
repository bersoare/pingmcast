#! /usr/bin/env python

import socket
import struct
import sys
import argparse
import ipaddress
import time

def getargs():

    parser = argparse.ArgumentParser()
    parser.add_argument("-g","--group", type=str,help="Group address")
    parser.add_argument("-mode", "-m",
                        help='''Mode. Use r for Receiver, s for sender.''',
                        choices=['r','s'])

    return parser.parse_args()

def sender(group):

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ttl = struct.pack('b', 10)
    sock.settimeout(0.2)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    print "Sending 5 packets to {}...".format(group)
    count = 1

    while count < 6:
        try:
            print "Sending packet number {}".format(count)
            sock.sendto("mcast ping", (group, 666))
            time.sleep(1)
        except:
            print "Failed sending packet ;("

        count +=1

    sock.close()

def receiver(group):

    try:

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', 666))

        mgroup = socket.inet_aton(group)
        mreq = struct.pack('4sL', mgroup, socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    except Exception as e:
        print "Error binding to socket. \n{}".format(e)
        sys.exit(1)

    count = 0

    while True:
        try:
            data, address = sock.recvfrom(1024)
            count += 1
            print "Packet received from source {}, group {}. Count: {}".format(address, group, count)
        except:
            sock.close()
            sys.exit(0)

def main():
    args = getargs()

    group_add = args.group

    try:
        valid = ipaddress.IPv4Address(u'{}'.format(group_add))
        if not valid.is_multicast:
            print "{} is not a valid multicast address. Please see RFC 3171.".format(group_add)
            sys.exit(1)
    except Exception as e:
        print "Error! {} is not a valid group address!".format(group_add)
        sys.exit(1)

    if args.mode == "s":
        sender(group_add)

    if args.mode == "r":
        print "Entering receiver mode! Quit with control-c"
        try:
            receiver(group_add)
        except:
            sys.exit(0)

if __name__ == "__main__":
    main()
