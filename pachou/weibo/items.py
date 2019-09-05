import scrapy

class WeiboItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # id = scrapy.Field()
    # text = scrapy.Field()
    # attitudes_count = scrapy.Field()
    # comments_count = scrapy.Field()
    # reposts_count = scrapy.Field()
    # image_urls = scrapy.Field()  # 保存图片地址
    # images = scrapy.Field()  # 保存图片的信息
    image_urls = scrapy.Field()  # 用来存储图片的链接
    imgname = scrapy.Field()  # 用来存储图片的名字