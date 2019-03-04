# The MIT License (MIT)

# Copyright (c) 2015 Hardik Vasa

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# Wikipedia Crawler v3 (inserting results into MySQL)
# @author: Hardik Vasa
# Small part of the original code is used

#Import Libraries
import time     #For Delay
import urllib.request    #Extracting web pages
import re
import pandas as pd
import json

#Downloading entire Web Document (Raw Page Content)
def download_page(url):
    try:
        headers = {}
        headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        req = urllib.request.Request(url, headers = headers)
        resp = urllib.request.urlopen(req)
        respData = str(resp.read())
        return respData
    except Exception as e:
        print(str(e))
        print(url.split('/')[-1])
        return 'shabi'


#Extract just the Introduction part of the page
def extract_introduction(page):
    start_introduction = page.find("<p>")
    stop_introduction = page.find('<div id="toctitle">', start_introduction + 1)

    #If the page onl has introduction
    if '<div id="toctitle">' not in page:
        stop_introduction = page.find('</p>', start_introduction + 1)
    else:
        pass

    raw_introduction = page[start_introduction : stop_introduction]
    return raw_introduction


#Remove all the HTML tags from the introduction to get the pure text
#Eliminate all the text inside '<' & '>'
def extract_pure_introduction(page):
    pure_introduction = (re.sub(r'<.+?>', '', page))       #From '<' to the next '>'
    return pure_introduction


#Main Crawl function that calls all the above function and crawls the entire site sequentially
def get_introduction(url):
    raw_html = download_page(url)
    if raw_html == 'shabi':
        return "None"
    raw_introduction = extract_introduction(raw_html)
    pure_introduction = extract_pure_introduction(raw_introduction)
    return pure_introduction


df = pd.read_csv('label_foodtype.csv', header=None, names=['id', 'name'])
recipe_name = [re.sub(r'\s+', '_', x.strip()) for x in df['name']]
url_prefix = "https://en.wikipedia.org/wiki/"
text = {}
for each in recipe_name:
    url = url_prefix + each
    intro = get_introduction(url)
    text[each] = intro
    time.sleep(2)

with open('wiki.json', 'w') as f:
    json.dump(text, f)

