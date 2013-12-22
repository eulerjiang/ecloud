'''
Created on Mar 16, 2013

@author: Euler Jiang
'''
import os
import subprocess
from ecloud import settings

class InstanceHanlder():
    # return non-zero code if failed to create instance
    def createInstance(self, image, username, orderNumber, executeCommand="executeCommand", resourceType = 1, logfile = None):
        self.image = image
        self.username = username
        self.resourceType = resourceType
        
        if logfile is None:
            self.logfile = settings.ecloud_log_dir + "/order" + str(orderNumber) + ".log"
        else:
            self.logfile = settings.ecloud_log_dir + "/order" + str(orderNumber) + ".log"
        
        self.failureReason = ""
        
        if os.path.isabs(executeCommand) == False:
            executeCommand = settings.ecloud_script_dir + "/" + executeCommand
        self.executeCommand = executeCommand
            
        if not os.path.exists(self.executeCommand):
            self.failureReason = "Missed the command %s to create instance" % (self.executeCommand)
            return 1
        
        commandLine = self.executeCommand + " --action=create " + self.image + " " + self.username + " " + str(self.resourceType)
        print("execute command: " + commandLine)

        output = open(self.logfile,'w')
        returnCode = subprocess.call(commandLine.split(), stdout= output )

        print("finished command " + commandLine)
        
        self.initInstanceInfo()
        
        return returnCode
    
    def destroyInstance(self, uuid, executeCommand="executeCommand"):
        self.logfile = "/tmp/" + uuid

        if os.path.isabs(executeCommand) == False:
            executeCommand = settings.ecloud_script_dir + "/" + executeCommand
        self.executeCommand = executeCommand
            
        if not os.path.exists(self.executeCommand):
            print("Error: no such command: " + self.executeCommand + ", please check the configuration of this template!")
            return 1
 
        commandLine = self.executeCommand + " --action=destroy " + uuid + " > " + self.logfile
        print("execute command:" + commandLine)

        output = open(self.logfile,'w')
        returnCode = subprocess.call(commandLine.split(), stdout= output )

        print("finished command " + commandLine)
       
        return returnCode
    
    def stopInstance(self, uuid, executeCommand="executeCommand"):
        if os.path.isabs(executeCommand) == False:
            executeCommand = settings.ecloud_script_dir + "/" + executeCommand
        self.executeCommand = executeCommand

        if not os.path.exists(self.executeCommand):
            print("Error: no such command: " + self.executeCommand + ", please check the configuration of this template!")
            return 1
        
        commandLine = self.executeCommand + " --action=stop " + uuid
        print("execute command:" + commandLine)

        returnCode = subprocess.call(commandLine.split())

        print("finished command " + commandLine)
       
        return returnCode
    
    def restartInstance(self, uuid, executeCommand="executeCommand"):
        if os.path.isabs(executeCommand) == False:
            executeCommand = settings.ecloud_script_dir + "/" + executeCommand
        self.executeCommand = executeCommand

        if not os.path.exists(self.executeCommand):
            print("Error: no such command: " + self.executeCommand + ", please check the configuration of this template!")
            return 1
        
        commandLine = self.executeCommand + " --action=restart " + uuid
        print("execute command:" + commandLine)

        returnCode = subprocess.call(commandLine.split())

        print("finished command " + commandLine)
       
        return returnCode 

    def startInstance(self, uuid, executeCommand="executeCommand"):
        if os.path.isabs(executeCommand) == False:
            executeCommand = settings.ecloud_script_dir + "/" + executeCommand
        self.executeCommand = executeCommand

        if not os.path.exists(self.executeCommand):
            print("Error: no such command: " + self.executeCommand + ", please check the configuration of this template!")
            return 1
        
        commandLine = self.executeCommand + " --action=start " + uuid
        print("execute command:" + commandLine)

        returnCode = subprocess.call(commandLine.split())

        print("finished command " + commandLine)
       
        return returnCode
    
    def initInstanceInfo(self):
        self.uniqueID = "133lskjdie"
        self.instanceName = "not_defined"
        self.publicIP = "127.0.0.1"
        self.privateIP = "127.0.0.1"
        
        infoFile = open(self.logfile, 'r')
        lines = infoFile.readlines()               
        infoFile.close()
        
        targetLines = lines[-4:]
        for line in targetLines:
            if line.startswith("InstanceName:"):
                self.instanceName = line.replace("InstanceName: ", "")
            elif line.startswith("InstanceUniqueID:"):
                self.uniqueID = line.replace("InstanceUniqueID: ", "")
            elif line.startswith("InstancePublicIP:"):
                self.publicIP = line.replace("InstancePublicIP: ", "")
            elif line.startswith("InstancePrivateIP:"):
                self.privateIP = line.replace("InstancePrivateIP: ", "")
            
    def getInstanceUniqueID(self):
        return self.uniqueID
    
    def getInstanceName(self):
        return self.instanceName

    def getInstancePublicIP(self):
        return self.publicIP
    
    def getInstancePrivateIP(self):
        return self.privateIP
    
if __name__ == '__main__':
    pass
