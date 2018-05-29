import requests as r
import time


url = 'http://api.getsms.online/stubs/handler_api.php'
key = ''


def get_number():
	params = {
		'api_key' : key,
		'action'  : 'getNumber',
		'country' : 'kz',
		'service' : 'vk',
	}

	num = r.get(url, params=params).text.split(':')

	if 'NO_NUMBER' in num:
		return 'NO_NUMBER'

	else:
		return num

def set_status(num):
	params = {
		'api_key': key,
		'action' : 'setStatus',
		'id'     : num[1],
		'status' : 1
	}

	response = r.get(url, params=params).text
	print (response)

def get_sms(num):
	params = {
		'api_key': key,
		'action' : 'getStatus',
		'id'     : num[1]
	}

	while True:
		response = r.get(url, params=params).text

		# if 'STATUS_ACCESS' in response:
		# 	return response.split(':')[1]
		time.sleep(9)
		print (response)

		try:
			q = response.split(':')[1]
			break

		except:
			if 'STATUS_WAIT_CODE' in response:
				continue
			else:
				break


	response = r.get(url, params=params).text
	return response.split(':')[1]

def set_status_bad(num):
	params = {
		'api_key': key,
		'action' : 'setStatus',
		'id'     : num[1],
		'status' : -1
	}

	response = r.get(url, params=params).text
	print (response)