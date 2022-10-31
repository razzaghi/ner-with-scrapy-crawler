import scrapy
from bs4 import BeautifulSoup

from escrawler.escrawler.utils.normalizer import cleanmailtext


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    tripadvisor_urls = [
        {"url": "https://www.tripadvisor.es/ShowTopic-g1-i11064-k3907738page_number-Edreams-General_Discussion.html",
         "pages": 158},
        {
            "url": 'https://www.tripadvisor.es/ShowTopic-g1-i12452-k3158072page_number-Historias_de_ultramar-El_sofa_de_la_comunidad.html',
            "pages": 158},
        {
            "url": 'https://www.tripadvisor.es/ShowTopic-g1-i12652-k10756607page_number-Telefono_contacto_tripadvisor-Soporte_tecnico.html',
            "pages": 49},
        {
            "url": 'https://www.tripadvisor.es/ShowTopic-g1-i12452-k3158072-o13100page_number-Historias_de_ultramar-El_sofa_de_la_comunidad.html',
            "pages": 1311},
        {
            "url": 'https://www.tripadvisor.es/ShowTopic-g1-i11062-k11263396page_number-Destinia_com_opiniones-Package_Holidays.html',
            "pages": 35},
        {
            "url": 'https://www.tripadvisor.es/ShowTopic-g1-i12452-k2546279page_number-ILos_viajeros_se_presentan-El_sofa_de_la_comunidad.html',
            "pages": 838},

    ]

    def start_requests(self):
        urls = []
        for page in self.tripadvisor_urls:
            url = page["url"]
            page_count = page["pages"]
            for i in range(0, page_count - 1):
                page_number = "-o" + str(i * 10)
                main_url = url.replace("page_number", page_number)
                urls.append(main_url)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def generate_email(self, text):
        return (str(text) + "@ysp.com").replace("\n", "")

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
                username = cleanmailtext(username_soup.get_text())
            body = cleanmailtext(body_soup.get_text())
            title = cleanmailtext(title_soup.get_text())
            post_date = cleanmailtext(quote.css('div.postDate::text').get())
            text = self.generate_email(username) + "\n" + title + "\n" + post_date + "\n" + body
            if len(body) > 200:
                yield {
                    'text': text,
                    'label': [],
                }
        # page = response.url.split("/")[-2]
        # filename = f'quotes-{page}.html'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log(f'Saved file {filename}')
