import requests, re
from bs4 import BeautifulSoup


def check_if_banned(link):

    r = requests.get(link)

    soup = BeautifulSoup(r.content, 'html.parser')

    s = soup.find(name='div', class_='profile_ban_status')

    if s == None:
        return False
    else:
        return True

# def find_steam_links_in_string(string):
#     string = string.split()
#     links = set()
#     for i in string:
#         if i.startswith("href=https://steamcommunity.com/profiles/"):
#             links.add(i)
#     return links
# #not banned
# print(check_if_banned('https://steamcommunity.com/id/pstwo/'))
#
# #banned
# print(check_if_banned('https://steamcommunity.com/profiles/76561199118069915'))


grouplink = str(input('paste steam group link '))

grouplink = grouplink+'/members'

print(grouplink)

r = requests.get(grouplink)

soup = BeautifulSoup(r.content, 'html.parser')

s = soup.find(name='div', id='memberList')

s = str(s)

s_without_qm = s.replace('"', '')

links = re.findall(r'href=https://steamcommunity.com/profiles/(\d+)', s_without_qm)

print(links)


