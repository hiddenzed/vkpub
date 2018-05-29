import requests as r
import lxml.html
import os

import get_sms
from random import randint, choice, shuffle
from time import sleep

path = '/home/emach/ws/ws2/2/modules'

import sys
sys.path.insert(0, path)

def reg(proxies, name, last_name, headers):
	s    = r.session()
	data = s.get('https://m.vk.com/join', headers=headers, proxies=proxies)
	page = lxml.html.fromstring(data.content)

	form = page.forms[0]
	form.fields['first_name'] = name
	form.fields['last_name']  = last_name
	form.fields['bday']       = str(randint(1, 24))
	form.fields['bmonth']     = str(randint(1,11))
	form.fields['byear']      = str(randint(1996, 1999))
	form.fields['sex']        = '1'

	response = s.post('https://m.vk.com/' + form.action, data=form.form_values(), proxies=proxies)

	num = get_sms.get_number()

	phone_page = lxml.html.fromstring(response.content)


	form = phone_page.forms[0]

	form.fields['phone_prefix'] = '+77'
	form.fields['phone_number'] = num[2][2:]

	res = s.post('https://m.vk.com/' + form.action, data=form.form_values(), proxies=proxies)
	code_page = lxml.html.fromstring(res.content)
	form = code_page.forms[0]

	if 'code' in form.fields:
		get_sms.set_status(num)
		code = get_sms.get_sms(num)
		form.fields['code'] = code
		res1 = s.post('https://m.vk.com/' + form.action, data=form.form_values(), proxies=proxies)

		pass_page = lxml.html.fromstring(res1.content)
		form = pass_page.forms[0]

		form.fields['pass'] = '12010712ll'

		res2 = s.post(form.action, data=form.form_values(), proxies=proxies)

		return num[2]

	else:
		print ('not lol')
		get_sms.set_status_bad(num)
		return 'BAD_NUM'

def get_access_token(login, pass_, proxies):
	s = r.session()
	login_page = s.get('https://m.vk.com/login', proxies=proxies)

	parsed_login_page = lxml.html.fromstring(login_page.content)
	form = parsed_login_page.forms[0]

	form.fields['email'] = login
	form.fields['pass'] = pass_

	auth = s.post(form.action, data=form.form_values(), proxies=proxies)

	params = {
		'client_id'     : '4083558',
		'scope'         : 'friends,photos,audio,video,docs,notes,pages,status,offers,questions,wall,groups,messages,notifications,stats,ads,market,offline',
		'redirect_uri'  : 'https://api.vk.com/blank.html',
		'display'       : 'wap',
		'v'             : '5.74',
		'response_type' : 'token',
		'revoke'        : 0
	}

	data = s.get('https://oauth.vk.com/authorize', params=params, proxies=proxies)

	try:
		toked = lxml.html.fromstring(data.content)
		form = toked.forms[0]

		data = s.post(form.action, proxies=proxies)
	except:
		pass

	access_token = data.url.split('access_token=')[1].split('&expires')[0]
	return access_token


def set_privacy (proxies, login, pass_, headers):
	url = 'https://m.vk.com/login'

	s    = r.session()
	data = s.get(url, headers=headers, proxies=proxies)
	page = lxml.html.fromstring(data.content)

	form = page.forms[0]
	form.fields['email'] = login
	form.fields['pass'] = pass_

	response = s.post(form.action, data=form.form_values(), proxies=proxies)

	url1 = 'https://m.vk.com/settings?act=privacy&privacy_edit=groups'
	url2 = 'https://m.vk.com/settings?act=privacy&privacy_edit=status_replies'
	url3 = 'https://m.vk.com/settings?act=privacy&privacy_edit=mail_send'

	set_one(url1, s, '3', headers, proxies)
	set_one(url2, s, '3', headers, proxies)
	set_one(url3, s, '3', headers, proxies)

	print ('privacy set')

def set_one(url, s, val, headers, proxies):
	data = s.get(url, headers=headers, proxies=proxies)
	page = lxml.html.fromstring(data.content)

	form = page.forms[0]
	form.fields['val'] = val

	s.post('https://m.vk.com/' + form.action, headers=headers, proxies=proxies, data=form.form_values())


def avatar_post (access_token, proxies):
	url = 'https://api.vk.com/method/'

	server = r.get(url + 'photos.getOwnerPhotoUploadServer', params={'access_token': access_token, 'version': '5.74'}, proxies=proxies).json()['response']['upload_url']
	files = {'file': open('modules/photos/' + choice(os.listdir('modules/photos/')), 'rb')}

	params = r.post(server, files=files, proxies=proxies).json()
	params.update({'version': '5.74', 'access_token': access_token})


	print (r.get(url + 'photos.saveOwnerPhoto', params=params, proxies=proxies).json())


def repost (access_token, proxies, posts):
	url = 'https://api.vk.com/method/'

	shuffle(posts)

	for post in posts:

		params = {
			'access_token': access_token,
			'version'     : '5.74',
			'object'      : post
		}

		resp = r.get(url + 'wall.repost', params=params, proxies=proxies).json()

		print (resp)
		sleep(2)

	# params = {
	# 	'access_token': access_token,
	# 	'version'     : '5.74',
	# 	'object'      : pwall
	# }

	# resp = r.get(url + 'wall.repost', params=params, proxies=proxies).json()

