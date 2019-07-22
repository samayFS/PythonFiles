import json
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
# f = open('/home/fixstream/SSH/ifconfig.txt', encoding='utf-8')

# channel.queue_declare(queue='text_fsm')
message = {
    "queue_name": "Win_Con",
    "actor_name": "Win_Con",
    "args": [],
    "options": {},
        "kwargs": {"ipaddr":"172.16.2.136","command":"systeminfo","username":"administrator","password":"FixStream012","domain":"bramha" }}

channel.basic_publish(exchange='',
                      routing_key='Win_Con',
                      body=json.dumps(message))
# f.close()
print("Message Sent")
connection.close()
