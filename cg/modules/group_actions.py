import requests as r

from random import randint, choice, shuffle
from time   import sleep

link = 'https://api.vk.com/method/'


def action (q):
	access_token = q['access_token']
	proxies      = q['proxies']

	s = r.session()

	return rand_join(q, s)


'''
actions
'''

def rand_join(q, s):
	access_token = q['access_token']
	proxies      = q['proxies']

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


	base = closed_pubs + open_pubs
	shuffle (base)
	pub = choice (base)

	join_params = {
		'access_token': access_token,
		'version'     : '5.74',
		'groups.join' : pub
	}


	result = s.get(link + 'groups.join', params=join_params, proxies=proxies).json()

	sleep (randint (10, 39))

	return 'groups.from_feed (rand_join): sent request to public {}'.format(pub)

def rand_leave():
	pass