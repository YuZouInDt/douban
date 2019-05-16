#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 17:07:52 2017

@author: jeff
"""

import requests
import codecs
from bs4 import  BeautifulSoup
import re
from time import sleep
#change it to your movie page
DOWNLOAD_URL = 'https://movie.douban.com/people/138660941/collect'

HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
}

def download_page(url):
    data = requests.get(url, headers = HEADERS).content
    return data

movie_name_list = []
movie_poster_list = []
movie_rating_list = []

def parse_html(html):
    soup = BeautifulSoup(html, "lxml")
    movie_list_soup = soup.find_all('div', {'class': 'item'})
    
    for items in movie_list_soup:
        date = items.find('span', {'class': 'date'}).getText().strip()
        if date[0:4] == "2018":
            movie_name = items.find('li', {'class': 'title'}).getText().split('/')[0].strip()
            movie_name_list.append(movie_name)
            movie_rating = items.find('span', {'class':re.compile(r"rating.*")})
            if movie_rating:
                movie_rating = movie_rating['class'][0][6]
            else:
#            标记但未评分的电影视为0星，可修改
                movie_rating = '0'
            movie_rating_list.append(movie_rating)
            movie_poster = items.find('img')['src']
            movie_poster_list.append(movie_poster)
            print(movie_name, movie_rating)
        if date[0:4] != "2018":
            return None

    next_page = soup.find('span', {'class': 'next'})

    if next_page:
        next_page = next_page.find('a')
        return "https://movie.douban.com" + next_page['href']

    return None
   
status = parse_html(download_page(DOWNLOAD_URL))
while status:
    status = parse_html(download_page(status))
    sleep(1)

poster=open("poster_2018.html","w",encoding="utf-8")
#html头，可修改width和height改变图片大小，修改brightness改变每种评星电影海报的亮度
string = """<html>
 <head>
  <title>Poster</title>
  <style>
  *{margin:0;padding:0;}
  .ai{white-space: nowrap}
.aixuexi0{position:relative;display: inline-block;width:100px;height:136px;background-color:black;background-size:cover;filter:brightness(0.2);white-space:nowrap;overflow-x:scroll;}
.aixuexi1{position:relative;display: inline-block;width:100px;height:136px;background-color:black;background-size:cover;filter:brightness(0.2);white-space:nowrap;overflow-x:scroll;}
.aixuexi2{position:relative;display: inline-block;width:100px;height:136px;background-color:black;background-size:cover;filter:brightness(0.3);white-space:nowrap;overflow-x:scroll;}
.aixuexi3{position:relative;display: inline-block;width:100px;height:136px;background-color:black;background-size:cover;filter:brightness(0.5);white-space:nowrap;overflow-x:scroll;}
.aixuexi4{position:relative;display: inline-block;width:100px;height:136px;background-color:black;background-size:cover;filter:brightness(0.65);white-space:nowrap;overflow-x:scroll;}
.aixuexi5{position:relative;display: inline-block;width:100px;height:136px;background-color:black;background-size:cover;filter:brightness(1);white-space:nowrap;overflow-x:scroll;}
  </style>
 </head>
 <body>
<div class="ai">"""
poster.write(string)

for i in range(len(movie_name_list)):
    string = '<div class="aixuexi' + movie_rating_list[i] + '" name='+ '"' + movie_name_list[i] + '"style="background-image:url(' + "'" + movie_poster_list[i] + "'" + ');"></div>'
#    string='<div class="aixuexi' + b[i] + '">' + '<img alt="'+a[i]+'" src="'+c[i]+'"/></div>'
    poster.write(string)
#    每行25张海报
    if (i+1)%25 ==0:
        poster.write('</br>')

poster.write("</div></body></html>")  
poster.close()

#浏览器打开生成的html，截图

