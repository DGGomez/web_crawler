from html.parser import HTMLParser  
from urllib.request import urlopen  
from urllib import parse

import time
start = time.process_time()

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print("Encountered a start tag:"+ tag)

    def handle_endtag(self, tag):
        print("Encountered an end tag :"+ tag)

    def handle_data(self, data):
        print("Encountered some data  :"+ data)
        
K = 10
pages = {}
content = []
links = []
# define topic: Workout

# search for workout information
name = 'bodybuilding'
url = 'https://www.bodybuilding.com/category/workouts'

# get initial web pages
response = urlopen(url)
htmlBytes = response.read()
htmlString = htmlBytes.decode("utf-8")

try:

    print(" **Success!**")
except:
    print(" **Failed!**")

parser = MyHTMLParser()
parser.feed(response)

# check similarity (pick threshold value)

# check robot.txt

# stop crawling

# write results
fileOut = open("results.txt", "w+")
for key in pages:
    fileOut.write(key+": "+str(pages[key])+"\n")
fileOut.close()

# time taken
print(time.process_time() - start)
