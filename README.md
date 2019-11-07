# pingmcast

## Quick way to send/receive multicast packets using python socket module

**Usage**

 Use mode 's' to run sender mode. Sender mode will generate 5 UDP echoes destined to the
 group address provided.

 `python pingmcast.py -g 239.1.1.1 -m s`

Mode 'r' is used to run receiver mode. In receiver mode, the program will
listen to packets destined to the group on all interfaces. Requires permissions to
bind to sockets.

`python pingmcast.py -g 239.1.1.1 -m r`
