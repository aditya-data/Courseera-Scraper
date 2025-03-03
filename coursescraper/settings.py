import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()


BOT_NAME = "coursescraper"

SPIDER_MODULES = ["coursescraper.spiders"]
NEWSPIDER_MODULE = "coursescraper.spiders"

# SCRAPEOPS_API_KEY = os.getenv("SCRAPEOPS_API_KEY")

SCRAPEOPS_FAKE_USER_AGENT_ENDPOINT = "https://headers.scrapeops.io/v1/user-agents"
SCRAPEOPS_FAKE_USER_AGENT_ENABLED = True
SCRAPEOPS_NUM_RESULTS = 50

ROBOTSTXT_OBEY = False

CONCURRENT_REQUESTS = 64
CONCURRENT_REQUESTS_PER_DOMAIN = 64
CONCURRENT_REQUESTS_PER_IP = 32
DOWNLOAD_DELAY = 0
RANDOMIZE_DOWNLOAD_DELAY = False

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 0.5
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_TARGET_CONCURRENCY = 5.0

COOKIES_ENABLED = False

DOWNLOADER_MIDDLEWARES = {
#    "coursescraper.middlewares.CoursescraperDownloaderMiddleware": 543,
   "coursescraper.middlewares.ScrapeOpsFakeUserAgentMiddleware": 400,
}

HTTPCACHE_ENABLED = False
HTTPCACHE_EXPIRATION_SECS = 3600
HTTPCACHE_DIR = "httpcache"
HTTPCACHE_IGNORE_HTTP_CODES = [403, 404]

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

ITEM_PIPELINES = {
   "coursescraper.pipelines.CoursescraperPipeline": 300,
   "coursescraper.pipelines.SaveToSQLiteAndJSONPipeline": 400,
}

LOG_LEVEL = "INFO"  # Or "WARNING" to reduce log verbosity

