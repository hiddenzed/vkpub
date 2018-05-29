from pathlib   import Path
from random    import randint, sample, shuffle
from time      import sleep, time, ctime
from threading import Thread as t
from bs4       import BeautifulSoup


import json
import requests as r

import sys
import os

sys.path.append(os.path.join(sys.path[0], './modules'))

import captcha as c
import data    as d


def main():
	path = Path('accs.json')
	data = json.loads(path.read_text(encoding='utf-8'))

	for item in data['object']:
		if item['status'] == '0':
			print ('id {} starting'.format(item['id']))

			start_threads(item)

		else:
			print ('id {} status not 0'.format(item['id']))

	out_0(data['object'])


def amain():
	path = Path('accs.json')
	data = json.loads(path.read_text(encoding='utf-8'))

	for item in data['object']:
		print ('id {} starting'.format(item['id']))

		start_threads(item)

	out_1(data['object'])


def start_threads(item):
	proxies = {
		"http"  :"http://{}".format(item['proxy']),
		"https" :"https://{}".format(item['proxy'])}

	t1 = t(target=thread_, args=(item['access_token'], proxies))
	t1.start()


def thread_(access_token, proxies):
	url = 'https://api.vk.com/method/'

	closed_pubs = []
	open_pubs   = []

	with open ('modules/closed.txt', 'r') as file:
		for line in file:
			closed_pubs.append(line.strip())

	with open ('modules/open.txt', 'r') as file:
		for line in file:
			open_pubs.append(line.strip())

	shuffle (closed_pubs)
	shuffle (open_pubs)    


	base = closed_pubs[0:40] + open_pubs[0:15]
	shuffle (base)

	s = r.session()
	for pub in base:
		joinparams = {
			'access_token': access_token,
			'version'     : '5.73',
			'group_id'    : pub}
		
		try:
			result = s.get(url + 'groups.join', params=joinparams, proxies=proxies).json()

		except:
			sleep (4)

		if 'response' in result:
			if result['response'] == 1:
				pass

		elif 'error' in result:
			if result['error']['error_code'] == 14:
				print ('captcha needed')
				capkey = c.main(result['error']['captcha_img'])

				joincaptchaparams = {
					'access_token': access_token,
					'version'     : '5.73',
					'group_id'    : line.strip(),
					'captcha_sid' : result['error']['captcha_sid'],
					'captcha_key' : capkey}

				s.get(url + 'groups.join', params=joincaptchaparams, proxies=proxies).json()
		
		sleep(randint(7, 20))

def out_0(objects):
	while True:
		print ('\n\n')
		print ('[{}]'.format(ctime(time())))
		for acc in objects:
			if acc['status'] == '0':
				print ('id {} | pubs count {} | {}'.format(acc['id'], pcount(acc['access_token']), ban_check(acc['id'])))

		sleep(40)

def out_1(objects):
	while True:
		print ('\n\n')
		print ('[{}]'.format(ctime(time())))

		for acc in objects:
			print ('id {} | pubs count {} | {}'.format(acc['id'], pcount(acc['access_token']), ban_check(acc['id'])))

		sleep (40)



def pcount(access_token):
	q = r.get('https://api.vk.com/method/groups.get', params={'access_token': access_token, 'version': '5.74', 'extended': 1}).json()

	try:
		return q['response'][0]

	except:
		return None

def ban_check(id_):
	q = r.get('https://m.vk.com/id{}'.format(id_))
	soup = BeautifulSoup(q.text, 'lxml')

	q1 = soup.find('div', class_="owner_panel profile_panel").find('img', class_="pp_img")['src']

	if '/images/deactivated_100.png' in q1:
		return 'banned'

	else:
		return 'active'

amain()
