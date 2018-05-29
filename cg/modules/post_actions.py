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


	pub  = feed_item['source_id']
	post = feed_item['post_id']

	items = [wall_comment, wall_like]

	if feed_item['comments']['count'] > 0:
		items.append(comment_like)


	if feed_item['comments']['can_post'] == 1:
		return choice (items) (pub, post, q, s, comm)
		# comment_like (pub, post, q, s)
		

	else:
		leave_pub (pub, q, s)
		return 'posts.actions (leave_pub): leaving pub {}'.format (pub)


'''
actions
'''

def wall_comment(pub, post, q, s, comm):
	access_token = q['access_token']
	proxies      = q['proxies']

	co_params = {
		'access_token': access_token,
		'version'     : '5.74',
		'owner_id'    : pub,
		'post_id'     : post,
		'message'     : comm
	}

	response = s.get(link + 'wall.createComment', params=co_params, proxies=proxies).json()

	sleep (randint (70, 150))

	return 'posts.actions (wall_comment): comment sent to club {}'.format (pub)


def wall_like(pub, post, q, s, comm):
	access_token = q['access_token']
	proxies      = q['proxies']

	like_params = {
		'access_token': access_token,
		'version'     : '5.74',
		'type'        : 'post',
		'owner_id'    : pub,
		'item_id'     : post
	}

	response = s.get(link + 'likes.add', params=like_params, proxies=proxies).json()

	sleep (randint (20, 70))

	return 'posts.actions (wall_like): like sent to club {}'.format (pub)


def comment_like(pub, post, q, s, comm):
	access_token = q['access_token']
	proxies      = q['proxies']

	get_comments_params = {
		'access_token': access_token,
		'version'     : '5.74',
		'owner_id'    : pub,
		'post_id'     : post,
		'sort'        : 'desc'
	}

	comment = s.get(link + 'wall.getComments', params=get_comments_params, proxies=proxies).json()['response'][1]
	
	like_params = {
		'access_token': access_token,
		'version'     : '5.74',
		'type'        : 'comment',
		'owner_id'    : pub,
		'item_id'     : comment['cid']}

	response = s.get(link + 'likes.add', params=like_params, proxies=proxies).json()

	sleep (randint (30, 50))

	return 'posts.actions (comment like): sent like to comment in the club {}'.format (pub)



def leave_pub(pub, q, s):
	access_token = q['access_token']
	proxies      = q['proxies']

	leave_params = {
		'access_token': access_token,
		'version'     : '5.74',
		'group_id'    : -pub
	}

	response = s.get(link + 'groups.leave', params=leave_params, proxies=proxies).json()

	sleep (randint (10, 45))
