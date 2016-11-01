# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

# class TripadvisorScraperPipeline(object):
#     def process_item(self, item, spider):
#         return item

class TripadvisorScraperPipeline(object):
	def process_item(self, item, spider):
		results.append(dict(item))

results = []
def spider_closed(spider):
	print results