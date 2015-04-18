# fauxqrz
QRZ XML interface emulator using free hamqth.com lookups

This script intercepts requests from HRDLogbook (tested on 5.24.0.38) to the QRZ XML callsign lookup and replies with data available for free from hamqth.com. 

In order for this script to do its job, one must edit the hosts file or configure the lan DNS server to redirect QRZ.com's XML servers to the address the script binds to. To edit the hosts file on windows, you need to run Notepad as administrator.

The following are the entries in my hosts file (%windir%\system32\drivers\etc\hosts on windows):
```
127.0.0.5 xml.qrz.com
127.0.0.5 xmldata.qrz.com
```

The script doesn't have to run locally however it does need to bind to port 80 which means it will need to run as root on an OS other than Windows. I bound it to 127.0.0.5 to keep it out of the way of any services that might bind to 127.0.0.1:80. 


To install necessary modules:
```
pip install requests cherrypy
```

How to use:

1. Register for a free account at www.hamqth.com.
2. Install Python 2.7.9+, install modules quoted above, download script, run script. 
3. Open HRDLogbook 5.x, Tools -> Configure -> Callsign Lookup. Enter
your hamqth login and password in the QRZ XML Service dialog and make sure it is enabled. Enter a callsign 
in the test box at the bottom to make sure it is working. I suggest using a callsign you haven't looked up
recently as HRDLogbook seems to cache lookups for a period of time. You will be able to determine if the 
callsign data was provided by the script by checking the output in the dos window.
