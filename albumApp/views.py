from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


#wev clawer
import selenium.webdriver
from bs4 import BeautifulSoup
import re
import os
import urllib.request
import json
from urllib.parse import quote
import time
import json
import socket
from selenium.webdriver.common.keys import Keys
import threading
#
from django.core.exceptions import MiddlewareNotUsed
from django.conf import settings
# csrf pass
from django.views.decorators.csrf import csrf_exempt
import chromedriver_binary
from pyvirtualdisplay import Display

def scrollTo():
    return 'window.scrollTo(0, document.body.scrollHeight)'



def index(request):
    global driver
    try:
        if driver :
            print('pass')
    except:
        display = Display(visible=0, size=(1280, 720))  
        display.start()
        driver = selenium.webdriver.Chrome()
    return render(request, 'albumApp/index.html')

@csrf_exempt
def upUrl(request):
    reg = 'https://twitter.com/(.*?)/'
    reg = re.compile(reg)
    url_receive = request.POST['url']+"/"
    _id = re.findall(reg,url_receive)
    url = 'https://twitter.com/' + _id[0] + '/media'
    print(url)
    global driver,handles
#     js='window.open("'+ url +'");'
#     driver.execute_script(js)
    driver.get(url)
    handle = driver.window_handles[-1]
    content = {'handle':handle }
    global idx
    idx= 0
    return render(request, 'albumApp/main.html' ,content)


@csrf_exempt
def jq(request):
    print(request.POST['name'])
    global idx,driver
#     driver.switch_to_window(request.POST['name'])
    soup = BeautifulSoup(driver.page_source,'html.parser')
    img_list=[]
    date_list=[]
    month_list=[]
    tweet=soup.find_all('',{'data-item-type' : 'tweet'})
    for i in range(len(tweet)):
        html =str(tweet[i])

        reg = 'img.*?data-aria-label-part.*?(https.*?)"'
        reg = re.compile(reg)

        date_reg = 'class="tweet-timestamp.*?title="(.*?)"'
        date_reg = re.compile(date_reg)

        month_reg = '年(.*?)月.*?日'
        month_reg = re.compile(month_reg)

        img = re.findall(reg,html)
        date = re.findall(date_reg,html)
        month = re.findall(month_reg,html)
        img_list.append(img)
        date_list.append(date)
        month_list.append(month)
    global content
    content = {'img_list':img_list , 'date_list':date_list , 'month_list':month_list }
    idx = len(date_list)
    print(scrollTo())
    driver.execute_script(scrollTo())
    return HttpResponse(json.dumps(content))



