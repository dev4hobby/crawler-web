import csv
import datetime
import requests
from bs4 import BeautifulSoup
from pprint import pprint

class Crawler():
    def __init__(self):
        self.main_url = None
    
    def get_contents(self, url):
        self.request = requests.get(url)
        self.content = self.request.content
        try:
            self.soup = BeautifulSoup(self.content, 'html5lib')
        except:
            self.soup = BeautifulSoup(self.content, 'html.parser')
        finally:
            pass
        return self.soup

    def get_cafe_id(self, cafe_name):
        self.cafe_name = cafe_name.replace(' ','+')
        self.main_url = 'https://m.cafe.naver.com/SectionCafeSearch.nhn?query='+self.cafe_name+'&sortBy=0&option=&escrow=&onSale='
        self.soup = self.get_contents(self.main_url)
        self.cafe_name = self.soup.find_all('ul', class_='cafe_list')[0].find('a')['onclick']
        return self.cafe_name.split(',')[2].replace('\'','')

    def cafe(self, cafe_id, keyword):
        try:
            print(int(cafe_id))
        except: # Exception as e
            cafe_id = self.get_cafe_id(cafe_id)
        finally:
            # if data bad, set me free.
            print('cafe ID >> {}'.format(cafe_id))

        self.main_url = 'https://m.cafe.naver.com'
        self.url = self.main_url + '/ArticleSearchList.nhn?search.query=' + keyword + '&search.menuid=&search.searchBy=1&search.sortBy=date&search.clubid=' + cafe_id + '&search.option=0&search.defaultValue='
        self.soup = self.get_contents(self.url)
        self.item_list = self.soup.find('div', id='articleList').find_all('ul', class_='list_tit')[0].find_all('li')

        self.links = list()
        self.status = list()
        self.title = list()
        self.trader = list()
        self.time = list()

        for item in self.item_list:
            self.links.append(self.main_url+item.find('a')['href'])
            self.title.append(item.find('h3').text)
            if self.title[-1].startswith('[공식앱]'):
                self.status.append('공식앱')
            else:
                self.status.append(str(item.find('span', class_='icon_txt'))[-9:-7])
            self.trader.append(item.find('span', class_='name').text)
            self.time.append(item.find('span', class_='time').text)

        self.new_table = list(zip(self.links, self.status, self.title, self.trader, self.time))

        # test-begin
        self.now = str(datetime.datetime.now()).split('.')[0].replace(' ','_')
        with open(self.now+'.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(self.new_table)
        # test-end
        
        return self.new_table
