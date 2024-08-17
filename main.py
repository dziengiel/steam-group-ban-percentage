import requests
from bs4 import BeautifulSoup


def check_if_banned(link):

    r = requests.get(link)

    soup = BeautifulSoup(r.content, 'html.parser')

    s = soup.find(name='div', class_='profile_ban_status')

    if s == None:
        return False
    else:
        return True


#not banned
print(check_if_banned('https://steamcommunity.com/id/pstwo/'))

#banned
print(check_if_banned('https://steamcommunity.com/id/psdwa'))