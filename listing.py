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
# MAIN
#=======================================================================================
#connect(userConfigFile='<userConfigFile_location>', userKeyFile='<userKeyFile_location>', url='t3://<myserver_ip>:<myserver_port>')
connect('weblogic', 'weblogic123', '127.0.0.1:7001')
domName=cmo.getName()
domainRuntime()

print 'start'
print domName

SessionMBean = findService(SessionManagementMBean.NAME,SessionManagementMBean.TYPE)
sessionName="WLSTSession"+ str(System.currentTimeMillis())
SessionMBean.createSession(sessionName)
alsbSession = findService(ALSBConfigurationMBean.NAME + "." + sessionName, ALSBConfigurationMBean.TYPE)
alsbCore = findService(ALSBConfigurationMBean.NAME, ALSBConfigurationMBean.TYPE)
allRefs=alsbCore.getRefs(Ref.DOMAIN)
for ref in allRefs.iterator():
	print ref

print 'koniec listing refs'

allProjects=alsbCore.getProjects()

for proj in allProjects.iterator():
	print proj

print 'koniec listing projects'

importJarPath = 'd:/helloosb.jar'
print 'Attempting to import :', importJarPath

theBytes = readBinaryFile(importJarPath)
print 'Read file', importJarPath
#print 'Content', theBytes

ALSBConfigurationMBean = findService(String("ALSBConfiguration.").concat(sessionName), "com.bea.wli.sb.management.configuration.ALSBConfigurationMBean")
print "ALSBConfiguration MBean found", ALSBConfigurationMBean
ALSBConfigurationMBean.uploadJarFile(theBytes)
print 'jar uploaded'

print 'No project specified, additive deployment performed'
alsbJarInfo = ALSBConfigurationMBean.getImportJarInfo()
alsbImportPlan = alsbJarInfo.getDefaultImportPlan()
#alsbImportPlan.setPassphrase(passphrase)
alsbImportPlan.setPreserveExistingEnvValues(true)
importResult = ALSBConfigurationMBean.importUploaded(alsbImportPlan)
SessionMBean.activateSession(sessionName, "Complete test import with customization using wlst")

print 'import executed'
		
