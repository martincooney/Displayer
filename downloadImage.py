#downloaded from https://github.com/hardikvasa/google-images-download/blob/master/google-images-download.py

'''
The MIT License (MIT)

Copyright (c) 2015 Hardik Vasa

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
'''
Modified by Martin Cooney 2017-11-27
Same terms as above apply (MIT license).
'''

import time       #Importing the time library to check the time of code execution
import sys    #Importing the System Library
import os
import urllib2


keywords = [' high resolution']

#Downloading entire Web Document (Raw Page Content)
def download_page(url):
    version = (3,0)
    cur_version = sys.version_info
    if cur_version >= version:     #If the Current Version of Python is 3.0 or above
        import urllib.request    #urllib library for Extracting web pages
        try:
            headers = {}
            headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
            req = urllib.request.Request(url, headers = headers)
            resp = urllib.request.urlopen(req)
            respData = str(resp.read())
            return respData
        except Exception as e:
            print(str(e))
    else:                        #If the Current Version of Python is 2.x
        import urllib2
        try:
            headers = {}
            headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
            req = urllib2.Request(url, headers = headers)
            response = urllib2.urlopen(req)
            page = response.read()
            return page
        except:
            return"Page Not found"


#Finding 'Next Image' from the given raw page
def _images_get_next_item(s):
    start_line = s.find('rg_di')
    if start_line == -1:    #If no links are found then give an error!
        end_quote = 0
        link = "no_links"
        return link, end_quote
    else:
        start_line = s.find('"class="rg_meta"')
        start_content = s.find('"ou"',start_line+1)
        end_content = s.find(',"ow"',start_content+1)
        content_raw = str(s[start_content+6:end_content-1])
        return content_raw, end_content


#Getting all links with the help of '_images_get_next_image'
def _images_get_all_items(page):
    items = []
    counter=0
    jpgCounter = 0
    while True:
        item, end_content = _images_get_next_item(page)
        if item == "no_links" or counter==10 or jpgCounter==3:#3
            break
        else:
            items.append(item)      #Append all the links in the list named 'Links'
            time.sleep(0.1)        #Timer could be used to slow down the request for image downloads
            page = page[end_content:]
            counter=counter+1
	    if item.endswith("jpg"):
		jpgCounter=jpgCounter+1


    return items


############## Main Program ############
t0 = time.time()   #start the timer

#Download Image Links
search_keyword = [ ]

#read in a keyword to search for
f=open("/home/turtlebot/ros_ws/src/hpc/my_keyword.txt", 'r') #CHANGE this to whatever location you use
l=list(f)
f.close()
search_keyword.append(l[0].rstrip())

i= 0
while i<len(search_keyword):
    items = []
    iteration = "Item no.: " + str(i+1) + " -->" + " Item name = " + str(search_keyword[i])
    print (iteration)
    print ("Evaluating...")
    search_keywords = search_keyword[i]
    search = search_keywords.replace(' ','%20')
    image_folder =  "/home/turtlebot/ros_ws/src/hpc/images/%s" % search_keywords #CHANGE this to whatever location you use
    try:
        os.makedirs(image_folder)
    except OSError, e:
        if e.errno != 17:
            raise   
        # time.sleep might help here
        pass
    
    j = 0
    while j<len(keywords):
        pure_keyword = keywords[j].replace(' ','%20')
        url = 'https://www.google.com/search?q=' + search + pure_keyword + '&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg'
        raw_html =  (download_page(url))
        time.sleep(0.1)
        items = items + (_images_get_all_items(raw_html))
        j = j + 1
    print ("Total Image Links = "+str(len(items)))
    print ("\n")

    t1 = time.time()    #stop the timer
    total_time = t1-t0   #Calculating the total time required to crawl, find and download all the links of 60,000 images
    print("Total time taken: "+str(total_time)+" Seconds")
    print ("Starting Download...")

    k=0
    from urllib2 import Request,urlopen
    from urllib2 import URLError, HTTPError
    
    weDontHaveAnImage = True
    while(weDontHaveAnImage):

	errorCount=0
	print k, items[k]
	endPart= items[k][-3:]

        try:
            req = Request(items[k], headers={"User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"})
            response = urlopen(req,None,15)

            if not (endPart == "jpg" or endPart == "png"):
		#try one last time to see if we are getting a jpg or not...
		if items[k].find('jpg') != -1:
			endPart='jpg'
		elif items[k].find('png') != -1:
			endPart='png'		
		else:
 			k=k+1
			continue

            output_file = open(image_folder+"/1."+endPart,'wb')


            data = response.read()
            output_file.write(data)
            response.close();

            print("completed ====> "+str(k+1))

            k=k+1


        except IOError:   #If there is any IOError

            errorCount+=1
            print("IOError on image "+str(k+1))
            k=k+1

        except HTTPError as e:  #If there is any HTTPError

            errorCount+=1
            print("HTTPError"+str(k))
            k=k+1
        except URLError as e:

            errorCount+=1
            print("URLError "+str(k))
            k=k+1

	if(k >= len(items)):
	    print "Failed, sorry"
	    break
	if(errorCount ==0):
	    weDontHaveAnImage = False

    i = i+1


print("\n")
print("Everything downloaded!")
print("\n"+str(errorCount)+" ----> total Errors")




