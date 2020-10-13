import requests
from bs4 import BeautifulSoup

url = 'https://odusapps.princeton.edu/StudentOrg/new/directory.php'
response = requests.get(url)
soup = BeautifulSoup(response.text)

clubs = soup.findAll("div", {"class": "jumbotron"})

for c in clubs:
    print(c)
