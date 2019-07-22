# import pika
# from example.dramatiq_parse import text_fsm
#
# connection = pika.BlockingConnection(
#     pika.ConnectionParameters(host='localhost'))
# channel = connection.channel()
#
# channel.queue_declare(queue='queue1')
#
#
# def display_output():
#     text_fsm()
#
#
# def callback(ch, method, properties, body):
#     # f = open("received.txt", "w+")
#     # f.write("%s" % body.decode("utf-8"))
#     # text_fsm(body.decode("utf-8"))
#     print("Received %s" % body.decode("utf-8"))
#
#
# channel.basic_consume(
#     queue='queue1', on_message_callback=callback, auto_ack=True)
#
# print(' [*] Waiting for messages. To exit press CTRL+C')
# channel.start_consuming()