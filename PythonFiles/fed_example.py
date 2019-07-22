import math
import pika
import configparser

import codecs
config=configparser.ConfigParser()
config.read("Config.conf")

Username=config.get("MyConfig","Username")
Password=config.get("MyConfig","Password")
Host=config.get("MyConfig",'Host')
vHost=config.get("MyConfig",'vHost')
Port=config.get("MyConfig",'Port')

# User=config.get("SeocndConfig",'User')
# Pass=config.get("SeocndConfig",'Pass')


# with codecs.open('Config.conf', 'r', encoding='utf-8') as f:config.readfp(f)
#
# password = config.get('MyConfig', 'Password')
#
# print ('Password:', password.encode("utf-8"))
#
# print(Username)
# print(Password)
# print(Host)
# print(vHost)


credentials = pika.PlainCredentials(Username,Password)
connection = pika.BlockingConnection(pika.ConnectionParameters(Host,Port,vHost,credentials))
channel = connection.channel()

channel.exchange_declare(exchange="fed_test", exchange_type="fanout", durable=True)
channel.queue_declare(queue='fed_test_queue', durable=True)
channel.queue_purge(queue='fed_test_queue')

channel.queue_bind(exchange="fed_test", queue="fed_test_queue",routing_key="")
for rk in list(map(lambda s: str(s), range(0, 5))):
    hdrs = {u'hash-on': rk}
    channel.basic_publish(exchange="fed_test", routing_key="",
                      body="My Config File is Running PLease Check Again",
                      properties = pika.BasicProperties(content_type='text/plain',
                                  delivery_mode=2,
                                headers=hdrs
                                  ))

print("Published.........")
m=math.tan(30)
connection.close()

