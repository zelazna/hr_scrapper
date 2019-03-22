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