import requests as r
import time


link         = 'https://api.vk.com/method/wall.post'
access_token = ''

message = 'Пятерочка приглашает Продавцов-Кассиров\n\nУсловия:\n• Оформление в соответствии с ТК РФ\n• Карьерный рост\n\nОбязанности:\n• Обслуживание покупателей на кассе\n• Выкладка товара в зале\n• Консультация покупателей в зале\n\nТребования:\n• Ответственность\n• Гражданство РФ (или РВП/ВНЖ)\n\nОставить резюме https://vk.cc/86yxeW'


pubs = open('base.txt', 'r')

for pub in pubs:

	params5 = {
		'access_token': access_token,
		'version'     : '5.78',
		'message'     : message,
		'attachments' : 'photo-39624278_456260076',
		'owner_id'    : '-' + pub.strip()
	}

	print (r.post(link, params=params5).json())
	print (pub.strip())
	print ('\n')
	time.sleep(3)
