import requests as r
import json

link = 'https://api.vk.com/method/messages.getDialogs'

pub_token = ''

class Get_dialogs:
	def __init__(self):
		print ('start')

		count = r.get(link, params={'access_token': pub_token, 'version': '5.73'}).json()['response'][0] // 200
		dialogs = []

		while count >= 0:
			dialog_list = self.request(200 * count)
			dialogs += dialog_list

			count -= 1

		print ('writing result in file')
		file = open('dialogs.txt', 'w')

		for item in dialogs:
			file.write(str(item) + '\n')

		print ('ready')
			

	def request(self, offset):
		response = r.get(link, params={'access_token': pub_token, 'version': '5.73', 'count': 200, 'offset': offset}).json()
		dialog_list = []

		for index in range(1, 200):
			try:
				dialog_list.append(response['response'][index]['uid'])

			except:
				continue

		return dialog_list

get = Get_dialogs()
