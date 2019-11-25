from html.parser import HTMLParser  
from urllib.request import urlopen as uReq
from urllib import parse
import urllib.request
import bs4
from bs4 import BeautifulSoup as soup
import math
import re
import sys
import time
import traceback
import random

headers = {
    'User-Agent': 'My User Agent 1.0',
    'From': 'youremail@domain.com'
}

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
oldPages = {}
robot = {}
postings = {}
frequencyList = {}

# web crawler arrays
content = []
links = []
visited = []

# similarity testing arrays
wordList = []
numberLists = []
numberList = []

#passList = []

# define topic: Workout
name = 'workout'
start_url = ["https://www.t-nation.com","https://www.bodybuilding.com/category/workouts","https://www.menshealth.com/uk/workouts"]
robot_url = ['https://www.t-nation.com/robots.txt', 'https://www.bodybuilding.com/robots.txt', 'https://www.menshealth.com/robots.txt']

# get initial web pages
try:
    print("Getting Intial Data")
    for num in range(len(start_url)):
        # fetch website
        myUrl = start_url[num]
        req = urllib.request.Request(myUrl, headers = headers)
        uClient = uReq(req)
        page_html = uClient.read()
        uClient.close()

        visited.append(myUrl)
        # get robot list for initial website
        myUrl2 = robot_url[num]
        req2 = urllib.request.Request(myUrl2, headers = headers)
        uClient2 = uReq(req2)
        page_html2 = uClient2.read()
        uClient2.close()
        p = page_html2.splitlines()
        disallowed = []

        for i in p:
            val = str(i)
            if "Disallow" in val:
                vals = val.split(" ")
                if len(val[1]) <2:
                    continue
                disallowed.append(vals[1][:-1])

        robot[myUrl2] = disallowed

        # generate dictionary
        page_soup = soup(page_html, "html.parser")
        for i in page_soup.findAll("a", href=True):
            a = i['href']
            if "forum" in a:
                continue
            if "forums" in a:
                continue
            if "search" in a:
                continue
            if "facebook" in a:
                continue  
            if "pinterest" in a:
                continue  
            if "youtube" in a:
                continue  
            if "instagram" in a:
                continue           
            if "www" not in a:
                continue            
            if "//" not in a:
                continue

            if "http:" in a:
                continue

            if a not in links:
                links.append(a)

        for i in page_soup.find_all('div'):
            words = i.get_text().split(" ")
            for word in words:

                # filter word
                if word == '':
                    continue
                word = re.sub(r'\W+', '', word.rstrip()).lower()

                # store in wordList
                if word in wordList:
                    index = wordList.index(word)
                    numberList[index] += 1
                    postings[word] += 1
                else:
                    wordList.append(word)
                    numberList.append(1)
                    postings[word] = 1

    # sim logic

    # remove low idf values
    # for line in postings:
    #     idf = math.log(3/int(postings[line]))
    #     if idf >= 0.3:
    #         passList.append(line)
    #     val = postings[line]
    #     frequencyList[line] = [val,idf]

    # wq = []
    # wadjusted = []
    # # get query weights
    # for i in range(len(numberList)):
    #     if numberList[i] > 0:            
    #         # fetch frequency
    #         tfi = tf(numberList[i])
    #         idf = frequencyList.get(wordList[i])
    #         if(idf == None):
    #             continue
    #         wq.append(w(tfi, idf[1]))
    #     else:
    #         wq.append(0)

    # go through links and check similarity
    done = 0
    holder = links
    while(done <len(links)):
        done +=1
        search = random.randint(0,len(holder)-1)
        a = holder[search]
        holder.pop(search)
        # skips
        if "https:" not in a:
            a = "https:"+a

        if a in visited:
            continue

        print("Checking link: " + str(a))
        # time delay 10 second
        time.sleep(10)
        # check robot.txt
        if "https://" in a:
            url = a[8:].split("/")
            urlRobot = "https://"+url[0]+"/robots.txt"
            # check if already been checked
            if urlRobot in robot:
                # if exists check if url in restrictions
                size = len("https://"+url[0])
                endpoint = a[size:]
                # skip if endpoint in robot files
                if endpoint in robot[urlRobot]:
                    continue
            else:
                # add links if robot not exist
                req = urllib.request.Request(urlRobot, headers = headers)
                uClient = uReq(req)
                page_html = uClient.read()
                uClient.close()
                p = page_html.splitlines()
                for i in p:
                    val = str(i)
                    if "Disallow" in val:
                        vals = val.split(" ")
                        if val[1] == " ":
                            continue
                        disallowed.append(vals[1][:-1])

                robot[myUrl2] = disallowed
        else:
            continue

        # read data
        req = urllib.request.Request(a, headers = headers)
        uClient = uReq(req)
        page_html = uClient.read()
        uClient.close()
        visited.append(a)

        # get values
        page_soup = soup(page_html, "html.parser")
        
        # add pages links to link to links array??
        # links = page_soup.findAll("a", href=True)

        # extract info
        pageNumberList = [0]* len(wordList)
        content = ""
        for i in page_soup.find_all('div'):
            # get page info and store
            words = i.get_text().split(" ")

            for word in words:
                # filter word
                if word == '':
                    continue
                word = re.sub(r'\W+', '', word.rstrip()).lower()
                content+=word+" "
                # store in wordList
                if word in wordList:
                    index = wordList.index(word)
                    pageNumberList[index] += 1

        # check similarity
        wi = []
        threshold = 0.30
        checkVals = 0
        numberVal = len(numberList)
        # get document list and check k-rating
        for j in range(len(pageNumberList)):
             # contains 90% of query values
            if int(pageNumberList[j]) > 0 and int(numberList[j]) > 0:
                checkVals+=1

        if (checkVals/numberVal) >threshold:
            # add to list

            pages[a] = content
        else:
            # if we run out of links and still haven't found review old content
            oldPages[checkVals/numberVal] = [a,content]

        # stop crawling
        if len(pages) >= K:
            break
    
    # take top k - len(pages) of oldPages
    if len(pages) != K:
        for key in sorted(oldPages.keys()):
            if len(pages) < K:
                val = oldPages[key][0]
                cont = oldPages[key][1]
                pages[val] = cont
            else:
                break

except Exception:
    traceback.print_exc()

print(len(links))
# write results
fileOut = open("results.txt", "w+")
for key in pages:
    fileOut.write(str(key)+": "+str(pages[key])+"\n")
fileOut.close()

# time taken
print(time.process_time() - start)
