from java.util import HashMap
from java.util import HashSet
from java.util import ArrayList
from java.io import FileInputStream

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
    print 'wlst ', sys.argv[0],'<property_file_path> <osb_jar_file_path>' 
	
#=======================================================================================
# MAIN
#=======================================================================================
if len(sys.argv) == 3:
	importConfigFile = sys.argv[1]
	jarPath = sys.argv[2]
else:
	usage()
	exit()

print 'Loading Deployment config from :', importConfigFile
exportConfigProp = loadProps(importConfigFile)
adminUrl = exportConfigProp.get("adminUrl")
importUser = exportConfigProp.get("importUser")
importPassword = exportConfigProp.get("importPassword")
		
connect(importUser, importPassword, adminUrl)
domName=cmo.getName()
domainRuntime()

print 'Domain for deploy ', domName

SessionMBean = findService(SessionManagementMBean.NAME,SessionManagementMBean.TYPE)
sessionName="WLSTSession"+ str(System.currentTimeMillis())
SessionMBean.createSession(sessionName)
alsbSession = findService(ALSBConfigurationMBean.NAME + "." + sessionName, ALSBConfigurationMBean.TYPE)
alsbCore = findService(ALSBConfigurationMBean.NAME, ALSBConfigurationMBean.TYPE)

print 'Attempting to import :',jarPath 

theBytes = readBinaryFile(jarPath)

ALSBConfigurationMBean = findService(String("ALSBConfiguration.").concat(sessionName), "com.bea.wli.sb.management.configuration.ALSBConfigurationMBean")
print "Upload jar", jarPath
ALSBConfigurationMBean.uploadJarFile(theBytes)
print 'jar uploaded'

print 'No project specified, additive deployment performed'
alsbJarInfo = ALSBConfigurationMBean.getImportJarInfo()
alsbImportPlan = alsbJarInfo.getDefaultImportPlan()
#alsbImportPlan.setPassphrase(passphrase)
alsbImportPlan.setPreserveExistingEnvValues(true)
importResult = ALSBConfigurationMBean.importUploaded(alsbImportPlan)
SessionMBean.activateSession(sessionName, "Complete test import with customization using wlst")

print 'import executed, project deployed'
		
