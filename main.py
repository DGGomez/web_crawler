from html.parser import HTMLParser  
from urllib.request import urlopen  
from urllib import parse

import time
start = time.process_time()



class MyHTMLParser(HTMLParser):
    count = 0
    def handle_starttag(self, tag, attrs):
        if tag == 'span':
            for attribute in attrs:
                attribute_name = attribute[0]
                attribute_value = attribute[1]

                if (attribute_value.find('cms-article-list--article') != -1):
                    print ("start: " + tag)
            
    # def handle_endtag(self, tag):
    #     # print("End: "+ tag)

    def handle_data(self, data):
        print(data)
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
parser.feed("""<html>
<span>
    <span class="cms-article-list--article"><a>123</a></span>
    <span class="cms-article-list--article">456</span>
</span>
</html>""")

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
