import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker
import jtextfsm as textfsm

rabbitmq_broker = RabbitmqBroker(host="localhost")
rabbitmq_broker.declare_queue('text_fsm')
dramatiq.set_broker(rabbitmq_broker)



@dramatiq.actor
def text_fsm(**kwargs):
    template = open("ifconfig.textfsm")
    re_table = textfsm.TextFSM(template)
    fsm_results = re_table.ParseText(kwargs['data'])

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
