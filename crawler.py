import csv
import datetime
import requests
from bs4 import BeautifulSoup
from pprint import pprint

class Naver():
    def __init__(self):
        self.main_url = {'cafe' : 'https://m.cafe.naver.com',
                         'datalab' : 'https://datalab.naver.com'
                         }
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.89 Whale/1.6.81.16 Safari/537.36',
                        'From': 'acidlab.help@gmail.com'}
        self.soup = None
    
    def get_contents(self, url):
        request = requests.get(url, headers=self.headers)
        content = request.content
        try:
            soup = BeautifulSoup(content, 'html5lib')
        except:
            soup = BeautifulSoup(content, 'html.parser')
        finally:
            pass
        return soup

    def get_cafe_id(self, cafe_name):
        cafe_name = cafe_name.replace(' ','+')
        url = self.main_url['cafe']+'/SectionCafeSearch.nhn?query='+cafe_name+'&sortBy=0&option=&escrow=&onSale='
        self.soup = self.get_contents(url)
        cafe_name = self.soup.find_all('ul', class_='cafe_list')[0].find('a')['onclick']
        return cafe_name.split(',')[2].replace('\'','')

    def get_cafe_post(self, cafe_id, keyword):
        try:
            print(int(cafe_id))
        except: # Exception as e
            cafe_id = self.get_cafe_id(cafe_id)
        finally:
            # if data bad, set me free.
            print('cafe ID >> {}'.format(cafe_id))

        url = self.main_url + '/ArticleSearchList.nhn?search.query=' + keyword + '&search.menuid=&search.searchBy=1&search.sortBy=date&search.clubid=' + cafe_id + '&search.option=0&search.defaultValue='
        self.soup = self.get_contents(url)
        item_list = self.soup.find('div', id='articleList').find_all('ul', class_='list_tit')[0].find_all('li')

        links = list()
        status = list()
        title = list()
        trader = list()
        time = list()

        for item in item_list:
            links.append(self.main_url+item.find('a')['href'])
            title.append(item.find('h3').text)

            if title[-1].startswith('[공식앱]'):
                status.append('공식앱')
            else:
                status.append(str(item.find('span', class_='icon_txt'))[-9:-7])

            trader.append(item.find('span', class_='name').text)
            time.append(item.find('span', class_='time').text)

        new_table = list(zip(links, status, title, trader, time))

        # test-begin
        now = str(datetime.datetime.now()).split('.')[0].replace(' ','_')
        with open(now+'.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(new_table)
        # test-end
        
        return new_table

    def get_trend(self, rank=20, age=0):
        self.url = self.main_url['datalab']+'/keyword/realtimeList.naver?where=main'
        self.soup = self.get_contents(self.url)
        trends = self.soup.find_all('div', class_='rank_inner')
        try:
            age = int(age) // 10
        except: # maybe index error or unknown age
            age = 0
        finally:
            pass
        trends = trends[age].find_all('span', class_='title')
        trends = [keyword.text for keyword in trends]
        return trends[:rank]
