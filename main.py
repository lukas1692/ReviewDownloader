'''
Created on 23.05.2017

@author: Lukas
'''
#from urllib.request import urlopen

import urllib.request

import os
import re



#if __name__ == '__main__':
    #html = urlopen("http://www.ign.com/search?q=atmosphere&page=0&count=10&type=article&filter=articles&")
    #print(html.read())
    
    #os.system('D:\Lukas\wkhtmltopdf D:\Lukas\IGN.html D:\Lukas\WebPage.pdf')
    #print("finished")

    #pass

import json
import re
from lib2to3.patcomp import pattern_convert
from asyncore import write
import sys

unknown_title = 1

ign_reviews =  {}

api_endpoint = 'http://selectpdf.com/api2/convert/'
#key = 'ca5bcabc-bac3-4f36-af4b-e3a043b2a7e7'
key = '!insert your key here!'
write_pdf = False

def ign_review():
    test_url = 'http://www.ign.com/games/reviews'
    i = 0
    while(1):
        response = urllib.request.urlopen(test_url+"?startIndex="+ str(i) +"&time=5y#")
        
        print(test_url+str(i))
        if response is None:
            break
        headers = response.info()
        data = response.read().decode('utf-8')
        
        pattern = '<a href=".*">Review</a>'
        
        matches = re.findall(pattern, data) 
        
        searchIGNResultPage(matches)
        
        i += 25
        
        if(len(matches) == 0):
            print("finished")
            break
    
def searchIGNResultPage(matches):

    for b in matches:
        
        
        link = re.search('"http://www.ign.com/.*"', b)
        link = link.group(0).replace('"','')
        
        if(link not in ign_reviews):
            ign_reviews[link] = 1
        else:
            continue
            
        response = urllib.request.urlopen(link)
        data = response.read().decode('utf-8')
        
        if(data.find("atmosphere") == -1 and data.find("Atmosphere") == -1):
            continue
        
        title = link.split("/")[-1]
        html_file = open("ign/"+title+".html","w")
        html_file.write(data)
        html_file.close()
        
        if not write_pdf:
            continue
            
        try:
            request = urllib.request.Request(api_endpoint)
            request.add_header('Content-Type', 'application/json')
            print("open")
            result = urllib.request.urlopen('http://selectpdf.com/api2/convert/?key='+ key + '&url=' + link + '')
            localFile = open("ign_pdf/"+title+".pdf", 'wb')
            localFile.write(result.read())
            localFile.close()
            print("Test pdf document generated successfully!")
        except:
            print("An error occurred!")

def polygon_review():

    #test_url = 'http://www.pcgamer.com/search/?searchTerm=atmosphere'
    test_url = 'https://www.polygon.com/games/reviewed/'
    local_file = 'test.pdf'
    
    # parameters - add here any needed API parameter 
    parameters = {
        'key': key,
        'url': test_url
    }
    
    i = 1
    while(1):
        response = urllib.request.urlopen(test_url+str(i))
        
        print(test_url+str(i))
        if response is None:
            break
        headers = response.info()
        data = response.read().decode('utf-8')
        
        pattern = '<a class="review_link" href=".*>'
        #found = re.search(pattern, data)
    
        matches = re.findall(pattern, data)    
        searchPolygonResultPage(matches)
        i+=1
        
        if(len(matches) == 0):
            print("finished")
            break
    
        pass
    
def searchPolygonResultPage(matches):
    for x in matches:
        link = re.search('"https://www.polygon.com/.*"', x)
        link = link.group(0).replace('"','')
        #print(link)
        
        response = urllib.request.urlopen(link)
        data = response.read().decode('utf-8')
        
        if(data.find("atmosphere") == -1 and data.find("Atmosphere") == -1):
            continue
        
        pattern = '<dd>....-..-..</dd>*'
        response_date_t = re.findall(pattern,data,re.M)
        if len(response_date_t) > 1:
            response_date = response_date_t[0]
            response_date = response_date.replace("<dd>","")
            response_date = response_date.replace("</dd>","")
        
            if(int(response_date[:4]) < 2006):
                continue
        
        try:
            title = link.split("/")[-1]
            html_file = open("polygon/"+title+".html","w")
            html_file.write(data)
            html_file.close()
        except:
            html_file.close()
            cwd = os.getcwd()
            path = (cwd+'/polygon/'+title+'.html').replace('/','\\')
            print("cant write file: " + path)
            os.remove(path)
        
        if not write_pdf:
            continue
        try:
            request = urllib.request.Request(api_endpoint)
            request.add_header('Content-Type', 'application/json')
            print("open")
            result = urllib.request.urlopen('http://selectpdf.com/api2/convert/?key='+ key + '&url=' + link + '')
            localFile = open("polygon_pdf/"+title+".pdf", 'wb')
            localFile.write(result.read())
            localFile.close()
            print("Test pdf document generated successfully!")
        except:
            print("An error occurred!")   
        
    pass
  
if __name__ == '__main__':
    polygon_review()
    #ign_review()
    

