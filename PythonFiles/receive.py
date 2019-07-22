import pika
import jtextfsm as textfsm

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='queue1')


class Device():

    def __init__(self):

        self.platform = None

        self.fqdm = None

        self.version = None


def text_fsm(raw_text_data):
    template = open("ifconfig.textfsm")
    re_table = textfsm.TextFSM(template)
    fsm_results = re_table.ParseText(raw_text_data)

    outfile_name = open("outfile.csv", "w+")
    outfile = outfile_name

    print(re_table.header)
    for s in re_table.header:
        outfile.write("%s;" % s)
    outfile.write("\n")

    # ...now all row's which were parsed by TextFSM
    counter = 0
    for row in fsm_results:
        print(row)
        for s in row:
            outfile.write("%s;" % s)
        outfile.write("\n")
        counter += 1
    print("Write %d records" % counter)


def callback(ch, method, properties, body):
    # f = open("received.txt", "w+")
    # f.write("%s" % body.decode("utf-8"))
    print("Received %s" % body.decode("utf-8"))
    # text_fsm(body.decode("utf-8"))


channel.basic_consume(
    queue='queue1', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()


A = Device()

A.platform = "Linux"

print(A.platform)
