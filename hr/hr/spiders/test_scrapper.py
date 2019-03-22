import base64
import io

import scrapy
from PIL import Image
from pytesseract import pytesseract
from scrapy_splash import SplashRequest

script = """
-- Arguments:
-- * url - URL to render;
-- * css - CSS selector to render;
-- * pad - screenshot padding size.

-- this function adds padding around region
function pad(r, pad)
  return {r[1]-pad, r[2]-pad, r[3]+pad, r[4]+pad}
end

-- main script
function main(splash)

  -- this function returns element bounding box
  local get_bbox = splash:jsfunc([[
    function(leftEl, rightEl) {
      var leftBounds = document.querySelector(leftEl).getBoundingClientRect();
      var rightBounds = document.querySelector(rightEl).getBoundingClientRect();
      return [leftBounds.left, leftBounds.top, rightBounds.right, leftBounds.bottom];
    }
  ]])

  assert(splash:go(splash.args.url))
  assert(splash:wait(0.5))

  -- don't crop image by a viewport
  splash:set_viewport_full()

  local region = pad(get_bbox(splash.args.leftEl, splash.args.rightEl), splash.args.pad)
  return { html = splash:html(), screenshot = splash:png{region=region} }
end
"""


class TestSpider(scrapy.Spider):
    name = "test"
    user_agent = 'Mozilla/5.0'

    def start_requests(self):
        url = 'https://www.lhotellerie-restauration.fr/emploi/annonce.asp?n=_3N_3NQ'
        yield SplashRequest(
            url,
            self.save_element_screenshot,
            endpoint='execute',
            args={
                'lua_source': script,
                'pad': 2,
                'leftEl': 'div.contenu-texte-annonce span:first-child',
                'rightEl': 'div.contenu-texte-annonce span:last-child'
            }
        )

    def save_element_screenshot(self, response):
        imgdata = base64.b64decode(response.data['screenshot'])
        image = Image.open(io.BytesIO(imgdata))
        yield {
            "email": pytesseract.image_to_string(image).strip()
        }
