import jtextfsm as textfsm
import json
import re
# Load the input file to a variable
input_file = open("/home/fixstream/Documents/File2.txt", encoding='utf-8')
raw_text_data = input_file.read()
input_file.close()

# Run the text through the FSM.
# The argument 'template' is a file handle and 'raw_text_data' is a
# string with the content from the show_inventory.txt file
template = open("OutputNMAP.textfsm")
re_table = textfsm.TextFSM(template)
fsm_results = re_table.ParseText(raw_text_data)

# the results are written to a CSV file
outfile_name = open("outfile.csv", "w+")
outfile = outfile_name

# Display result as CSV and write it to the output file
# First the column headers...
print(re_table.header)
for s in re_table.header:
    outfile.write("%s;" % s)
outfile.write("\n")

class Device_Obj():
    My_List = []
    def __init__(self,object):

        self.Ip=object[0]
        self.Host=object[1]
        self.fqdm=object[2]
        self.port=object[3]
        Val = []
        for i in object[3]:
            Val.append(i.split())
        object[3] = Val





        # my_dict={"IpAddr":self.Ip,
        #          "Fqdm":self.fqdm,
        #          "Host":self.Host,
        #          "Port":self.port
        #          }

        dictionary_data={"PortSet":
                {"Port":[self.port],"Host":self.Host},
            "hardwareInfo":
                {"vendor": "XEN", "bios": None, "architecture": None, "instanceUuid": None, "model": "HVM DOMU", "serial": "0004FB00-0006-0000-D7FE-2D4A419B64F0"},
            "gatewayInfo":
                {"phyAddr": None, "ipv4Addr": self.Ip},
            "serviceAccountInfo":
                {"ids": ["e7cd2d23-fc5f-4309-ae24-2c15a31b97b9"]},
            "scheduleInfo": None,
            "stackInfo":
                {"model": "HVM DOMU", "type": "COMPUTE", "serial": "0004FB00-0006-0000-D7FE-2D4A419B64F0"},
            "virtualizationInfo":
                {"vendor": "XEN", "name": None, "parent": [], "virtual": 1, "role": "UNKNOWN", "type": "COMPUTE"},
            "nodeInfo":
                {"ipv4AddressSet": [self.Ip], "name": None, "dnsNameSet": [self.fqdm], "domainName": "", "alias": None, "systemName": "dcm-1", "phyAddrSet": ["0021F6D73797"], "shortName": None},
            "softwareInfo":
                {"release": None, "kernel": None, "version": "2.6.32-696.EL6.X86_64", "operatingSystem": None, "platform": "LINUX"},
            "siteInfo":
                {"id": "US"},
            "customerInfo":
                {"id": "FixStream"},
            "requestInfo":
                {"id": "c77f0d18-e830-4ed8-ba96-3a31067ed891", "name": "abhinay-2"},
            "jobRunInfo":
                {"triggerTime": "20190704050156", "msgType": "DISCOVERY/COMPUTE/IDENTIFICATION", "id": None},
            "nodeTypeInfo":
                {"category": None, "subType": "VM", "type": "COMPUTE"},
            "targetPoolInfo":
                {"target": "172.16.2.62", "pool": ["172.16.2.62"], "targets": ["172.16.2.62"]},
            "statusInfo":
                {"status": "ACTIVE", "subStatus": "TRIGGERED"},
            "connectorInfo":
                {"type": "SSH", "id": "SSH"},
            "credentials":
                [{"privilege": "a", "login": "root", "type": "cli", "secret": "FixStream"}],
            "jobInfo":
                {"id": "4267a9c7-caf1-4382-b62a-613452acc4d9"}}
        for i in object[3]:
            Port=re.findall("\d+",i[0])
            dictionary_data["PortSet"][i[2]]=Port


        self.My_List.append(dictionary_data)



# ...now all row's which were parsed by TextFSM
counter = 0
for row in fsm_results:
    Device=Device_Obj(row)
    # print(row)
    for s in row:
        outfile.write("%s;" % s)
    outfile.write("\n")
    counter += 1
print(Device.My_List)
print("Write %d records" % counter)


