# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CoursescraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class CourseItem(scrapy.Item):
    title = scrapy.Field()
    company = scrapy.Field()
    instructor = scrapy.Field()
    num_enrolled = scrapy.Field()
    ratings = scrapy.Field()
    num_reviews = scrapy.Field()
    learners_liked = scrapy.Field()
    what_to_learn = scrapy.Field()
    skills_covered = scrapy.Field()
    about = scrapy.Field()
    assignment_details = scrapy.Field()
    url = scrapy.Field()
    learner_review_date = scrapy.Field()
    learner_review_rating = scrapy.Field()
    learner_reviews = scrapy.Field()
    level_required = scrapy.Field()
    language_taught = scrapy.Field()
    certificate = scrapy.Field()
    modules = scrapy.Field()
    modules_desc = scrapy.Field()
    time_to_complete = scrapy.Field()