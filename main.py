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


def getting_banned_numbers_from_one_site_of_members(link, soup):
    request = requests.get(link)

    soup = BeautifulSoup(request.content, 'html.parser')

    s = soup.find(name='div', id='memberList')

    s = str(s)

    s_without_qm = s.replace('"', '')

    links = find_steam_links_in_string(s_without_qm)

    banned_number = 0
    notbanned_number = 0

    for i in links:
        if check_if_banned(i):
            banned_number += 1
            print('y')
        else:
            notbanned_number += 1
            print('n')
    return [banned_number, notbanned_number]

def calculating_steam_group_ban_percentage(steam_group_link, number_of_member_sites, soup):

    all_pages_numbers = [0, 0]

    for i in range(number_of_member_sites):
        current_site = getting_banned_numbers_from_one_site_of_members(steam_group_link+'/?p='+str(i+1), soup)
        print(current_site)
        all_pages_numbers[0] += current_site[0]
        all_pages_numbers[1] += current_site[1]
        print(all_pages_numbers)

    return all_pages_numbers
grouplink = str(input('paste steam group link '))+'/members'

print(grouplink)
r = requests.get(grouplink)

soup = BeautifulSoup(r.content, 'html.parser')

s = soup.find(name='div', class_='membercount members')

number_of_members = s.find(name='span', class_='count')

number_of_members = str(number_of_members)

number_of_members = int(re.findall(r'\d+', number_of_members)[0])

number_of_member_sites = int(number_of_members/51) + 1
print(number_of_members, number_of_member_sites)
final_numbers = (calculating_steam_group_ban_percentage(grouplink, number_of_member_sites, soup))

percentage = final_numbers[0]/number_of_members

print(percentage)