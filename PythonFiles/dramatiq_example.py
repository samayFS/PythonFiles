import dramatiq
import requests
import time
from dramatiq.middleware import TimeLimitExceeded


@dramatiq.actor(priority=10)
def count_words(url):
     response = requests.get(url)
     count = len(response.text.split(" "))
     print(f"There are {count} words at {url!r}.")

@dramatiq.actor(priority=0)
def count_wordss(url):
     response = requests.get(url)
     count = len(response.text.split(" "))
     print(f"There are {count} words at 2 {url!r}.")


# Synchronously count the words on example.com in the current process
count_words("http://fo.com")
count_wordss("http://fo.com")

# or send the actor a message so that it may perform the count
# later, in a separate process.
#      count_words.send("http://fb.com")