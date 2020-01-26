import scrapy

class CelescSpider(scrapy.Spider):
    name = 'celescspider'
    start_urls = ['https://www.aneel.gov.br/postos-tarifarios']

    def parse(self, response):
        for title in response.css('.inf-tec-titulo'):
            yield {'title': title.css('h2 ::text').get()}

        '''for next_page in response.css('a.next-posts-link'):
            yield response.follow(next_page, self.parse)'''
