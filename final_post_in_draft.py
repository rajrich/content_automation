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

# Returns the current local date

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
  host="64.227.176.243",
  user="phpmyadmin",
  password="Possibilities123.@",
  database="automation"
)


header = Headers(
    browser="chrome",  # Generate only Chrome UA
    os="win",  # Generate only Windows platform
    headers=False # generate misc headers
)

chrome_options = Options()
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
mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM destination_website where status = 1 ")
myresul = mycursor.fetchall()
mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM Total_posts ")
myresult = mycursor.fetchall()
previous_date = myresult[-1][4]
prev_id=set()
for ir in myresult:
    prev_id.add(ir[1])

# print(prev_id)
# print(myresult)
# print(previous_date)
prev_post=[]
for uu in myresult:
    # print(uu)
    if previous_date==uu[4]:
        prev_post.append(uu[3])


print(prev_post)
total_posts = []
dest_table_id=[]
cou=0
for dir in myresul:
    dest_id = dir[0]
    domain=dir[1]
    destination_idd=dir[0]
    dest_table_id.append(destination_idd)
    print(domain)
    # print(destination_idd)
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
    print(token)
    # mycursor = mydb.cursor()
    # mycursor.execute("SELECT * FROM bulk_quill where publish_status is null limit 10")
    # myresult = mycursor.fetchall()
    mycursor = mydb.cursor()
    # mycursor.execute("SELECT * FROM destination_website where status = 1 ")
    # myr = mycursor.fetchall()
    mycursor.execute("SELECT * FROM bulk_feed_website where des_id=(%s)" %  (dir[0]))
    # mycursor.execute("SELECT * FROM destination_website where username=(%s)" %  (myresult[2]))

    websites = mycursor.fetchall()
    alll=[]
    post_count=[]
    for i in websites:

        mycursor.execute("SELECT * FROM bulk_feed_content where bfw_id=(%s) and status = 1 and status_publish is null  " % (i[0]) )
        webs = mycursor.fetchall()
        alll.extend(webs)
        post_count.append(mycursor.rowcount)
        # mycursor.execute("SELECT * FROM bulk_feed_content where status_publish is null limit 10 ")
        # my_publish = mycursor.fetchall()

    # print(mycursor.rowcount, "record inserted.")
    for x in alll:
        url = domain+"wp-json/wp/v2/posts"
        category_url = domain+"wp-json/wp/v2/categories/"
        category = x[6]
#        print(category)
        #user = "rishi"
        #password = "271191.rishi"
        #credentials = user + ':' + password
        #token = base64.b64encode(credentials.encode())
        #token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOlwvXC9sb2NhbGhvc3Q6ODEiLCJpYXQiOjE2NDkzMjU5MjEsIm5iZiI6MTY0OTMyNTkyMSwiZXhwIjoxNjQ5OTMwNzIxLCJkYXRhIjp7InVzZXIiOnsiaWQiOjEsImRldmljZSI6IiIsInBhc3MiOiI3YWQ3MjcwODkzNDgyNmVhMmVhZTI1YjQ2NjA2N2I3NyJ9fX0.i_TkLtUBl-RAdDwuik3czhFL1mXaa1Da9wiWrH1AeQM"
        header = {'Authorization': 'Bearer ' + token}
        current=time.strftime("%Y-%m-%dT%H:%M:%S",time.localtime())

        title = x[3]
        print(title)
        post = {
        'title'    : title,
        'status'   : 'draft',
        'content'  : x[5]
        }
        responce = requests.post(url , headers=header, json=post)
        # print(responce)
        #postid = str(json.loads(responce.content))
        # print(postid)
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
            'status'   : 'draft',
            'content'  : x[5],'categories':postiid}
        update = requests.post(url + '/' + postid, headers=header, json=updatedpost)
        sql = "update bulk_feed_content set status_publish=%s where bfw_id=%s and status = 1"
        val = (1, x[1])
        mycursor.execute(sql, val)
        mydb.commit()

        #'date'   : '2022-04-07T10:00:00'

    total = 0
    for ele in range(0, len(post_count)):
        total = total + post_count[ele]
    print(total, "record inserted.")
    mycursor = mydb.cursor()
    # print(mycursor)
    mycursor.callproc('sp_website_post',args=(domain,total,dest_id))
    mydb.commit()
