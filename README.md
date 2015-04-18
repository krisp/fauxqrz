# fauxqrz
QRZ XML interface emulator using free hamqth.com lookups

This script intercepts requests from HRDLogbook (tested on 5.24.0.38) to the QRZ XML callsign lookup and replies with data available for free from hamqth.com. 

In order for this script to do its job, one must edit the ```hosts``` file or configure the lan DNS server to redirect QRZ.com's XML servers to the address the script binds to. To edit the ```hosts``` file on windows, you need to run Notepad as administrator.

The following are the entries in my ```hosts``` file (%windir%\system32\drivers\etc\hosts on windows):
```
127.0.0.5 xml.qrz.com
127.0.0.5 xmldata.qrz.com
```
Run ```ipconfig /flushdns``` in a command window to reload the hosts file.

Support to pass through the NOAA solar data that causes an "unknown error" when launching HRDLogbook has been added as well. The following hosts entry is needed for this to work:
```
127.0.0.5 www.swpc.noaa.gov
```
If you are still seeing the error after making the change, delete the 4 or 5 text files from %appdata%\Simonb~1\HRDLog~1\ and restart HRDLogbook. 

To use just the sunspot fix, leave the qrz entries out of your ```hosts``` file.

The script doesn't have to run locally however it does need to bind to port 80 which means it will need to run as root on an OS other than Windows. I bound it to 127.0.0.5 to keep it out of the way of any services that might bind to 127.0.0.1:80. 

Installation:

1. Install python 2.7.9+ (https://www.python.org/ftp/python/2.7.9/python-2.7.9.msi). Check "Add python to path" on the last screen.
2. Run a command prompt and run ```pip install requests cherrypy```
3. Run notepad as administrator and edit ```%windir%\system32\drivers\etc\hosts```, add the appropriate entries listed above.
4. Flush dns from the command line: ```iptables /flushdns```
5. Delete text files from ```%appdata%\Simonb~1\HRDLog~1\``` for solar data fix
6. Sign up for a hamqth.com account and configure QRZ lookup using your hamqth.com login.

How to set up hamqth passthrough in HRDLogbook

1. Register for a free account at www.hamqth.com.
2. Open HRDLogbook 5.x, Tools -> Configure -> Callsign Lookup. Enter
your hamqth login and password in the QRZ XML Service dialog and make sure it is enabled. Enter a callsign 
in the test box at the bottom to make sure it is working. I suggest using a callsign you haven't looked up
recently as HRDLogbook seems to cache lookups for a period of time. You will be able to determine if the 
callsign data was provided by the script by checking the output in the dos window.
