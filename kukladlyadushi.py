import time
import requests
from bs4 import BeautifulSoup





headers = {
	'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'
	}

f = open('links.txt', 'w')

def get_page(page_number,headers):
	url = 'https://kukladlyadushi.ru/page/{}/'.format(page_number)
	r = requests.get(url,headers = headers)
	return r.text

def get_links(html,headers):

	soup = BeautifulSoup(html, 'html.parser')
	links_to_ali = soup.find_all('a',{'class':'button product_type_external'})
	


	for l in links_to_ali:

		link =l.get('href')
		link_k = l.previous_sibling.get('href')

		
		if lack_of_goods(link,headers):
			f.write(link_k+'\n')

			
			print('Ссылка недоступна: ' + str(link_k))
		else:
			pass
			#print(link_k + ' доступна')
			
		
		


def get_number_pages():

	html = get_page(1,headers)
	soup = BeautifulSoup(html, 'html.parser')

	number_pages = soup.find('ul',{'class':'page-numbers'}).find_all('a',{'class':'page-numbers'})[-2].get_text()
	

	return number_pages


def lack_of_goods(url,headers):
	r = requests.get(url,headers = headers)
	soup_ali = BeautifulSoup(r.text, 'html.parser')
	
	lack_of_goods = soup_ali.find('title').get_text()
	if 'Not Found' in lack_of_goods:
		return url
	else:
		return False
	time.sleep(2)
	





		



if __name__ == '__main__':

	user_input = input('Для проверки всего диапазона страниц введите 1, если хотите задать свой диапазон введите 2:  ')

	if user_input == str(1):
		page_num = int(get_number_pages())

		for i in range(page_num):
			print('Страница ' + str(i+1) + ' из '+ str(get_number_pages()))

			get_links(get_page(i+1,headers),headers)
		
			time.sleep(1)
		f.close()

	elif user_input == str(2):
		first_page = int(input('Ведите первую страницу диапазона:  '))
		last_page = int(input('Ведите последнюю страницу диапазона:  '))

		for i in range(first_page,last_page+1):
			print('Страница ' + str(i) + ' из '+ str(get_number_pages()))

			get_links(get_page(i,headers),headers)
		
			time.sleep(1)
		f.close()

	else:
		print('Вы ввели неверное значение')
		exit()



	



