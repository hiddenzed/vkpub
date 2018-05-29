from pathlib   import Path
from threading import Thread as t
from time      import sleep, time, ctime
from random    import randint, sample, shuffle
from bs4       import BeautifulSoup

import json
import requests as r
import captcha  as cap

url = 'https://api.vk.com/method/'


def main():
	path = Path('accs.json')
	data = json.loads(path.read_text(encoding='utf-8'))

	for item in data['object']:
		if item['status'] == '1':
			print ('id {} starting'.format(item['id']))

			start_threads(item)

		else:
			print ('id {} banned/not ready'.format(item['id']))

	# test(data['object'])

def start_threads(item):
	proxies = {
		"http"  :"http://{}".format(item['proxy']),
		"https" :"https://{}".format(item['proxy'])}

	t1 = t(target=thread_, args=(item['access_token'], proxies))
	t1.start()

def thread_(access_token, proxies):
	while True:
		by_banned(access_token, proxies)
                #join_pubs(access_token, proxies)


def join_pubs(access_token, proxies):
	closed_pubs = []
	open_pubs   = []

	with open ('closed.txt', 'r') as file:
		for line in file:
			closed_pubs.append(line.strip())

	with open ('open.txt', 'r') as file:
		for line in file:
			open_pubs.append(line.strip())

	shuffle (closed_pubs)
	shuffle (open_pubs)


	base = closed_pubs[0:30] + open_pubs[0:30]
	shuffle (base)

	for pub in base:
		joinparams = {
			'access_token': access_token,
			'version'     : '5.73',
			'group_id'    : pub
		}

		result = r.get(url + 'groups.join', params=joinparams, proxies=proxies).json()

		if 'response' in result:
			if result['response'] == 1:
				print ('join request added to community', pub)

		elif 'error' in result:
			if result['error']['error_code'] == 14:
				print ('captcha needed')
				capkey = cap.main(result['error']['captcha_img'])

				joincaptchaparams = {
					'access_token': access_token,
					'version'     : '5.73',
					'group_id'    : line.strip(),
					'captcha_sid' : result['error']['captcha_sid'],
					'captcha_key' : capkey
				}

				print (r.get(url + 'groups.join', params=joincaptchaparams, proxies=proxies).json())

		sleep(randint(7, 40))



def by_banned(access_token, proxies):



	groups_get_params = {
		'access_token': access_token,
		'version'     : '5.74',
		'count'       : '1000'
	}

	groups = r.get(url + 'groups.get', params=groups_get_params, proxies=proxies)

	for pubid in groups.json()['response'][1:1000]:
		get_wall_params = {
			'access_token': access_token,
			'version'     : '5.74',
			'owner_id'    : -pubid,
			'count'       : 1
		}

		wall_info = r.get(url + 'wall.get', params=get_wall_params, proxies=proxies)

		if wall_info.json()['response'][1]['comments']['can_post'] == 0:
			leave_params = {
				'access_token': access_token,
				'version'     : '5.74',
				'group_id'    : pubid
			}

			print (r.get(url + 'groups.leave', params=leave_params, proxies=proxies).json())
			sleep(2)
		sleep(0.6)

if __name__ == '__main__':
	main()
