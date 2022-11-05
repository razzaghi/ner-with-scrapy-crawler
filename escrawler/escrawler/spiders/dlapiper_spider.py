import csv

import scrapy
from bs4 import BeautifulSoup
from escrawler.normalizer import cleanmailtext


class DlapiperSpider(scrapy.Spider):
    name = "dlapiper"

    start_url = "https://www.dlapiper.com/en/us/"

    urls = []
    crawled_urls = []
    fetched_urls = []

    file_header = ['page_title', 'category_type', 'category_name', 'category_level', "category_short_description",
                   'address', 'body', "related_categories"]
    tripadvisor_file = open('.csv', 'w', encoding="UTF-8")
    csv_writer = csv.writer(tripadvisor_file)

    def start_requests(self):
        print("=================")
        # urls = []
        yield scrapy.Request(url=self.start_url, callback=self.extract_url)

    def generate_email(self, text):
        return (str(text) + "@ysp.com").replace("\n", "")

    def enter_removal(self, text):
        return str(text).replace("\n", "")

    def text_normalizer(self, text):
        return str(text).replace("\n", "")

    def extract_url(self, response):
        print("---------------------- Start To Extract ----------------------")
        page_soup = BeautifulSoup(response.body)
        for a in page_soup.find_all('a', href=True):
            url = a['href']
            if not url in self.urls:
                self.urls.append(url)

        for url in self.urls:
            if not url in self.crawled_urls:
                self.crawled_urls.append(url)
                yield scrapy.Request(url=url, callback=self.extract_url)

        if len(self.crawled_urls) == len(self.urls):
            print("=================== All URLS Fetched =================")
            print(len(self.urls))
            # for url in self.urls:
            #     yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        print("------------------------- yes ----------------------------")
        page_soup = BeautifulSoup(response)
        body = page_soup.css("body")
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
