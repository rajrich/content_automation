from ntpath import join
import scrapy
from datetime import datetime,timedelta
from urllib.parse import urlparse
import os
import csv
import mysql.connector
import sys



class QuotesSpider(scrapy.Spider):
    mydb = mysql.connector.connect(
            host="64.227.176.243",
            user="phpmyadmin",
            password="Possibilities123.@",
            database="final_database")
    name = "quotes"
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM last_feed_date where category='feed' limit 1")
    myresult = mycursor.fetchone()
    if not myresult:
        sql = "insert into last_feed_date(last_update,category) values(now(),'feed')"
        mycursor.execute(sql)
        mycursor.execute("SELECT now();")
        currentdate = mycursor.fetchone()
        SavedDate = currentdate[0]
    else:
        SavedDate=myresult[1]

    LatestDate = datetime.now()#- timedelta(hours=5,minutes=30)#datetime.strptime(response.xpath('//pubDate/text()').get().replace(" +0000",""), '%a, %d %b %Y %H:%M:%S')
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM destination_website where status = 1 ")
    myresult = mycursor.fetchall()
    print(myresult)
    al_web=[]
    for ress in myresult:
#        print(ress[0])
        mycursor.execute("SELECT * FROM bulk_feed_website where des_id=(%s)" %  (ress[0]))

        websites = mycursor.fetchall()
        al_web.extend(websites)
#    print(al_web)
    def start_requests(self):
        #urls = [
        #    'https://www.hitc.com/feed/',
        #    'https://dmerharyana.org/feed/'
        #]
        #urls=self.rows
        print("request")
        for url in self.al_web:
            # print(url)

            yield scrapy.Request(url=url[1], meta={'bfw_id':url[0],'Destination_id':url[4]}, callback=self.parse)

    def parse(self, response):
        print("parsing started")
        domain = urlparse(response.url).netloc
        response.selector.register_namespace('content','http://purl.org/rss/1.0/modules/content/')


        print(f'Saved Data:{self.SavedDate}')

        print(f'LatestDate Data:{self.LatestDate}')

        #File_object.close()
        for quote in response.xpath('//item'):
            pubDate=quote.xpath('.//pubDate/text()').get().replace(" +0000","") #Thu, 12 May 2022 17:43:01 +0000
            date_time_obj = datetime.strptime(pubDate, '%a, %d %b %Y %H:%M:%S')

            if self.SavedDate<date_time_obj:
                print(f'Pub Date: {date_time_obj}')
                # title = quote.xpath('.//title/text()').get()
                # content=quote.xpath('.//content:encoded/text()').get()
                # category = quote.xpath('.//category/text()').get()
                url=quote.xpath('.//link/text()').get()
                sql = "insert into bulk_feed_content(bfw_id,url,Destination_id) values(%s,%s,%s)"
                val = (response.meta['bfw_id'],url,response.meta['Destination_id'])
                self.mycursor.execute(sql, val)
                self.mydb.commit()
                #self.log(f'Saved file {filename}')
    def closed(self, reason):
        sql = "update last_feed_date set last_update=now() where ldf_id=2"
        #print(str(self.myresult[0]))
        self.mycursor.execute(sql)
        self.mydb.commit()
