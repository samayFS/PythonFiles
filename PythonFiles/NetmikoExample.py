from netmiko import Netmiko
import getpass

cisco1 = {
    "host": "172.16.5.37",
    "username": "root",
    "password": getpass.getpass(),
    "device_type": "cisco_ios",
}
net_connect = Netmiko(**cisco1)
net_connect.enable()
print(net_connect.find_prompt())
net_connect.disconnect()
# from __future__ import print_function, unicode_literals

# Netmiko is the same as ConnectHandler
from netmiko import Netmiko
from getpass import getpass

# my_device = {
#     "host": "172.16.5.37",
#     "username": "root",
#     "password": getpass(),
#     "device_type": "cisco_ios",
# }
#
# net_connect = Netmiko(**my_device)
# # Requires ntc-templates to be installed in ~/ntc-templates/templates
# output = net_connect.send_command("show ip int brief", use_textfsm=True)
# print(output)