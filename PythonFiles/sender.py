import json
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
f = open('/home/fixstream/SSH/ifconfig.txt', encoding='utf-8')

# channel.queue_declare(queue='text_fsm')
message = {
    "queue_name": "text_fsm",
    "actor_name": "text_fsm",
    "args": [],
    "options": {},
        "kwargs": {"data": f.read()}}

channel.basic_publish(exchange='',
                      routing_key='text_fsm',
                      body=json.dumps(message))
f.close()
print("Message Sent")
connection.close()
