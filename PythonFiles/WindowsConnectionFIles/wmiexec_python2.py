import sys
import os
import cmd
import argparse
import time
import ntpath

from impacket import version, ntlm
from impacket.smbconnection import *
from impacket.dcerpc.v5.dcomrt import DCOMConnection
from impacket.dcerpc.v5.dcom import wmi
from impacket.dcerpc.v5.dtypes import NULL

OUTPUT_FILENAME = '__'


class WMIEXEC:
    def __init__(self, command='', username='', password='', domain='', hashes=None, share=None, noOutput=False):
        self.__command = command
        self.__username = username
        self.__password = password
        self.__domain = domain
        self.__lmhash = ''
        self.__nthash = ''
        self.__share = share
        self.__noOutput = noOutput
        if hashes is not None:
            self.__lmhash, self.__nthash = hashes.split(':')

    def run(self, addr):
        if self.__noOutput is False:
            smbConnection = SMBConnection(addr, addr)
            smbConnection.login(self.__username, self.__password, self.__domain, self.__lmhash, self.__nthash)
            dialect = smbConnection.getDialect()
            if dialect == SMB_DIALECT:
                print("[*] SMBv1 dialect used")
            elif dialect == SMB2_DIALECT_002:
                print("[*] SMBv2.0 dialect used")
            elif dialect == SMB2_DIALECT_21:
                print("[*] SMBv2.1 dialect used")
            else:
                print("[*] SMBv3.0 dialect used")
        else:
            smbConnection = None

        dcom = DCOMConnection(addr, self.__username, self.__password, self.__domain, self.__lmhash, self.__nthash, oxidResolver=True)

        iInterface = dcom.CoCreateInstanceEx(wmi.CLSID_WbemLevel1Login, wmi.IID_IWbemLevel1Login)
        iWbemLevel1Login = wmi.IWbemLevel1Login(iInterface)
        iWbemServices = iWbemLevel1Login.NTLMLogin('//./root/cimv2', NULL, NULL)
        iWbemLevel1Login.RemRelease()

        win32Process, _ = iWbemServices.GetObject('Win32_Process')

        try:
            self.shell = RemoteShell(self.__share, win32Process, smbConnection)
            if self.__command != ' ':
                self.shell.onecmd(self.__command)
            else:
                self.shell.cmdloop()
        except (Exception, KeyboardInterrupt)as e:
            #import traceback
            #traceback.print_exc()
            print (e)
            if smbConnection is not None:
                smbConnection.logoff()
            dcom.disconnect()
            sys.stdout.flush()
            sys.exit(1)

        if smbConnection is not None:
            smbConnection.logoff()
        dcom.disconnect()


class RemoteShell(cmd.Cmd):
    def __init__(self, share, win32Process, smbConnection):
        cmd.Cmd.__init__(self)
        self.__share = share
        self.__output = '\\' + OUTPUT_FILENAME
        self.__outputBuffer = ''
        self.__shell = 'cmd.exe /Q /c '
        self.__win32Process = win32Process
        self.__transferClient = smbConnection
        self.__pwd = 'C:\\'
        self.__noOutput = False
        self.intro = '[!] Launching semi-interactive shell - Careful what you execute'

        # We don't wanna deal with timeouts from now on.
        if self.__transferClient is not None:
            self.__transferClient.setTimeout(100000)
            self.do_cd('\\')
        else:
            self.__noOutput = True

    def do_shell(self, s):
        os.system(s)

    def do_exit(self, s):
        return True

    def emptyline(self):
        return False

    def do_cd(self, s):
        self.execute_remote('cd ' + s)
        if len(self.__outputBuffer.strip('\r\n')) > 0:
            print (self.__outputBuffer)
            self.__outputBuffer = ''
        else:
            self.__pwd = ntpath.normpath(ntpath.join(self.__pwd, s))
            self.execute_remote('cd ')
            self.__pwd = self.__outputBuffer.strip('\r\n')
            self.prompt = self.__pwd + '>'
            self.__outputBuffer = ''

    def default(self, line):
        # Let's try to guess if the user is trying to change drive
        if len(line) == 2 and line[1] == ':':
            # Execute the command and see if the drive is valid
            self.execute_remote(line)
            if len(self.__outputBuffer.strip('\r\n')) > 0:
                # Something went wrong
                print (self.__outputBuffer)
                self.__outputBuffer = ''
            else:
                # Drive valid, now we should get the current path
                self.__pwd = line
                self.execute_remote('cd ')
                self.__pwd = self.__outputBuffer.strip('\r\n')
                self.prompt = self.__pwd + '>'
                self.__outputBuffer = ''
        else:
            if line != '':
                self.send_data(line)

    def get_output(self):
        def output_callback(data):
            self.__outputBuffer += data

        if self.__noOutput is True:
            self.__outputBuffer = ''
            return

        while True:
            try:
                self.__transferClient.getFile(self.__share, self.__output, output_callback)
                break
            except Exception as e:
                if str(e).find('STATUS_SHARING_VIOLATION') >= 0:
                    # Output not finished, let's wait
                    time.sleep(1)
                    pass
                else:
                    #print str(e)
                    pass
        self.__transferClient.deleteFile(self.__share, self.__output)

    def execute_remote(self, data):
        command = self.__shell + data
        if self.__noOutput is False:
            command += ' 1> ' + '\\\\127.0.0.1\\%s' % self.__share + self.__output + ' 2>&1'
        obj = self.__win32Process.Create(command, self.__pwd, None)
        self.get_output()

    def send_data(self, data):
        self.execute_remote(data)
        print (self.__outputBuffer)
        self.__outputBuffer = ''


# Process command-line arguments.
if __name__ == '__main__':
    print (version.BANNER)

    parser = argparse.ArgumentParser()

    #parser.add_argument('target', action='store', help='[domain/][username[:password]@]<address>')
    parser.add_argument('-d', action='store', help='[domain]')
    parser.add_argument('-u', action='store', help='[username]')
    parser.add_argument('-p', action='store', help='[password]')
    parser.add_argument('-ip', action='store', help='[ip address]')
    parser.add_argument('-f', action='store', help='[file containg list of IP addresses]')
    parser.add_argument('-share', action='store', default='ADMIN$', help='share where the output will be grabbed from (default ADMIN$)')
    parser.add_argument('-nooutput', action='store_true', default=False, help='whether or not to print the output (no SMB connection created)')

    parser.add_argument('-command', action='store', help='command to execute at the target. If empty it will launch a semi-interactive shell')
    #parser.add_argument('command', nargs='*', default = ' ', help='command to execute at the target. If empty it will launch a semi-interactive shell')

    group = parser.add_argument_group('authentication')

    group.add_argument('-hashes', action="store", metavar="LMHASH:NTHASH", help='NTLM hashes, format is LMHASH:NTHASH')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    options = parser.parse_args()

    if options.command == ' ' and options.nooutput is True:
        print ("[-] Error: -nooutput switch and interactive shell not supported")
        sys.exit(1)

    addList = []

    if options.f:
        inp = open(options.f, "r")
        for line in inp.readlines():
            addList.append(line.rstrip())
        for address in addList:
            print ("[*] Running command on %s..." % address)
            username = options.u
            password = options.p
            try:
                if options.d is None:
                    domain = ''
                else:
                        domain = options.d
                if password == '' and username != '' and options.hashes is None:
                        from getpass import getpass
                        password = getpass("Password:")

                executer = WMIEXEC(options.command, username, password, domain, options.hashes, options.share, options.nooutput)
                executer.run(address)
            except (Exception, KeyboardInterrupt) as e:
                #import traceback
                #print traceback.print_exc()
                print ('\n[-] Error: %s' % e)
                sys.exit(0)

    else:
        username = options.u
        password = options.p
        address = options.ip
        try:
            if options.d is None:
                domain = ''
            else:
                    domain = options.d
            if password == '' and username != '' and options.hashes is None:
                    from getpass import getpass
                    password = getpass("Password:")

            executer = WMIEXEC(options.command, username, password, domain, options.hashes, options.share, options.nooutput)
            executer.run(address)
        except (Exception, KeyboardInterrupt) as e:
            #import traceback
            #print traceback.print_exc()
            print ('\n[-] Error: %s' % e)
            sys.exit(0)