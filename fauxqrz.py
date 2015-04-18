# fauxqrz.py -- Fool HRD Logbook into thinking this script is xmldata.qrz.com
#               and feed it free hamqth.com data instead
# pip install cherrypy requests
# add the following entries to %windir%\system32\drivers\etc\hosts:
# 127.0.0.5 xmldata.qrz.com
# 127.0.0.5 xml.qrz.com

import cherrypy
import requests
import re
import os
from datetime import datetime
from xml.etree import ElementTree

hamqthurl = "http://www.hamqth.com/xml.php"

translate = [
              [ r'<callsign>(.*)</callsign>', lambda match: r'<call>%s</call>' % (match.group(1).upper())],
              [ r'<(.*)>(-?\d*\.\d+)</.*>', lambda match: "<%s>%.5f</%s>" % (match.group(1),float(match.group(2)),match.group(1))],
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
              [ r'<HamQTH version="\d*\.\d+" xmlns="http://www.hamqth.com">', r'<QRZDatabase version="1.33" xmlns="http://www.qrz.com">'],
              [ r'<search>', r'<Callsign>'],
              [ r'</search>', r'</Callsign>'],
              [ r'</HamQTH>', r''],
              [ r'<(.*)>\?</.*>', r'<\1>N</\1>' ],
              [ r'<itu>(.*)</itu>', r'<ituzone>\1</ituzone>'],
              [ r'<cq>(.*)</cq>', r'<cqzone>\1</cqzone>'],
              [ r'utc_offset', r'GMTOffset'],
              [ r'<nick>.*</nick>', r''],
              [ r'<qth>.*</qth>', r''],
              [ r'<continent>.*</continent>', r'<bio>none</bio>'],
              [ r'<qsldirect>.*</qsldirect>', r''],
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
			
            r = requests.get(hamqthurl + "?u=%s&p=%s" % (username, password))
            t = ElementTree.fromstring(r.content)

            key = t[0][0].text
            # error the way qrz would if login to h
            if "Wrong" in key:
                return """<?xml version="1.0" encoding="iso-8859-1" ?>
                        <QRZDatabase version="1.33" xmlns="http://www.qrz.com">
                        <Session>
                        <Error>Password Incorrect</Error>
                        <GMTime>"""+now+"""</GMTime>
                        <Remark>cpu: 0.027s</Remark>
                        </Session>
                        </QRZDatabase>"""

            # return hamqth.com key            
            return """<?xml version="1.0" ?> 
                    <QRZDatabase version="1.33" xmlns="http://www.qrz.com">
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

            r = requests.get(hamqthurl + "?id=%s&callsign=%s&prg=fauxqrz" % (s,callsign.upper()))
            xml = r.content

            # translate xml from hamqth format to qrz format
            for x in (translate):
                xml = re.sub(x[0], x[1], xml)
            
            return xml + """<Session>
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
                            <bio>Imported using fauxqrz (http://github.com/krisp/fauxqrz)</bio> 
                            <modified>2015-04-18</modified> 
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
    print "===== fauxqrz starting up =====\nhttp://github.com/krisp/fauxqrz"
    print "==============================="
    cherrypy.config.update({'server.socket_host': '127.0.0.5',
                            'server.socket_port': 80,
                       })
    cherrypy.tree.mount(fauxqrz(), "/xml/current")
    cherrypy.tree.mount(fauxqrz(), "/bin")
    cherrypy.engine.start()
    cherrypy.engine.block()
