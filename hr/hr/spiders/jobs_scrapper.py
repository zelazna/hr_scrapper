import base64
import io

import scrapy
from PIL import Image
from pytesseract import pytesseract
from scrapy_splash import SplashRequest

from ..items import HrItem
import os

dir_path = os.path.dirname(os.path.abspath(__file__))
script_path = os.path.join(dir_path, "../scripts/main.lua")


class JobsSpider(scrapy.Spider):
    name = "jobs"
    start_urls = ['https://www.lhotellerie-restauration.fr/emploi/chef-de-rang-75-paris']

    def parse(self, response):
        for job in response.css(".ad_emploi"):
            ad_path = job.xpath('@onclick').get().split("'")[1]
            ad_page = response.urljoin(ad_path)

            request = SplashRequest(
                ad_page,
                self.parse_job,
                endpoint='execute',
                args={
                    'lua_source': open(script_path, 'r').read(),
                    'pad': 2,
                    'css': 'div.contenu-texte-annonce span',
                }
            )
            request.meta['ad_url'] = ad_page
            yield request

        # follow pagination links
        for href in response.css('ul.cd-pagination li:not(:first-child) a::attr(href)'):
            yield response.follow(href, self.parse)

    def parse_job(self, response):
        yield HrItem(
            date=response.css('.date-lieu-annonce :first-child::text').get(),
            text=self.get_ad_text(response),
            ref=response.css('.reference-annonce::text').get(),
            url=response.meta['ad_url'],
            # email=self.get_ad_email(response.data.get('screenshot'))
        )

    @staticmethod
    def get_ad_text(response):
        text = response.css('.contenu-texte-annonce::text').get()
        return ''.join(response.css('.contenu-texte-annonce b ::text').getall()) if text == "\t" else text

    @staticmethod
    def get_ad_email(base64_image):
        if not base64_image:
            return None
        data = base64.b64decode(base64_image)
        image = Image.open(io.BytesIO(data))
        return pytesseract.image_to_string(image).strip()
