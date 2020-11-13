import os
import sys
import csv
import time
import wget
import shutil
import urllib
import zipfile
import datetime
import platform
import requests # pip install requests
from fake_useragent import UserAgent # pip install fake-useragent
from bs4 import BeautifulSoup # pip install beautifulsoup4
from pprint import pprint
from lxml.html import fromstring # pip install lxml
from pyvirtualdisplay import Display
from multiprocessing import Pool

class Crawl():
    def __init__(self):
        self.headers = {'User-Agent': UserAgent().random,
                        'From': 'hello_world@domain.com'}

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

class Naver(Crawl):
    def __init__(self):
        super().__init__()
        self.main_url = {'search' : 'https://search.naver.com/search.naver?ie=utf8&query=',
                         'cafe' : 'https://m.cafe.naver.com',
                         'datalab' : 'https://m.datalab.naver.com',}
        self.soup = None

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

        url = self.main_url['cafe'] + '/ArticleSearchList.nhn?search.query=' + keyword + '&search.menuid=&search.searchBy=1&search.sortBy=date&search.clubid=' + cafe_id + '&search.option=0&search.defaultValue='
        self.soup = self.get_contents(url)
        item_list = self.soup.find('div', id='articleList').find_all('ul', class_='list_tit')[0].find_all('li')

        links = list()
        status = list()
        title = list()
        trader = list()
        time = list()

        for item in item_list:
            links.append(self.main_url['cafe']+item.find('a')['href'])
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

    def get_trend_keyword(self, rank=20, age=0):
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
    
    def get_weather(self, spot, raw_option=True):
        spot += '+날씨'
        try:
            self.url = self.main_url['search']+spot
            self.soup = self.get_contents(self.url)
            result = [self.soup.find('span', class_='btn_select').find('em').text,
                      self.soup.find('p', class_='info_temperature').find('span', class_='todaytemp').text,
                      self.soup.find('p', class_='cast_txt').text]
            if raw_option:
                return result
            else:
                return '현재 ' + result[0] + '의 기온은 ' + result[1] + '도 입니다. \n[ ' + result[2] + ' ]'
        except:
            return '죄송합니다. 관련 정보가 없습니다.\n감사합니다.'

class Google(Crawl):
    def __init__(self):
        super().__init__()
        self.main_url = {'main' : 'https://google.com',}
        self.soup = None
   
    def get_microdust(self):
        pass

class PPU(Crawl):
    def __init__(self):
        super().__init__()
        self.main_url = {'forum' : 'http://www.ppomppu.co.kr/zboard/zboard.php?id=',}
        self.soup = None
    
    def get_forum_oversea_title(self, keyword):
        self.soup = self.get_contents(self.main_url['forum']+'oversea')
        check_first_title = self.soup.find('table', id='revolution_main_table').find('tbody').find_all('tr')[38].find_all('td')[3].find('a').text

        #print('현재 필터링중인 키워드 >> '+ str(keyword))
        return check_first_title 

