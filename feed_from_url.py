from ntpath import join
import scrapy
from datetime import datetime,timedelta
from urllib.parse import urlparse
import os
import csv
import mysql.connector


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    #FilePath="D:\\work\\python\\webscrape\\"
    mydb = mysql.connector.connect(
            host="64.227.176.243",
  user="phpmyadmin",
  password="Possibilities123.@",
  database="final_database")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM bulk_feed_content where featured_image is null ")
    myresult = mycursor.fetchall()
    #read url csv file
    #urlCsvFile = open(join(FilePath,"sitemapurl.csv"))
    #csvreader = csv.reader(urlCsvFile)
    rows = []
    #for row in csvreader:
    #    rows.append(row)
        #print(row)
    #urlCsvFile.close()
    def start_requests(self):
        #urls = [
        #    'https://www.hitc.com/feed/',
        #    'https://dmerharyana.org/feed/'
        #]
        #urls=self.rows
        for url in self.myresult:
            # print(url)
            yield scrapy.Request(url=url[2], meta={'bfw_id':url[1],'bfc_id':url[0]}, callback=self.parse)

    def parse(self, response):
        domain = urlparse(response.url).netloc
        #print(response.xpath('//h1[@class="tdb-title-text"]').get())
        #print(response.xpath('//div[contains(concat(" ", normalize-space(@class), " "), " td-post-content ")]').get(default='not-found'))
        self.mycursor.execute("SELECT * FROM bulk_feed_website where des_id=%s" % response.meta['bfw_id'])
        myresult = self.mycursor.fetchone()
        if not myresult:
          exit
        webTitle= response.xpath(myresult[2]).get()
        # print(webTitle)
        categoryy=response.xpath(myresult[5]).get()
        content=response.xpath(myresult[3]).get()
        image_link= response.xpath(myresult[4]).get()
        #data = [webTitle, content]

        mycursor = self.mydb.cursor()
        sql = "update bulk_feed_content set title=%s,content=%s,featured_image=%s,Category=%s where bfc_id=%s"
#        sql = "update bulk_quill_bank set title=%s,content=%s,featured_image=%s where wcid=%s"

#        sql = "update bulk_quill_bank set featured_image=%s where wcid=%s"
#        val = (webTitle,content,image_link,response.meta['wcid'])

        val = (webTitle,content,image_link,categoryy,response.meta['bfc_id'])
        #val = (image_link,response.meta['wcid'])
        mycursor.execute(sql, val)
        self.mydb.commit()
        #with open('WebsiteContent.csv', 'w', encoding='UTF8', newline='') as f:
            #writer = csv.writer(f)
            # write the data
            #writer.writerow(data)
    #def closed(self, reason):
    #    ft = open(self.FilePathName, "w", encoding='utf-8')
    #    ft.write(self.LatestDate.strftime("%Y-%m-%d %H:%M:%S"))
    #    ft.close()
