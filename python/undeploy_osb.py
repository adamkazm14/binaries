from java.util import HashMap
from java.util import HashSet
from java.util import ArrayList
from java.io import FileInputStream
from java.util import Collections

from com.bea.wli.sb.management.configuration import SessionManagementMBean
from com.bea.wli.sb.management.configuration import ALSBConfigurationMBean
from com.bea.wli.sb.management.configuration import BusinessServiceConfigurationMBean
 
from com.bea.wli.sb.util import EnvValueTypes
from com.bea.wli.config import Ref
from com.bea.wli.sb.util import Refs
from xml.dom.minidom import parseString

import sys

#=======================================================================================
# Utility function to read a binary file
#=======================================================================================
def readBinaryFile(fileName):
    file = open(fileName, 'rb')
    bytes = file.read()
    return bytes

#=======================================================================================
# Utility function to load properties from a config file
#=======================================================================================

def loadProps(configPropFile):
    propInputStream = FileInputStream(configPropFile)
    configProps = Properties()
    configProps.load(propInputStream)
    return configProps
	
#=======================================================================================
# Utility function to load properties from a config file
#=======================================================================================

def usage():
    print 'Usage:'
    print 'wlst ', sys.argv[0],'<property_file_path> <project_name>' 
	
#=======================================================================================
# MAIN
#=======================================================================================
if len(sys.argv) == 3:
	importConfigFile = sys.argv[1]
	projectName = sys.argv[2]
else:
	usage()
	exit()

print 'Loading Deployment config from :', importConfigFile
exportConfigProp = loadProps(importConfigFile)
adminUrl = exportConfigProp.get("adminUrl")
importUser = exportConfigProp.get("importUser")
importPassword = exportConfigProp.get("importPassword")
		
connect(importUser, importPassword, adminUrl)
#connect('weblogic', 'weblogic123', '127.0.0.1:7001')
domName=cmo.getName()
domainRuntime()

sessionName="WLSTSession"+ str(System.currentTimeMillis())
print "Trying to remove " + projectName
projectRef = Ref(Ref.PROJECT_REF, Ref.DOMAIN, projectName)

SessionMBean = findService("SessionManagement", "com.bea.wli.sb.management.configuration.SessionManagementMBean")
print "SessionMBean started session"
SessionMBean.createSession(sessionName)
print 'Created session<', sessionName, '>'
ALSBConfigurationMBean = findService("ALSBConfiguration." + sessionName, "com.bea.wli.sb.management.configuration.ALSBConfigurationMBean")

if ALSBConfigurationMBean.exists(projectRef):
	ALSBConfigurationMBean.delete(Collections.singleton(projectRef))
	SessionMBean.activateSession(sessionName, "Complete project removal with customization using wlst")
else:
	failed = "OSB project <" + projectName + "> does not exist"
	print failed
	raise Failure(failed)

