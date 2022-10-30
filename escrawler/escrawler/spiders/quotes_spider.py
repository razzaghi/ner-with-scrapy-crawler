import scrapy
from bs4 import BeautifulSoup


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = []
        for i in range(0, 200):
            page = "o" + str(i * 10)
            urls.append(
                'https://www.tripadvisor.es/ShowTopic-g1-i12452-k3158072-' + page + '-Historias_de_ultramar-El_sofa_de_la_comunidad.html')

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def generate_email(self, text):
        return (str(text)+"@ysp.com").replace("\n", "")

    def enter_removal(self, text):
        return str(text).replace("\n", "")

    def text_normalizer(self, text):
        return str(text).replace("\n", "")

    def parse(self, response):
        for quote in response.css('div.post'):
            username_html = quote.css('div.username').extract()
            title_html = quote.css('div.postTitle').extract()[0]
            body_html = quote.css('div.postBody').extract()[0]
            title_soup = BeautifulSoup(title_html)
            body_soup = BeautifulSoup(body_html)
            username = None
            if username_html:
                username_soup = BeautifulSoup(username_html[0])
                username = self.enter_removal(username_soup.get_text())
            body = body_soup.get_text()
            title = self.enter_removal(title_soup.get_text())
            post_date = self.enter_removal(quote.css('div.postDate::text').get())
            text = self.generate_email(username) + "\n" + title + "\n" + post_date + "\n" + body
            yield {
                'text': text,
                'label': [],
            }
        # page = response.url.split("/")[-2]
        # filename = f'quotes-{page}.html'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log(f'Saved file {filename}')
