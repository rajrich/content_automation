from genericpath import isdir
from socket import timeout
from selenium import webdriver
import time
import requests
import json
import base64
import time
import shutil
from datetime import date
#driver = webdriver.PhantomJS('/opt/homebrew/bin/phantomjs')
#driver = webdriver.Remote(
 # desired_capabilities=webdriver.DesiredCapabilities.HTMLUNIT)
#driver = webdriver.Chrome()
#from webdriver_manager.chrome import ChromeDriverManager
#Timer starts
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

#from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import os
from fake_headers import Headers
# %%
from os import listdir
# %%
from os.path import isfile, join
#import sys
from sys import exit
import mysql.connector
mydb = mysql.connector.connect(
  host="3.140.57.116",
  user="wp_raj1",
  password="rajPassword95$",
  database="url_automation"
)

#sitepath="/Users/rishi/Dropbox/sites/"
#mypath="/Users/rishi/Google Drive/My Drive/sites/editorials24.com/"
#processed_path=mypath+"processed/"
#dirs = [f.name for f in os.scandir(sitepath) if f.is_dir()]
dirs = ["www.therconline.com"]
#onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
#if not onlyfiles:
#   exit("no files to process")

header = Headers(
    browser="chrome",  # Generate only Chrome UA
    os="win",  # Generate only Windows platform
    headers=False # generate misc headers
)
#customUserAgent = header.generate()['User-Agent']


#start = timeit.default_timer()
# instantiate a chrome options object so you can set the size and headless preference
chrome_options = Options()
#chrome_options.add_argument("--headless")
#chrome_options.add_argument("--window-size=1920x1080")
#chrome_options.add_argument("--user-data-dir=chrome-data")
chrome_options.add_argument("--user-agent={customUserAgent}")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--proxy-server='direct://'")
chrome_options.add_argument("--proxy-bypass-list=*")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--ignore-certificate-errors')
#driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)
#driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=r'D:\\work\\python\\webscrape\\chromedriver.exe')
#driver.set_window_size(1920, 1080)

# wp_user = "gh1YcBHVrq"
# wp_pwd = "zd2eW0Aj6F"

mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM multiple_destination_websites where status = 1 ")
myresult = mycursor.fetchall()
for dir in myresult:
    dest__id = dir[0]

    domain=dir[1]
    auth_url = domain+"wp-json/jwt-auth/v1/token"



    wp_user = dir[2]
    wp_pwd = dir[3]


    auth_data = {
            "username":wp_user,
            "password":wp_pwd
        }
    auth_responce = requests.post(auth_url , json=auth_data)
    try:
        token = auth_responce.json().get('data').get('token')
    except AttributeError:
        token = auth_responce.json().get('token')
    # print(auth_responce.json().get('data').get('token'))
    print(domain)
    print(token)

    # bfw_li=[]
    # for des in listt:
    #   mycursor.execute("SELECT * FROM bulk_feed_website where des_id=(%s)" %  (des))
    #   websites = mycursor.fetchall()
    #   bfw_li.extend(websites)

    alll=[]
    post_count=[]
    mycursor.execute("SELECT * FROM bulk_quill_bank where bqt_id=(%s) and status = 1 and publish_status is NULL " % (dir[0]) )
    webs = mycursor.fetchall()
    alll.extend(webs[0:2])
    post_count.append(len(alll))
    for x in alll:

    # print(dir)
    # for x in alll:
        url = domain+"wp-json/wp/v2/posts"
        category_url = domain+"wp-json/wp/v2/categories/"
        imageURL=x[4]
        category = x[5]
        # print(imageURL)
        #user = "rishi"
        #password = "271191.rishi"
        #credentials = user + ':' + password
        #token = base64.b64encode(credentials.encode())
        #token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOlwvXC9sb2NhbGhvc3Q6ODEiLCJpYXQiOjE2NDkzMjU5MjEsIm5iZiI6MTY0OTMyNTkyMSwiZXhwIjoxNjQ5OTMwNzIxLCJkYXRhIjp7InVzZXIiOnsiaWQiOjEsImRldmljZSI6IiIsInBhc3MiOiI3YWQ3MjcwODkzNDgyNmVhMmVhZTI1YjQ2NjA2N2I3NyJ9fX0.i_TkLtUBl-RAdDwuik3czhFL1mXaa1Da9wiWrH1AeQM"
        header = {'Authorization': 'Bearer ' + token}
        current=time.strftime("%Y-%m-%dT%H:%M:%S",time.localtime())

        title = x[2]
        print(title)

        post = {
        'title'    : title,
        'status'   : 'draft',
        'content'  : x[6],
        'categories': 1
        }

        #'date'   : '2022-04-07T10:00:00'
        responce = requests.post(url , headers=header, json=post)
        img_data = requests.get(imageURL).content


        uploadImageFilename = "661b943654f54bd4b2711264eb275e1b.jpg"
        curHeaders = {
        'Authorization': 'Bearer ' + token,
        "Content-Type": "image/jpeg",
        "Accept": "application/json",
        'Content-Disposition': "attachment; filename=%s" % uploadImageFilename ,
        }

        resp = requests.post(domain+"wp-json/wp/v2/media",
        headers=curHeaders,
        data=img_data,
        )
        newDict=resp.json()
        postid = str(json.loads(responce.content)['id'])
        upd={
            'name':category,'slug':category
        }

        update_cat = requests.post(category_url , headers=header, json=upd)
        try:
            postiid = str(json.loads(update_cat.content)['id'])
        except KeyError:
            postiid = str(json.loads(update_cat.content)['data']['term_id'])
        # print(postiid)
        updatedpost = {'title'    : title,
            'status'   : 'publish',
            'content'  : x[6],'categories':postiid,


            "featured_media":int(postid)+1}
        update = requests.post(url + '/' + postid, headers=header, json=updatedpost)
        # print("postid = " ,postid)
        # link1=update.json().get('id')
        # print("link1id = ",link1)
        sql = "update bulk_quill_bank set publish_status=1  where wcid=%s" % (x[0])
        # val = (1)
        mycursor.execute(sql)
        mydb.commit()

    total = 0
    for ele in range(0, len(post_count)):
        total = total + post_count[ele]
    print(total, "record inserted.")
    mycursor = mydb.cursor()
    # print(mycursor)
    mycursor.callproc('sp_website_post',args=(domain,total,dest__id))
    mydb.commit()
