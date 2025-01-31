from coursescraper.spiders.coursespider import CoursespiderSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

def run():
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(CoursespiderSpider)
    process.start()


if __name__ == "__main__":
    run()