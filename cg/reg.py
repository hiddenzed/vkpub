import sys
import os

sys.path.append(os.path.join(sys.path[0], './modules'))

import data

headers    = data.headers
names      = data.names
last_names = data.last_names
posts      = data.posts
pass_      = data.pass_

import json
import requests as r

from random  import choice, shuffle, randint
from pathlib import Path
from time    import sleep

import vkp
import captcha  as c


def one (proxy):
	proxies = {
		"http"  :"http://{}".format(proxy.strip()), 
		"https" :"https://{}".format(proxy.strip())
	}

	while  True:
		login = str(vkp.reg(proxies, choice(names), choice(last_names), headers))

		if login != 'BAD_NUM':
			access_token = vkp.get_access_token(login, pass_, proxies)
			id_          = r.get('https://api.vk.com/method/users.get', params={'access_token': access_token, 'version': '5.74'}, proxies=proxies).json()['response'][0]['uid']
			status       = '0'

			write_json      (id_, login, pass_, proxies, proxy.strip(), status, access_token)
			vkp.set_privacy (proxies, login, pass_, headers)
			vkp.avatar_post (access_token, proxies)
			vkp.repost      (access_token, proxies, posts)


			print ('ended')
			return True

		else:
			print (login)

def write_json (id_, login, pass_, proxies, proxy, status, access_token):
	newobject = {
		"id"          : id_,
		"link"        : 'https://vk.com/id{}'.format(id_),
		"login"       : login,
		"pass"        : pass_,
		"proxy"       : proxy,
		"status"      : status,
		"access_token": access_token}

	path   = Path('accs.json')
	myjson = json.loads(path.read_text(encoding='utf-8'))


	myjson['object'].append(newobject)

	with open('accs.json', 'w') as file:
		json.dump(myjson, file, indent=2, ensure_ascii=False)

def main ():
	proxy_file = open('modules/proxies.txt', 'r')

	for proxy in proxy_file:
		one (proxy)


if __name__ == '__main__':
	main()