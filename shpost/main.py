import requests as r

import os
import random

access_token = ''
pubid        = 

link       = 'https://api.vk.com/method/'
message    = '#sex #porn #hotgirls #erotic #порнуха #секс #порно #бот'
promo_link = ''


def main (q):
	utime = r.get(link + 'utils.getServerTime',  params={'version': '5.78', 'access_token': access_token}).json()['response'] + 70

	for iq in q:

		
		messg = iq [1]

		files = {'file': open(iq [0], 'rb')}

		url = r.get(link + 'photos.getWallUploadServer', params={'access_token': access_token, 'version': '5.74', 'group_id': pubid}).json()['response']['upload_url']
		photoload = r.post(url, files=files).json()

		wallsaveparams = {
			'access_token' : access_token,
			'version'      : '5.78',
			'group_id'     : pubid,
			'photo'        : photoload['photo'],
			'server'       : photoload['server'],
			'hash'         : photoload['hash']
			}

		photo = r.get(link + 'photos.saveWallPhoto', params=wallsaveparams).json()['response'][0]['id']

		postparams = {
			'owner_id'     : -pubid,
			'message'      : messg,
			'publish_date' : utime,
			'access_token' : access_token,
			'version'      : '5.78',
			'attachments'  : photo
		}

		answertopost = r.post(link + 'wall.post', params=postparams)

		print (answertopost.json ())

		utime += 8640

def amain ():
	rfiles   = 'rphoto.jpg'
	rmessage = 'Бесплатный секс видео чат 🍓\n\nЗарегистрируйся и получи VIP достут к привату😉🍓\nА так же получишь 50 бесплатных токенов за которые девушки выполнят твои желания 😏\n\nПолучить VIP 👉 {}\n\n{}'.format (promo_link, message)
	reclam = [rfiles, rmessage]
	q = []

	for i in range (0, 151):
		files = 'photos/' + random.choice(os.listdir('photos/'))
		q0 = [files, message]
		q.append (q0)

	for i in range (0, 151, 4):
		q[i] = reclam

	main (q)

	



if __name__ == '__main__':
	amain()