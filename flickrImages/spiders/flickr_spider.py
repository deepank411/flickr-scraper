import scrapy, re
from scrapy_splash import SplashRequest
from hashlib import sha1

from flickrImages.items import FlickrimagesItem

class FlickrSpider(scrapy.Spider):
	name = 'flickrspider'

	start_urls = ['https://www.flickr.com/photos/tags/food', 'https://www.flickr.com/photos/tags/sport']

	def parse(self, response):

		next_url = response.css("div.pagination-view a::attr(href)").extract()[-1]

		for i in response.css("div.photo-list-photo-interaction a.overlay::attr(href)").extract():
			full_url = response.urljoin(i)
			print 'full_url: ' + full_url
			yield SplashRequest(full_url, callback = self.parse_image, args={'wait': 5})

		yield scrapy.Request(response.urljoin(next_url), callback = self.parse)

	def parse_image(self, response):
		item = FlickrimagesItem()
		outerlist = response.css("ul.tags-list")
		l = outerlist.css("li.autotag a::text").extract()
		l = [i.strip() for i in l]
		l2 = filter(None, l)
		print l2
		if l2 == []:
			pass
		else:
			title = response.css("h1.photo-title::text").extract()
			print title
			if title:
				item['title'] = title[0]
			img = response.css("div.photo-well-media-scrappy-view img.main-photo::attr(src)").extract()
			img = ['http:' + img[0]]
			print img
			item['image_urls'] = img
			item['image_name'] = sha1(img[0]).hexdigest() + '.jpg'
			item['tags'] = l2
			return item
