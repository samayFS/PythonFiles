from pypsexec.client import Client

# creates an encrypted connection to the host with the username and password
c = Client("172.16.2.136", username="administrator", password="FixStream012",port=139)

c.connect()
try:
 c.create_service()
 stdout = c.run_executable("cmd.exe", arguments="iisreset")
 output = []
 output = stdout[0].decode("utf-8")
 print(output.split("\r\n")[1:3])
finally:
 c.cleanup()
 c.remove_service()
 c.disconnect()