import sys
from pysphere import VIServer, VIProperty, MORTypes, VIApiException
from pysphere.resources import VimService_services as VI
from pysphere.vi_task import VITask

def setupConnection(host, user, password):
        server = VIServer()

        try:
                server.connect(host, user, password)
                print "Host: " + host
                print "Version: " + server.get_server_type() + " " + server.get_api_version() + "\n"
                return server
        except Exception, err:
                print "Cannot connect to host: "+host+" error message: " +err.message
                sys.exit(2)

def closeConnection(server):
        server.disconnect()

def getVMListStatus(server):
        vmlist = server.get_registered_vms()
        for vm in vmlist:
                print "Name: " + server.get_vm_by_path(vm).get_property('name')
                print "Path: " + vm
                print "Status: " + server.get_vm_by_path(vm).get_status()
                print "Properties: " + str(server.get_vm_by_path(vm).get_properties()) + "\n"

def main(host,user,password):
        vsp = setupConnection(host,user,password)
        getVMListStatus(vsp)
        closeConnection(vsp)

if __name__ == "__main__":
        if len(sys.argv) < 3:
                print "Usage: %s vsphereserver username password" % sys.argv[0]
                sys.exit(1)

        main(sys.argv[1],sys.argv[2],sys.argv[3])

