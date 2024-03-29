import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
ch = connection.channel()

ch.exchange_declare(exchange="e", exchange_type="x-consistent-hash", durable=True)

for q in ["q1", "q2", "q3", "q4"]:
    ch.queue_declare(queue=q, durable=True)
    ch.queue_purge(queue=q)

for q in ["q1", "q2"]:
    ch.queue_bind(exchange="e", queue=q, routing_key="1")

for q in ["q3", "q4"]:
    ch.queue_bind(exchange="e", queue=q, routing_key="2")

n = 10000

for rk in list(map(lambda s: str(s), range(0, n))):
    ch.basic_publish(exchange="e", routing_key=rk, body="")
print("Done publishing.")

print("Waiting for routing to finish...")
# in order to keep this example simpler and focused,
# wait for a few seconds instead of using publisher confirms and waiting for those
time.sleep(5)

print("Done.")
connection.close()
