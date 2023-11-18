# pip install requests

# On the other device (ex.: 10.1.1.1) run the: python3 -m http.server 2020

import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

def download_file(url, local_filename):
    with requests.get(url, stream=True) as r:
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
    return local_filename

def list_files(url):
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    return [url + '/' + node.get('href') for node in soup.find_all('a') if node.get('href')]

def download_from_server(url, path='.'):
    if not os.path.exists(path):
        os.mkdir(path)
    for item in list_files(url):
        if item.endswith('/'):
            download_from_server(item, os.path.join(path, item.split('/')[-2]))
        else:
            download_file(item, os.path.join(path, item.split('/')[-1]))

server_url = 'http://10.1.1.1:2020'
download_from_server(server_url)
