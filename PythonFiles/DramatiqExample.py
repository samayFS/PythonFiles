from dramatiq.middleware import TimeLimitExceeded
import dramatiq
import requests

@dramatiq.actor()
def Count_Words(url):
    response=requests.get(url)
    count=len(response.text.split())
    print(f"There are {count} words in this URL:{url}")

Count_Words.send_with_options(args=("https://example.com",), delay=10000)
Count_Words("https://example.com")