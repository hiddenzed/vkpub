from random import randint, choice
from time   import sleep

import requests as r


link  = 'https://api.vk.com/method/'

'''
main functions
'''

def from_feed(q, comm):
	access_token = q['access_token']
	proxies      = q['proxies']

	s = r.session()

	feedparams = {
		'access_token': access_token,
		'version'     : '5.74',
		'filters'     : 'post',
		'count'       : 1
	}

	feed_item = s.get(link + 'newsfeed.get', params=feedparams, proxies=proxies).json()['response']['items'][0]


	pub_id = -feed_item['source_id']

	mem_params = {
		'access_token': access_token,
		'version'     : '5.74',
		'group_id'    : pub_id,
		'sort'        : 'id_desc',
		'offset'      : randint(10, 200),
		'count'       : 1}

	# print ('why bug')
	# print (s.get(link + 'groups.getMembers', params=mem_params, proxies=proxies).json())
	user_in = s.get(link + 'groups.getMembers', params=mem_params, proxies=proxies).json()
	if 'error' in user_in:
		print (user_in)
		print ('error in user_in')

	else:
		user = user_in['response']['users'][0]


		user_params = {
			'access_token': access_token,
			'version'     : '5.74',
			'user_ids'    : user,
			'fields'      : 'sex'
		}

		user_info = s.get(link + 'users.get', params=user_params, proxies=proxies).json()['response'][0]


		if 'deactivated' in user_info:
			return 'users.from_feed: id {} is banned'.format(user_info['uid'])

		else:
			if user_info['sex'] == 2:
				return choice ([av_like, po_like, wall_co, av_co]) (user_info['uid'], q, s, comm)
				# po_like (user_info['uid'], q, s)

			else:
				return 'users.from_feed: id {} \'s sex is female'.format(user_info['uid'])

'''
actions
'''

def av_like(user, q, s, comm):
	access_token = q['access_token']
	proxies      = q['proxies']

	av_params = {
		'access_token': access_token,
		'version'     : '5.74',
		'user_ids'    : user,
		'fields'      : 'photo_id'
	}

	av = s.get(link + 'users.get', params=av_params, proxies=proxies).json()['response'][0]
	

	if 'photo_id' not in av:
		return 'users.from_feed (av_like): id {} has no avatar'.format(user)

	else:
		like_params = {
			'access_token': access_token,
			'version'     : '5.74',
			'type'        : 'photo',
			'owner_id'    : user,
			'item_id'     : av['photo_id'].split('_')[1]
		}

		response = s.get(link + 'likes.add', params=like_params, proxies=proxies).json()

		sleep (randint (40, 90))

		return 'users.from_feed (av_like): sent like to id {}'.format(user)


def wall_co(user, q, s, comm):
	access_token = q['access_token']
	proxies      = q['proxies']

	wall_params = {
		'access_token': access_token,
		'version'     : '5.74',
		'owner_id'    : user,
		'count'       : 1,
		'offset'      : randint(0, 3),
		'filer'       : 'owner'
	}

	wall = s.get(link + 'wall.get', params=wall_params, proxies=proxies).json()['response']

	try:
		if wall[1]['comments']['can_post'] == 1:

			co_params = {
				'access_token': access_token,
				'version'     : '5.74',
				'owner_id'    : user,
				'post_id'     : wall[1]['id'],
				'message'     : comm
			}

			response = s.get(link + 'wall.createComment', params=co_params, proxies=proxies).json()

			sleep (randint (50, 250))

			return 'users.from_feed (wall_co): sent comment to id {} '.format(user)

		else:
			return 'users.from_feed (wall_co): commenting in id {} \'s wall is not allowed'.format(user)


	except:
		return 'users.from_feed (wall_co): id {} \'s wall is empty'.format(user)


def po_like(user, q, s, comm):
	access_token = q['access_token']
	proxies      = q['proxies']

	wall_params = {
		'access_token': access_token,
		'version'     : '5.74',
		'owner_id'    : user,
		'count'       : 1,
		'offset'      : randint(0, 3),
		'filer'       : 'owner'
	}

	wall = s.get(link + 'wall.get', params=wall_params, proxies=proxies).json()['response']

	try:
		if wall[1]['likes']['can_like'] == 1:

			like_params = {
				'access_token': access_token,
				'version'     : '5.74',
				'type'        : 'post',
				'owner_id'    : user,
				'item_id'     : wall[1]['id']
			}

			response = s.get(link + 'likes.add', params=like_params, proxies=proxies).json()

			sleep (randint (3, 20))

			return 'users.from_feed (po_like): sent like to id {} \'s wall'.format(user)

		else:
			return 'users.from_feed (po_like): id {} liking is not allowed'.format(user)

	except:
		return 'users.from_feed (po_like): id {} \'s wall is empty'.format(user)


def av_co(user, q, s, comm):
	access_token = q['access_token']
	proxies      = q['proxies']

	av_params = {
		'access_token': access_token,
		'version'     : '5.74',
		'user_ids'    : user,
		'fields'      : 'photo_id'
	}

	av = s.get(link + 'users.get', params=av_params, proxies=proxies).json()['response'][0]

	if 'photo_id' not in av:
		return 'users.from_feed (av_co): id {} has no avatar'.format(user)

	else:
		co_params = {
			'access_token': access_token,
			'version'     : '5.74',
			'owner_id'    : user,
			'photo_id'    : av['photo_id'].split('_')[1],
			'message'     : comm
		}

		response = s.get(link + 'photos.createComment', params=co_params, proxies=proxies).json()

		if 'error' in response:
			return 'users.from_feed (av_co): commenting in id {} \'s avatar is not allowed'.format(user)

		else:
			sleep (randint (40, 99))

			return 'users.from_feed (av_co): sent comment to id {} \'s avatar'.format(user)

def send_re(user, q):
	access_token = q['access_token']
	proxies      = q['proxies']

	'''
	maybe later?
	right now friends requests sending is risk because of big chance of ban
	'''

def send_me(user, q):
	access_token = q['access_token']
	proxies      = q['proxies']

	'''
	this too
	'''