import pika
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
f = open('/home/fixstream/workspace/python/fsm/SSH/ifconfig.txt', encoding='utf-8')
channel.queue_declare(queue='queue1')
channel.basic_publish(exchange='',
                      routing_key='queue1',
                      body=f.read())
print("Message Sent")
connection.close()