import os
import sys
import csv
import time
import urllib
import datetime
import requests # pip install requests
from fake_useragent import UserAgent # pip install fake-useragent
from bs4 import BeautifulSoup # pip install beautifulsoup4
from pprint import pprint
from lxml.html import fromstring # pip install lxml
from selenium import webdriver # pip install selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class Crawl():
    def __init__(self):
        self.headers = {'User-Agent': UserAgent().random,
                        'From': 'acidlab.help@gmail.com'}
    
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
        self.main_url = {'cafe' : 'https://m.cafe.naver.com',
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

class Google(Crawl):
    def __init__(self):
        super().__init__()
        self.main_url = {'main' : 'https://google.com',}
        self.soup = None
    
    def get_images_url(self, page_url, step=3):
        options = webdriver.FirefoxOptions()
        options.add_argument('headless')
        options.add_argument('disable-gpu')
        driver = webdriver.Firefox(options=options)
        driver.get(page_url)
        driver.implicitly_wait(2)
        html = driver.find_element_by_tag_name('body')
        for i in range(step):
            print("image crawling...")
            for j in range(30):
                html.send_keys(Keys.PAGE_DOWN)
                time.sleep(0.5)
            try:
                driver.execute_script('document.getElementById("smc").style.display="block";')
                time.sleep(2)
                driver.find_element_by_id('smb').click()
            except:
                print("something goes wrong...")
                source = driver.page_source
                driver.quit()
                return source
            print('Progress >> {}/{}'.format(i, step))
        time.sleep(2)
        source = driver.page_source
        driver.quit()
        return source
    
    def get_images_as_file(self, link):
        try:
            request = requests.get(self.main_url['main']+link.get('href'), headers=self.headers)
        except:
            print('cannot get link.')
        title = str(fromstring(request.content).findtext('.//title'))
        link = title.split(" ")[-1]
        print("At: " + os.getcwd() + ", Downloading from " + link)
        try:
            if link.split(".")[-1] == ('jpg' or 'png' or 'jpeg'):
                urllib.urlretrieve(link, link.split("/")[-1])
        except:
            print('failed')


    def get_images(self, keyword):
        try:
            sys.setrecursionlimit(pow(10,6))
            search_page = self.main_url['main'] + '/search?q='+keyword+'&source=lnms&tbm=isch&sa=X&ved=0ahUKEwjEzJnD3fbcAhUMO3AKHfLyCkkQ_AUICigB'
            content = self.get_images_url(search_page)
            self.soup = BeautifulSoup(str(content), 'html.parser')
            if not os.path.isdir(keyword):
                os.makedirs(keyword)
            os.chdir(str(os.getcwd()) + '/' + str(keyword))
            links= self.soup.find_all('a', class_='rg_l')
            self.get_images_as_file(links)
        except Exception as e:
            print(e)
            print('failed to get_images')
        finally:
            sys.setrecursionlimit(pow(10,3))
