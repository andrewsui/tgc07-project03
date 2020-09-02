import re

def generate_amazon_url(url):
    amazon_SKU_regex = re.compile(r'B\w\w\w\w\w\w\w\w\w')
    match_obj = amazon_SKU_regex.search(url)
    if match_obj:
        sku = match_obj.group()
        affiliate_ref = "ref=unique-affiliate-reference-code"
        return "https://www.amazon.com/dp/" + sku + "/" + affiliate_ref
    else:
        return "https://www.amazon.com/"