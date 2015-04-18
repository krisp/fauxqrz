# fauxqrz
QRZ XML interface emulator using free hamqth.com lookups

This python script emulates the QRZ XML interface using lookups from hamqth.com's XML interface.
In order for this script to intercept requests from Ham Radio Deluxe's Logbook, one must add
the following entries to the hosts file (%windir%\system32\drivers\etc\hosts on windows):

```
127.0.0.5 xml.qrz.com
127.0.0.5 xmldata.qrz.com
```

The script doesn't have to run locally however it does need to bind to port 80 which means it will need to run as root on an OS other than Windows. I bound it to 127.0.0.5 to keep it out of the way of any services that might bind to 127.0.0.1:80. 


To install necessary modules:
```
pip install requests cherrypy
```

Register for a free account at www.hamqth.com, open HRDLogbook 5.x, Tools -> Options -> Callsign Lookup. Enter
your hamqth login and password in the QRZ XML Service dialog and make sure it is enabled. Enter a callsign 
in the test box at the bottom to make sure it is working.
