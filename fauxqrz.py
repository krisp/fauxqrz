# fauxqrz.py -- Fool HRD Logbook into thinking this script is xmldata.qrz.com
#               and feed it free hamqth.com data instead
# pip install cherrypy requests
# add the following entries to %windir%\system32\drivers\etc\hosts:
# 127.0.0.5 xmldata.qrz.com
# 127.0.0.5 xml.qrz.com

import cherrypy
import requests
import re
from datetime import datetime
from xml.etree import ElementTree

hamqthurl = "http://www.hamqth.com/xml.php"

translate = [
              [ r'<callsign>(.*)</callsign>', r'<call>\1</call>'],
              [ r'<adif>(.*)</adif>', r'<dxcc>\1</dxcc>'],              
              [ r'<adr_name>(.*)\s(.*)</adr_name>', r'<fname>\1</fname><name>\2</name>'],
              [ r'adr_street1', r'addr1'],
              [ r'adr_city', r'addr2'],
              [ r'us_county', r'county'],
              [ r'latitude', r'lat'],
              [ r'longitude', r'lon'],
              [ r'us_state', r'state'],
              [ r'adr_zip', r'zip'],
              [ r'adr_country', r'country'],
              [ r'adr_adif', r'ccode'],
              [ r'<HamQTH version="2.6" xmlns="http://www.hamqth.com">', r'<QRZDatabase version="1.33">'],
              [ r'<search>', r'<Callsign>'],
              [ r'</search>', r'</Callsign>'],
              [ r'</HamQTH>', r''],
            ]

class fauxqrz(object):
    @cherrypy.expose
    def xml(self, *args, **kargs):
      return self.index(*args, **kargs)

    @cherrypy.expose
    def index(self, username=0, password=0, agent=0, s=0, callsign=0, bio=0):        
	if not username and not callsign and not bio:
            return "fauxqrz runs here (http://github.com/krisp/fauxqrz)"

        now = datetime.utcnow().ctime()
        # logging in
        if username:
            cherrypy.response.headers['Content-Type'] = "text/xml"            
            # need these for hamqth.com
            self.username = username
            self.password = password
			
            r = requests.get(hamqthurl + "?u=%s&p=%s" % (username, password))
            t = ElementTree.fromstring(r.content)

            key = t[0][0].text
            # error the way qrz would if login to h
            if "Wrong" in key:
                return """<?xml version="1.0" encoding="iso-8859-1" ?>
<QRZDatabase version="1.33" xmlns="http://xmldata.qrz.com">
<Session>
<Error>Password Incorrect</Error>
<GMTime>"""+now+"""</GMTime>
<Remark>cpu: 0.027s</Remark>
</Session>
</QRZDatabase>"""

            # return hamqth.com key            
            return """<?xml version="1.0" ?> 
<QRZDatabase version="1.33">
  <Session>
    <Key>"""+key+"""</Key> 
    <Count>1</Count> 
    <SubExp>Thu Jan 1 12:00:00 2099</SubExp> 
    <GMTime>"""+now+"""</GMTime> 
  </Session>
</QRZDatabase>
"""
        # looking up callsign
        if callsign and s:
            cherrypy.response.headers['Content-Type'] = "text/xml"

            r = requests.get(hamqthurl + "?id=%s&callsign=%s&prg=fauxqrz" % (s,callsign))
            xml = r.content
            #t = ElementTree.fromstring(r.content)

            # translate raw xml text
            newxml = xml
            for x in (translate):
                newxml = re.sub(x[0], x[1], newxml)
            
            return newxml + """
  <Session>
      <Key>"""+s+"""</Key> 
      <Count>1</Count> 
      <SubExp>Thu Jan 1 12:00:00 2099</SubExp> 
      <GMTime>"""+now+"""</GMTime> 
  </Session>
</QRZDatabase>"""            

        if bio and s:
            cherrypy.response.headers['Content-Type'] = "text/xml"
            return """<?xml version="1.0" ?> 
<QRZDatabase version="1.18" xmlns="http://www.qrz.com">
    <Bio>
	<call>"""+bio+"""</call> 
	<size>258</size> 
	<bio>http://www.qrz.com/db/"""+bio+"""</bio> 
	<modified>2015-01-01</modified> 
    </Bio>
  <Session>
      <Key>"""+s+"""</Key> 
      <Count>1</Count> 
      <SubExp>Thu Jan 1 12:00:00 2099</SubExp> 
      <GMTime>"""+now+"""</GMTime> 
  </Session>
</QRZDatabase>"""
        else:
            return "Invalid combination of options"

if __name__ == "__main__":
    cherrypy.config.update({'server.socket_host': '127.0.0.5',
                            'server.socket_port': 80,
                       })
    cherrypy.tree.mount(fauxqrz(), "/xml/current")
    cherrypy.tree.mount(fauxqrz(), "/bin")
    cherrypy.engine.start()
    cherrypy.engine.block()