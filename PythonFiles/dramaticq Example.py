# import dramatiq
# import requests
# import sys
# import logging
#
#
# @dramatiq.actor
# def count_words(url):
#      response = requests.get(url)
#      count = len(response.text.split(" "))
#      print("There are {} words at {}.".format(count,url))
# #
# #  urls = [
# #      "https://google.com",
# #     "https://github.com",
# #     "https://rabbitmq.com",
# #  ]
# # Synchronously count the words on example.com in the current process
# # count_words(urls)
#
# # or send the actor a message so that it may perform the count
# # later, in a separate process.
# # [count_words.send(url) for url in urls]
# count_words.send_with_options(args=("https://example.com",), delay=10000)


import dramatiq
import requests
import sys
import logging


@dramatiq.actor
def count_words(url):
    response = requests.get(url)
    count = len(response.text.split(" "))
    print("There are {} words at {}.".format(count,url))


count_words("https://google.com")

count_words.send("https://google.com")
logging.warning("SENT SUCCESSFULLY")


@dramatiq.actor
def add(x, y):
    add.logger.info("The sum of %d and %d is %d.", x, y, x + y)

