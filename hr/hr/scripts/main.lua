-- Arguments:
-- * url - URL to render;
-- * css - CSS selector to render;
-- * pad - screenshot padding size.

-- this function adds padding around region
function pad(r, pad)
    return { r[1] - pad, r[2] - pad, r[3] + pad, r[4] + pad }
end

-- main script
function main(splash)

    -- this function returns element bounding box
    local get_bbox = splash:jsfunc([[
        function(css) {
          var elements = document.querySelectorAll(css)
          if(!elements){
            return
          }
          var domElLeft = elements[0]
          var domElRight = elements[elements.length-1]
          if(!domElLeft && !domElRight){
            return
          }
          var leftBounds = domElLeft.getBoundingClientRect();
          var rightBounds = domElRight.getBoundingClientRect();
          return [leftBounds.left, leftBounds.top, rightBounds.right, leftBounds.bottom];
        }
    ]])

    local headers = {
        ["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        ["Accept-Encoding"] = "gzip, deflate, br",
        ["Accept-Language"] = "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
        ["Cache-Control"] = "max-age=0",
        ["Connection"] = "keep-alive",
        ["Cookie"] = "ASPSESSIONIDAQBQBQRC=OHGLLLECGAOJCDJDHDPKGLKL; WEBTRENDS_ID=19030404034407341402; atidvisitor=%7B%22name%22%3A%22atidvisitor%22%2C%22val%22%3A%7B%22vrn%22%3A%22-131883-%22%7D%2C%22options%22%3A%7B%22path%22%3A%22%2F%22%2C%22session%22%3A15724800%2C%22end%22%3A15724800%7D%7D; _ga=GA1.2.102164943.1551974808; alerte%5Fcookie%5Flhr=1; ASPSESSIONIDCQBRARQC=LCKPCFIDJBFAEIKPNMPLGANP; _gid=GA1.2.30797432.1552991614; ASPSESSIONIDSADABQBS=AGOLAJPAKCBBMBBJNDPOPAHC; ASPSESSIONIDSADCAQBS=DDIFDEBBALKHGMGMGAKLAAMJ; LastSearchHO=3%7C8; _gat_gtag_UA_118576901_1=1",
        ["Host"] = "www.lhotellerie-restauration.fr",
        ["Upgrade-Insecure-Requests"] = "1"
    }

    splash:set_custom_headers(headers)

    assert(splash:go(splash.args.url))
    assert(splash:wait(0.5))

    -- don't crop image by a viewport
    splash:set_viewport_full()

    local bbox = get_bbox(splash.args.css)

    if bbox == nil then
        return { html = splash:html() }
    end

    local region = pad(bbox, splash.args.pad)
    return { html = splash:html(), screenshot = splash:png { region = region } }
end