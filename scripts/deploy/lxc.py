import os, subprocess 
class Lxc:
    @staticmethod
    def execute(cmd):
        cwd = os.getcwd()
        os.chdir('../lxc')
        result = subprocess.check_output(cmd, shell=True)
        os.chdir(cwd)
        return result
    @staticmethod
    def getContainersIP():
        ipList = Lxc.execute('./learn-ip.sh').split('\n')
        ipList = filter(lambda x: x != '', ipList)
        return ipList

