from html.parser import HTMLParser  
from urllib.request import urlopen as uReq
from urllib import parse
import bs4
from bs4 import BeautifulSoup as soup
import math
import re
import sys
import time

def contains_digits(s):
    return any(char.isdigit() for char in s)

def tf(f):
    return 1 + math.log(f)

def w(tf, idf):
    return tf * idf

def sim(wi,wq):

    di = 0
    dNi = 0
    dNq = 0
    size = 0
    if len(wi) > len(wq):
        size = len(wq)
    else:
        size = len(wi)
    for i in range(size):
        di += wi[i] * wq[i]
        dNi += wi[i] * wi[i]
        dNq += wq[i] * wq[i]
    dNi = math.sqrt(dNi)
    dNq = math.sqrt(dNq)
    return ((di)/(dNi*dNq))

start = time.process_time()

K = 10
pages = {}
robot = {}
content = []
links = []
wordList = []
numberList = []
# define topic: Workout
name = 'bodybuilding'

# get initial web pages
try:
    myUrl = 'https://www.bodybuilding.com/category/workouts'
    uClient = uReq(myUrl)
    page_html = uClient.read()
    uClient.close()
    print(" **Success!**")

    # generate dictionary
    page_soup = soup(page_html, "html.parser")
    links = page_soup.findAll("a", href=True)

    for i in page_soup:
        for word in i:
            if word in wordList:
                index = wordList.index(word)
                numberList[index] += 1
            else:
                wordList.append(word)
                numberList.append(1)
    
    # go through links and check similarity
    for a in links:
        # check robot.txt
        if "https://" in a:
            url = a[8:].split("/")
            urlRobot = url[0]+"/robots.txt"
            # check if already been checked
            uClient = uReq(urlRobot)
            page_html = uClient.read()
            uClient.close()
        else:
            continue
        # read data
        uClient = uReq(a)
        page_html = uClient.read()
        uClient.close()

        # get values
        page_soup = soup(page_html, "html.parser")
        # links = page_soup.findAll("a", href=True)

        # check similarity (pick threshold value)

        # stop crawling
        if len(pages) >= K:
            break
except:
    print(" **Failed!**")

# write results
fileOut = open("results.txt", "w+")
for key in pages:
    fileOut.write(key+": "+str(pages[key])+"\n")
fileOut.close()

# time taken
print(time.process_time() - start)
