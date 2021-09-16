import time
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='queue2', durable=True)


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    time.sleep(3)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(" [x] Done")


channel.basic_qos(prefetch_count=2)
channel.basic_consume(
    queue='queue2', on_message_callback=callback)


print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
