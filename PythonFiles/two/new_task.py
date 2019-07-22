import sys
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
# message = ' '.join(sys.argv[1:]) or "Hello World!"
for i in range(1,20):
    channel.basic_publish(exchange='',
                          routing_key='queue2',
                          body=str(i),
                          properties=pika.BasicProperties(
                          delivery_mode=2,  # make message persistent
        ))
    print(" [x] Sent %r" % i)
connection.close()
