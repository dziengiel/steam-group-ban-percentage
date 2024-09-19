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


def getting_banned_numbers_from_one_side_of_members(link, soup):
    request = requests.get(link)

    soup = BeautifulSoup(request.content, 'html.parser')

    s = soup.find(name='div', id='memberList')

    s = str(s)

    s_without_qm = s.replace('"', '')

    links = find_steam_links_in_string(s_without_qm)

    banned_number = 0
    notbanned_number = 0

    for i in links:
        print('checking if banned')
        if check_if_banned(i):
            notbanned_number += 1
            print('n')
        else:
            banned_number += 1
            print('y')
    return banned_number, notbanned_number

grouplink = str(input('paste steam group link '))+'/members'

print(grouplink)
r = requests.get(grouplink)

soup = BeautifulSoup(r.content, 'html.parser')

s = soup.find(name='div', class_='membercount members')

number_of_members = s.find(name='span', class_='count')

number_of_members = str(number_of_members)

number_of_members = int(re.findall(r'\d+', number_of_members)[0])

number_of_member_sites = int(number_of_members/51) + 1
print(number_of_members)

print(getting_banned_numbers_from_one_side_of_members(grouplink, soup))
