import scrapy

class AnnonceSpider(scrapy.Spider):
    name = 'annonces'
    start_urls = [
        'http://www.seloger.com/list.htm?org=advanced_search&idtt=2&idtypebien=2,1&cp=75&tri=initial&LISTING-LISTpg=1&naturebien=1,2,4',
    ]

    def parse(self, response):
        for annonce in response.css('div.c-wrap-main:nth-child(2)'):
            yield {
                'price': annonce.css('div.ListContent__SmartClassifiedExtended-sc-1viyr2k-2:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1)').get(),
                'room': annonce.css('div.ListContent__SmartClassifiedExtended-sc-1viyr2k-2:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > ul:nth-child(2) > li:nth-child(1)').get(),
                'bedroom': annonce.css('div.ListContent__SmartClassifiedExtended-sc-1viyr2k-2:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > ul:nth-child(2) > li:nth-child(2)').get(),
                'surface': annonce.css('div.ListContent__SmartClassifiedExtended-sc-1viyr2k-2:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > ul:nth-child(2) > li:nth-child(3)').get()
            }

        # next_page = response.css('li.next a::attr("href")').get()
        # if next_page is not None:
        #     yield response.follow(next_page, self.parse)