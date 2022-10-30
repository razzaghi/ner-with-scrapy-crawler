import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = []
        for i in range(0, 2):
            page = "o" + str(i * 10)
            urls.append(
                'https://www.tripadvisor.es/ShowTopic-g1-i12452-k3158072-' + page + '-Historias_de_ultramar-El_sofa_de_la_comunidad.html')

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for quote in response.css('div.postcontent'):
            yield {
                'postTitle': quote.css('div.postTitle::text').get(),
                'postDate': quote.css('div.postDate::text').get(),
                'postBody': quote.css('div.postBody::text').get(),
            }
        # page = response.url.split("/")[-2]
        # filename = f'quotes-{page}.html'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log(f'Saved file {filename}')
