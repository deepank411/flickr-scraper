import scrapy, re
from scrapy_splash import SplashRequest

from flickrImages.items import FlickrimagesItem

class FlickrSpider(scrapy.Spider):
    name = 'flickrspider'

    # date = [str(item).zfill(2) for item in range(1,26)]
    # month = [str(item).zfill(2) for item in range(1,13)]
    # year = ['2015', '2016']

    start_urls = ['https://www.flickr.com/explore']

    def start_requests(self):
        for url in self.start_urls:
            print url
            yield SplashRequest(url, self.parse, args={'wait': 0.5})

    def parse(self, response):
        # print response.css("div.title-row").extract()
        print response.css("div.explore-pagination a::attr(href)").extract_first()

        for i in response.css("div.photo-list-photo-view"):
            href = i.css("div.photo-list-photo-interaction a.overlay::attr(href)")
            print href.extract()
            full_url = response.urljoin(href.extract()[0])
            yield SplashRequest(full_url, self.parse_image, args={'wait': 1.5})
            # break

    def parse_image(self, response):
        item = FlickrimagesItem()
        # print response.css("body").extract()
        title = response.css("h1.photo-title::text").extract()
        print title

        img = response.css("div.photo-well-media-scrappy-view img.main-photo::attr(src)").extract()
        print img
        item['image_url'] = img[0]
        item['title'] = title[0]
        outerlist = response.css("ul.tags-list")
        l = outerlist.css("li a::text").extract()
        l = [i.strip() for i in l]
        l2 = filter(None, l)
        print l2
        if l2 == []:
            pass
        else:
            item['tags'] = l2
            return item
