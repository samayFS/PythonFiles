import getpass
import telnetlib

HOST = "172.16.1.27"
user = input("Enter your remote account: ")
password = getpass.getpass()

tn = telnetlib.Telnet(HOST)

# tn.read_until(b"login: ",20)
tn.write(user.encode('ascii') + b"\n")
if password:
    tn.read_until(b"Password: ",20)
    tn.write(password.encode('ascii') + b"\n")
tn.interact()
# tn.write(b"x  dir\n")
# tn.write(b"exit\n")
print(tn.read_all().decode('ascii'))