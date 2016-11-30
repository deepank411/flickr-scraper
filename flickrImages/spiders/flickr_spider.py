import scrapy, re
from scrapy_splash import SplashRequest
from hashlib import sha1

from flickrImages.items import FlickrimagesItem

class FlickrSpider(scrapy.Spider):
    name = 'flickrspider'

    start_urls = ['https://www.flickr.com/explore/2016/10/01']

    def start_requests(self):
        for url in self.start_urls:
            print url
            yield SplashRequest(url, self.parse, args={'wait': 0.5})

    def parse(self, response):
        # print response.css("div.title-row").extract()
        next_url = response.css("div.explore-pagination a::attr(href)").extract()
        print next_url
        print 'next url: '+ next_url[-1]

        for i in response.css("div.photo-list-photo-view"):
            href = i.css("div.photo-list-photo-interaction a.overlay::attr(href)")
            print  href.extract()
            if len(href.extract()) != 0:
                full_url = response.urljoin(href.extract()[0])
                yield SplashRequest(full_url, self.parse_image, args={'wait': 2.5})
            #break

        yield SplashRequest(response.urljoin(next_url[-1]), self.parse, args={'wait': 1.5})

    def parse_image(self, response):
        item = FlickrimagesItem()
        # print response.css("body").extract()
        title = response.css("h1.photo-title::text").extract()
        print title
        if title:
            item['title'] = title[0]
        img = response.css("div.photo-well-media-scrappy-view img.main-photo::attr(src)").extract()
        img = ['http:' + img[0]]
        print img
        item['image_urls'] = img
        item['image_name'] = sha1(img[0]).hexdigest() + '.jpg'
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
        # item['tags'] = l2
        # return item
