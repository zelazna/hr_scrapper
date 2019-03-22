import base64
import io
import os

import scrapy
from PIL import Image
from pytesseract import pytesseract
from scrapy_splash import SplashRequest

from ..items import JobItem, JobItemLoader

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
        loader = JobItemLoader(item=JobItem(), response=response)
        loader.add_css("date", ".date-lieu-annonce :first-child::text")
        loader.add_css("date", ".date-lieu-annonce div:first-child::text")
        loader.add_css("text", ".contenu-texte-annonce::text")
        loader.add_css("text", ".contenu-texte-annonce b ::text")
        loader.add_css("text", ".contenu-texte-annonce-pave ::text")
        loader.add_css("ref", ".reference-annonce::text")
        loader.add_value("url", response.meta['ad_url'])
        loader.add_value("email", self.get_ad_email(response.data.get('screenshot')))
        return loader.load_item()

    @staticmethod
    def get_ad_email(base64_image):
        if not base64_image:
            return None
        data = base64.b64decode(base64_image)
        image = Image.open(io.BytesIO(data))
        return pytesseract.image_to_string(image).replace(" ", "")
