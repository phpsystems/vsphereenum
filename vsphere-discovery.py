#!/bin/env python

# Imports
import nmap
from pysphere import VIServer, VIProperty, MORTypes, VIApiException
from pysphere.resources import VimService_services as VI
from pysphere.vi_task import VITask
from netaddr import *
import sys

# Supporting Functions
def setupConnection(host, user, password):
        server = VIServer()

        try:
                server.connect(host, user, password)
                print "[+] Host: " + host + " Version: " + server.get_server_type() + " " + server.get_api_version() + "\n"
                closeConnection(server)
                return True
        except Exception, err:
                print "[-] Cannot connect to host: "+host+" error message: " +err.message
                return None

def closeConnection(server):
        server.disconnect()
        return None

def scanRange(range):
        nmScan = nmap.PortScanner()
        nmScan.scan(range,'902,443')
        activeHosts = []
        for host in nmScan.all_hosts():
                strHost = str(host)
                state1=nmScan[strHost]['tcp'][902]['state']
                print "[*] " + strHost + " tcp/902 " +state1
                state2=nmScan[strHost]['tcp'][443]['state']
                print "[*] " + strHost + " tcp/443 " +state2
                if state1 == "open" and state2 == "open" :
                        activeHosts.append(strHost)
        return activeHosts

# Main function

def main(range,username,password):

        # Scan IP address range. Look for open ports 902 and 443.
        print "[=] Initialing scan of " +range
        vmhostlist = scanRange(range)

        print "[=]Checking the hosts a little closer..."
        # Interrogate 902 a little bit closer with the vSphere API.
        results = []
        for vmhost in vmhostlist:
                print "[=] Checking host: "+vmhost
                if setupConnection(vmhost, username, password) is True:
                        results.append([vmhost,'Success'])
                else:
                        results.append([vmhost,'Failed'])

        print "[Possible vmhost, Login attempt]"
        print results


# Argument handler

if __name__ == "__main__":
        if len(sys.argv) < 4:
                print "Usage: %s range username password" % sys.argv[0]
                print "Example: %s 192.168.1.0/24 test pass" % sys.argv[0]
                sys.exit(1)
        main(sys.argv[1],sys.argv[2],sys.argv[3])
