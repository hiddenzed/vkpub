import sys
import os


sys.path.append(os.path.join(sys.path[0], './modules'))

import group_actions as groups
import post_actions  as posts
import user_actions  as users

import requests as r
import logging  as l

import data
import json

from random    import randint, sample, choice
from threading import Thread as t
from pathlib   import Path
from time      import sleep, ctime, time
from bs4       import BeautifulSoup


comms      = data.comms

link  = 'https://api.vk.com/method/'



def feed(q):
	access_token = q['access_token']
	proxies		 = q['proxies']


	f_actions = [posts, users]

	try:

		log = choice (f_actions).from_feed (q, choice(comms))
		l.info(log)

	except ConnectionError:
		'''
		иногда вылезает ошибки подключения, connection error и еще какие то. 
		тут предполагается это дело исправлять
		'''

		print ('ConnectionError')


def group(q):
	access_token = q['access_token']
	proxies		 = q['proxies']

	log = groups.action(q)
	l.info(log)

def friend(q):
	pass

def smthng(q):
	'''
	тут будут всякие действия, например, добавить аудиозапись, создать заметку и так далее
	'''
	pass


def test(objects):
	while True:
		print ('\n\n')
		print ('[{}]'.format(ctime(time())))
		for acc in objects:
			print ('id {} | views {} | {}'.format(acc['id'], view_count(acc['id']), ban_check(acc['id'])))

		sleep(30)


def ban_check(id_):
	q = r.get('https://m.vk.com/id{}'.format(id_))
	soup = BeautifulSoup(q.text, 'lxml')

	q1 = soup.find('div', class_="owner_panel profile_panel").find('img', class_="pp_img")['src']

	if '/images/deactivated_100.png' in q1:
		return 'banned'

	else:
		return 'active'

def view_count(id_):
	try:
		page = r.get('https://m.vk.com/id{}'.format(id_))

		soup = BeautifulSoup(page.text, 'lxml')
		div  = soup.find('span', class_="item_views ")

		return (str(div).split('"v_views">')[1].split('</b>')[0])

		# return str(div.split('=\"')[1].split('\"')[0].split(' ')[0])

	except:
		return 'None'


def main():
	path = Path('accs.json')
	data = json.loads(path.read_text(encoding='utf-8'))

	for item in data['object']:
		if item['status'] == '1':
			print ('id {} starting'.format(item['id']))

			start_threads(item)

		else:
			print ('id {} banned/not ready'.format(item['id']))

	test(data['object'])


def start_threads (item):
	proxies = {
		"http"  :"http://{}".format(item['proxy']),
		"https" :"https://{}".format(item['proxy'])}

	t1 = t(target=thread_, args=(item['access_token'], proxies, item['id']))
	t1.start()

	# sleep (1)


def thread_(access_token, proxies, id_):
	print (id_)
	l.basicConfig(filename="{}.log".format(id_), level=l.INFO)
	q = {'access_token': access_token, 'proxies': proxies}

	while True:
		choice ([group, feed, feed]) (q)
		# sleep (randint(30, 190))

if __name__ == '__main__':
	main()

