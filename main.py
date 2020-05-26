import os
import json
import math
import sys
import requests
import csv
import urllib.request
from datetime import datetime, timezone, timedelta
from time import localtime, strftime, sleep

headers = {
	'authority': 'stockx.com',
	'upgrade-insecure-requests': '1',
	'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
	'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
	'sec-fetch-site': 'none',
	'sec-fetch-mode': 'navigate',
	'sec-fetch-user': '?1',
	'sec-fetch-dest': 'document',
	'accept-language': 'en-US,en;q=0.9',
}

def load_from_json(file):
	try:
		with open(file, 'r') as myfile:
			return json.load(myfile)
	except IOError:
		with open(file, 'w') as myfile:
			json.dump({}, myfile)
		return {}

def center(text, spacer=' ', length=100, clear=False, display=True):
	if clear:
		os.system('cls' if os.name == 'nt' else 'clear')
	count = int(math.ceil((length - len(text)) / 2))
	if count > 0:
		if display:
			print(spacer * count + text + spacer * count)
		else:
			return (spacer * count + text + spacer * count)
	else:
		if display:
			print(text)
		else:
			return text

def smart_time():
	return str(strftime('%m/%d/%y %I:%M:%S %p', localtime()))

def smart_sleep(delay):
	if delay > 0:
		for a in range(delay, 0, -1):
			print('{}\r'.format(center('Sleeping for {} seconds...'.format(str(a)), display=False)), end='')
			sleep(1)
		center('Sleeping for {} seconds complete!'.format(str(delay)))

def header():
	center(' ', clear=True)
	center('StockX to CSV by @DefNotAvg')
	center('-', '-')

def get_products(sku):
	response = session.get('https://stockx.com/api/browse?&_search={}&dataType=product'.format(sku), headers=headers)
	try:
		return response.json()['Products']
	except KeyError:
		return []

def get_market(product_id):
	result = []
	response = session.get('https://stockx.com/api/products/{}/activity?state=480&currency=USD&limit=1000000&page=1&sort=createdAt&order=DESC&country=US'.format(product_id), headers=headers)
	try:
		for item in response.json()['ProductActivity']:
			result.append({
					'Date': item['createdAt'].split('T')[0],
					'Time': item['createdAt'].split('T')[1].split('+')[0],
					'Size': item['shoeSize'],
					'Price': '${:.2f}'.format(item['amount']),
				})
		return result
	except KeyError:
		return []

header()
if len(sys.argv) > 1:
	for sku in sys.argv[1:]:
		session = requests.Session()
		print('{}\r'.format(center('[{}] Searching StockX for {}...'.format(smart_time(), sku), display=False)), end='')
		products = get_products(sku)
		if products:
			center('[{}] Successfully found product matching {}.'.format(smart_time(), sku))
			print('{}\r'.format(center('[{}] Gathering market data for {}...'.format(smart_time(), products[0]['title']), display=False)), end='')
			market = get_market(products[0]['id'])
			if market:
				center('[{}] Successfully gathered market data for {}.'.format(smart_time(), products[0]['title']))
				print('{}\r'.format(center('[{}] Writing market data to {}.csv...'.format(smart_time(), sku), display=False)), end='')
				with open(sku + '.csv', 'w') as csvfile:
					writer = csv.DictWriter(csvfile, fieldnames=list(market[0].keys()), lineterminator='\r')
					writer.writeheader()
					for data in market:
						writer.writerow(data)
				center('[{}] Successfully wrote market data to {}.csv.'.format(smart_time(), sku))
				urllib.request.urlretrieve(products[0]['media']['imageUrl'], sku + '.jpg')
				center('[{}] Successfully saved product image to {}.jpg.'.format(smart_time(), sku))
				product_overview = ''
				with open(sku + '.txt', 'w') as myfile:
					myfile.write('{}\n{}\n${}\n{}'.format(sku, products[0]['title'], products[0]['retailPrice'], products[0]['releaseDate'].split(' ')[0]))
				center('[{}] Successfully saved product overview to {}.txt.'.format(smart_time(), sku))
			else:
				center('[{}] Unable to get market data for {}.'.format(smart_time(), products[0]['title']))
		else:
			center('[{}] Unable to find product matching {}.'.format(smart_time(), sku))
else:
	center('[{}] Please provide a style code when running main.py.'.fomrat(smart_time()))