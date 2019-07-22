# from wmiexec import WMIEXEC
from ateexec import TSCH_EXEC
# # from ateexec import TSCH_EXEC
# # from PythonFiles.WindowsConnectionFIles.wmiexec import WMIEXEC
# # # import WMIEXEC from wmiexec
from wmiexec_python2 import WMIEXEC




#!!!!!!!!!!!!!!DRAMATIQ EXECUTION!!!!!!!!!!!!!!!!!
# import dramatiq
# from dramatiq.brokers.rabbitmq import RabbitmqBroker
#
# rabbitmq_broker = RabbitmqBroker(host="localhost")
# rabbitmq_broker.declare_queue('Win_Con')
# dramatiq.set_broker(rabbitmq_broker)
#
# @dramatiq.actor
# def Win_Con(**kwargs):
#     print(kwargs)
#     executer = TSCH_EXEC(username=kwargs['username'], password=kwargs['password'], domain=kwargs['domain'],hashes=None,aesKey=None,doKerberos=False,kdcHost=None,command=kwargs['command'])
#     ip_addr=kwargs['ipaddr']
#     data=executer.play(ip_addr)




#
# executer = WMIEXEC(command="systeminfo",username="Administrator",password="FixStream012",domain="bramha",noOutput=False,hashes=None, aesKey=None, share=None,doKerberos=False, kdcHost=False)
# data=executer.run("172.16.2.136")

executer = TSCH_EXEC(username="administrator", password="FixStream012", domain="bramha",hashes=None,aesKey=None,doKerberos=False,kdcHost=None,command="systeminfo")
ip_addr="172.16.2.136"
data=executer.play(ip_addr)
# print(data)

# executer=WMIEXEC(command="systeminfo", username="administrator", password="FixStream012", domain="bramha", hashes=None, share=None, noOutput=False)
# data=executer.run("172.16.2.136")
# print(data)