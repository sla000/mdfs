import paramiko
import os
import shutil
import stat

class Ssh:
    def __init__(self, ip, user, passwd):
        self.ip = ip
        self.port = 22
        self.user = user
        self.passwd = passwd

        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    def connect(self):
        self.client.connect(hostname=self.ip, username=self.user, password=self.passwd, port=self.port)

    def execute(self, cmd):
        stdin, stdout, stderr = self.client.exec_command(cmd)
        return (stdout.read() + stderr.read()).strip('\n')

    def __tar(self, directory):
        assert directory != '/'
        tarName = os.path.basename(directory.strip(os.path.sep)) + '.tar.gz'
        if os.path.exists(tarName):
            return tarName
        print tarName
        assert tarName != ''
        cmd = 'tar zcvf %s %s' % (tarName, directory)
        os.system(cmd)
        print cmd
        return tarName
        
    def __openTransport(self):
        transport = paramiko.Transport((self.ip, self.port))
        transport.connect(username=self.user, password=self.passwd)
        sftp = paramiko.SFTPClient.from_transport(transport)
        return sftp, transport
    def __closeTransport(self, sftp, transport):
        sftp.close()
        transport.close()

    def __pushFile(self, local, remote):
        sftp, transport = self.__openTransport()
        try:
            sftp.put(local, remote)
        except Exception as e:
            print 'Failed push file: %s --> %s. Error: %s' % (local, remote, e.message)
        finally:
            self.__closeTransport(sftp, transport)


    def __pushDir(self, directory, remote):
        tar = self.__tar(directory)
        remotetar = remote + '.tar.gz'
        self.__pushFile(tar, remotetar)
        cmd = 'tar zxvf %s -C %s' % (remotetar, os.path.dirname(remote))
        print cmd
        self.execute(cmd)
        self.execute('rm -rf ' + remotetar)

    def push(self, local, remote):
        if os.path.isdir(local):
            self.__pushDir(local, remote)
        else:
            self.__pushFile(local, remote)

    def __pullFile(self, remote, local, sftp):
        sftp.get(remote, local)
        
    def __pullDir(self, remote, directory, sftp):
        tar = os.path.basename(remote.strip(os.path.sep)) + '.tar.gz'
        cmd = 'cd %s && tar zcvf %s *' % (remote, tar)
        self.execute(cmd)
        
        remoteTarAbsPath = os.path.join(remote, tar)
        self.__pullFile(remoteTarAbsPath, tar, sftp) 
        self.execute('rm -rf ' + remoteTarAbsPath)
        
        if not os.path.exists(directory):
            os.mkdir(directory)
            os.chmod(directory, 0755)

        os.system('tar zxvf %s -C %s >/dev/null' % (tar, directory))
        os.unlink(tar)


    def pull(self, remote, local):
        sftp, transport = self.__openTransport()
        try:
            info = sftp.stat(remote)
        except Exception as e:
            print 'Failed stat remote file: %s. Error: %s' % (remote, e.message)
            self.__closeTransport(sftp, transport)
            return

        try:
            if stat.S_ISDIR(info.st_mode):
                self.__pullDir(remote, local, sftp)
            else:
                self.__pullFile(remote, local, sftp)
        except Exception as e:
            print 'Failed pull remote file: %s --> %s. Error: %s' % (remote, local, e.message)
        finally:
            self.__closeTransport(sftp, transport)

    def close(self):
        self.client.close()

ip='10.0.3.178'
un = 'ubuntu'
ssh = Ssh(ip, un, un)
ssh.connect()
ssh.pull('/home/ubuntu/aa/bb', 'bbc')
