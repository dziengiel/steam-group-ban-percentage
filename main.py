import requests, re
from bs4 import BeautifulSoup


def check_if_banned(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'html.parser')
    s = soup.find(name='div', class_='profile_ban_status')
    if s:
        return True
    else:
        return False

def find_steam_links_in_string(string):
    results = re.findall(r'href=https://steamcommunity.com/(?:profiles/(\d+)|id/([\w-]+))', string)
    links = []
    for i in results:
        if i[0]:
            links.append(f'https://steamcommunity.com/profiles/{i[0]}')
        else:
            links.append(f'https://steamcommunity.com/id/{i[1]}')
    return set(links)

grouplink = str(input('paste steam group link '))

grouplink = grouplink+'/members'

r = requests.get(grouplink)

soup = BeautifulSoup(r.content, 'html.parser')

s = soup.find(name='div', id='memberList')

s = str(s)

s_without_qm = s.replace('"', '')

links = find_steam_links_in_string(s_without_qm)

banned = 0
notbanned = 0

for i in links:
    if check_if_banned(i):
        banned+=1
    else:
        notbanned+=1

bannedpercentage = banned/(banned+notbanned)*100

print(f'{bannedpercentage}%')