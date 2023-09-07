from bs4 import BeautifulSoup
import requests
import requests.exceptions
import urllib.parse
from collections import deque
import re

user_url = str(input('[+]Enter the Target URL which is required to be scanned: '))
urls = deque([user_url])
scraped_urls = set()  # Corrected variable name
email = set()
count = 0

try:
    while len(urls):
        count += 1
        if count == 100:
            break
        url = urls.popleft()  # Corrected variable name
        
        scraped_urls.add(url)  # Use "scraped_urls" instead of "scrapped_url"

        parts = urllib.parse.urlsplit(url)
        base_url = '{0.scheme}://{0.netloc}'.format(parts)
        
        path = url[:url.rfind('/') + 1] if '/' in parts.path else url
        print('[%d] Processing %s' % (count, url))
        try:
            response = requests.get(url)
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):  # Fixed typo in exception names
            continue
        
        new_emails = set(re.findall(r'[a-z0-9\. \-+_]+@[a-z0-9\. \-+_]+\.[a-z]+', response.text, re.I))
        email.update(new_emails)

        soup = BeautifulSoup(response.text, features="lxml")  # Fixed variable name "Response" to "response"

        for anchor in soup.find_all("a"):
            link = anchor.get('href', '')
            if link.startswith('/'):
                link = base_url + link
            elif not link.startswith('http'):
                link = path + link
            if link not in urls and link not in scraped_urls:  # Use "not in" instead of "not link in"
                urls.append(link)

except KeyboardInterrupt:
    print('[-] Closing!!')

for mail in email:
    print(mail)
