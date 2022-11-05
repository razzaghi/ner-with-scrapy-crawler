import csv
import re
from pathlib import Path

import scrapy
from bs4 import BeautifulSoup

from escrawler.normalizer import cleanmailtext


class SkaddenSpider(scrapy.Spider):
    name = "skadden"

    start_url = "https://www.skadden.com/"

    urls = []
    crawled_urls = []

    file_header = ['page_title', 'category_type', 'category_name', 'category_level', "category_short_description",
                   'address', 'body', "related_categories"]
    tripadvisor_file = open('.csv', 'w', encoding="UTF-8")
    csv_writer = csv.writer(tripadvisor_file)

    def start_requests(self):
        base_dir = Path(__file__).resolve().parent.parent.parent.parent

        xml_file_path = str(base_dir) + f"/sitemaps/{self.name}.xml"
        print("=================")
        print(base_dir)
        print(xml_file_path)
        f = open(xml_file_path)
        file_text = f.read()
        pattern = '(?<=<loc>)[a-zA-z]+://[^\s]*(?=</loc>)'

        urls = re.findall(pattern, file_text)
        print(len(urls))
        print("=================")
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def generate_email(self, text):
        return (str(text) + "@ysp.com").replace("\n", "")

    def enter_removal(self, text):
        return str(text).replace("\n", "")

    def text_normalizer(self, text):
        return str(text).replace("\n", "")

    def parse(self, response, **kwargs):
        print("------------------------- yes ----------------------------")
        print(len(response.css('a')))
        page_soup = BeautifulSoup(response)
        page_text = cleanmailtext(page_soup.get_text())
        print(page_text)
        print("==================================================")
        # for quote in response.css('div.post'):
        #     print("------------------------- yes 2 ----------------------------")
        #     username_html = quote.css('div.username').extract()
        #     title_html = quote.css('div.postTitle').extract()[0]
        #     body_html = quote.css('div.postBody').extract()[0]
        #     title_soup = BeautifulSoup(title_html)
        #     body_soup = BeautifulSoup(body_html)
        #     username = None
        #     if username_html:
        #         username_soup = BeautifulSoup(username_html[0])
        #         username = cleanmailtext(self.enter_removal(username_soup.get_text()))
        #     body = cleanmailtext(body_soup.get_text())
        #     title = cleanmailtext(self.enter_removal(title_soup.get_text()))
        #     post_date = cleanmailtext(quote.css('div.postDate::text').get())
        #     text = self.generate_email(username) + "\n" + title + "\n" + post_date + "\n" + body
        #     print(len(body))
        #     data = [username, title, post_date, body]
        #     self.csv_writer.writerow(data)
        # page = response.url.split("/")[-2]
        # filename = f'quotes-{page}.html'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log(f'Saved file {filename}')
