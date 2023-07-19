import urllib
import time
from lxml import etree
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
import json
from bs4 import BeautifulSoup
from urllib import request
import json
import os


#该方法用来确认元素是否存在，如果存在返回flag=true，否则返回false
def isElementExist(browser, xpath):
    flag=True
    try:
        browser.find_element_by_xpath(xpath)
        return flag
    except:
        flag = False
        return flag

browser = webdriver.Chrome()
start_url_1 = 'https://www.familydoctor.com.cn/ask/did/87/?page='
# 显式等待
WebDriverWait(browser, 3)

XpahtList = [   "/html/body/div[5]/div/div[1]/div[2]/div[2]/dl[1]/dt/p/a",
                "/html/body/div[5]/div/div[1]/div[2]/div[2]/dl[2]/dt/p/a",
                "/html/body/div[5]/div/div[1]/div[2]/div[2]/dl[3]/dt/p/a",
                "/html/body/div[5]/div/div[1]/div[2]/div[2]/dl[4]/dt/p/a",
                "/html/body/div[5]/div/div[1]/div[2]/div[2]/dl[5]/dt/p/a",
                "/html/body/div[5]/div/div[1]/div[2]/div[2]/dl[6]/dt/p/a",
                "/html/body/div[5]/div/div[1]/div[2]/div[2]/dl[7]/dt/p/a",
                "/html/body/div[5]/div/div[1]/div[2]/div[2]/dl[8]/dt/p/a",
                "/html/body/div[5]/div/div[1]/div[2]/div[2]/dl[9]/dt/p/a",
                "/html/body/div[5]/div/div[1]/div[2]/div[2]/dl[10]/dt/p/a",
                "/html/body/div[5]/div/div[1]/div[2]/div[2]/dl[11]/dt/p/a",
                "/html/body/div[5]/div/div[1]/div[2]/div[2]/dl[12]/dt/p/a",
                "/html/body/div[5]/div/div[1]/div[2]/div[2]/dl[13]/dt/p/a",
                "/html/body/div[5]/div/div[1]/div[2]/div[2]/dl[14]/dt/p/a",
                "/html/body/div[5]/div/div[1]/div[2]/div[2]/dl[15]/dt/p/a",
                "/html/body/div[5]/div/div[1]/div[2]/div[2]/dl[16]/dt/p/a",
                "/html/body/div[5]/div/div[1]/div[2]/div[2]/dl[17]/dt/p/a",
                "/html/body/div[5]/div/div[1]/div[2]/div[2]/dl[18]/dt/p/a",
                "/html/body/div[5]/div/div[1]/div[2]/div[2]/dl[19]/dt/p/a",
                "/html/body/div[5]/div/div[1]/div[2]/div[2]/dl[20]/dt/p/a",
                "/html/body/div[5]/div/div[1]/div[2]/div[2]/dl[21]/dt/p/a",
                "/html/body/div[5]/div/div[1]/div[2]/div[2]/dl[22]/dt/p/a",
                "/html/body/div[5]/div/div[1]/div[2]/div[2]/dl[23]/dt/p/a",
                "/html/body/div[5]/div/div[1]/div[2]/div[2]/dl[24]/dt/p/a",
                "/html/body/div[5]/div/div[1]/div[2]/div[2]/dl[25]/dt/p/a",
                "/html/body/div[5]/div/div[1]/div[2]/div[2]/dl[26]/dt/p/a",
                "/html/body/div[5]/div/div[1]/div[2]/div[2]/dl[27]/dt/p/a",
                "/html/body/div[5]/div/div[1]/div[2]/div[2]/dl[28]/dt/p/a",
                "/html/body/div[5]/div/div[1]/div[2]/div[2]/dl[29]/dt/p/a",
                "/html/body/div[5]/div/div[1]/div[2]/div[2]/dl[30]/dt/p/a",
                "/html/body/div[5]/div/div[1]/div[2]/div[2]/dl[31]/dt/p/a",
                "/html/body/div[5]/div/div[1]/div[2]/div[2]/dl[32]/dt/p/a",
                "/html/body/div[5]/div/div[1]/div[2]/div[2]/dl[33]/dt/p/a",
                "/html/body/div[5]/div/div[1]/div[2]/div[2]/dl[34]/dt/p/a",
                "/html/body/div[5]/div/div[1]/div[2]/div[2]/dl[35]/dt/p/a",
                "/html/body/div[5]/div/div[1]/div[2]/div[2]/dl[36]/dt/p/a",
                "/html/body/div[5]/div/div[1]/div[2]/div[2]/dl[37]/dt/p/a",
                "/html/body/div[5]/div/div[1]/div[2]/div[2]/dl[38]/dt/p/a",
                "/html/body/div[5]/div/div[1]/div[2]/div[2]/dl[39]/dt/p/a",
                "/html/body/div[5]/div/div[1]/div[2]/div[2]/dl[40]/dt/p/a",
                "/html/body/div[5]/div/div[1]/div[2]/div[2]/dl[41]/dt/p/a",
                "/html/body/div[5]/div/div[1]/div[2]/div[2]/dl[42]/dt/p/a",
                "/html/body/div[5]/div/div[1]/div[2]/div[2]/dl[43]/dt/p/a",
                "/html/body/div[5]/div/div[1]/div[2]/div[2]/dl[44]/dt/p/a",
                "/html/body/div[5]/div/div[1]/div[2]/div[2]/dl[45]/dt/p/a",
                "/html/body/div[5]/div/div[1]/div[2]/div[2]/dl[46]/dt/p/a",
                "/html/body/div[5]/div/div[1]/div[2]/div[2]/dl[47]/dt/p/a",
                "/html/body/div[5]/div/div[1]/div[2]/div[2]/dl[48]/dt/p/a",
                "/html/body/div[5]/div/div[1]/div[2]/div[2]/dl[49]/dt/p/a"
             ]



page = 21
qalist = []
while page <= 50:
    page_url = start_url_1+ str(page)+"&"
    browser.get(page_url)
    #print(page_url)
    time.sleep(5)
    sites = []
    for Xpath in XpahtList:
        try:
         x = browser.find_element_by_xpath(Xpath)
        except Exception:
            print("exception x1")
            continue
        sites.append(x.get_attribute("href"))

    count = 1
    for site in sites:
        browser.get(site)
        time.sleep(2)
        try:
            x = browser.find_element_by_xpath("/html/body/div[5]/div/div[1]/div[1]/div/h3")
        except Exception:
            print('exception x')
            continue
        try:
            y = browser.find_element_by_xpath("/html/body/div[5]/div/div[1]/div[2]/ul/li/div[2]/dl/dd/p")
        except Exception:
            print('exception y')
            continue

        print(count)
        qa = {
            "q": "",
            "a": ""
        }
        qa['q'] = x.text
        qa['a'] = y.text
        qalist.append(qa)
        count += 1
    page = page + 1

with open('QA2.json','w',encoding='utf8') as f:
      # for q in qalist:
      #   print(q)
      #   f.write(str(q))
      json.dump(qalist,f,indent=4,ensure_ascii=False)


f.close()














