import scrapy
import json
from coursescraper.items import CourseItem


class CoursespiderSpider(scrapy.Spider):
    name = "coursespider"
    allowed_domains = ["coursera.org"]
    start_urls = [
        "https://www.coursera.org/courses?query=data%20analytics&productTypeDescription=Courses"
    ]

    def parse(self, response):
        # Parse courses on the current query page
        courses = response.xpath("//div[@class='cds-ProductCard-header']//a")
        for course in courses:
            course_link = response.urljoin(course.attrib['href'])
            yield response.follow(course_link, callback=self.parse_course_page)

        # Handle pagination for query pages
        next_page = response.xpath("//a[@aria-label='Next Page']//@href").get()
        url = "https://www.coursera.org" + next_page
        if next_page:
            yield response.follow(url, callback=self.parse)

    def parse_course_page(self, response):
        # Extract course metadata
        company = response.xpath("//div[@data-e2e='hero-module']//img/@alt").get(default="N/A")
        title = response.xpath("//h1[@data-e2e='hero-title']/text()").get(default="N/A")
        instructor = response.xpath("//a[@data-track-component='hero_instructor']//text()").get(default="N/A")

        num_enrolled = response.xpath("//span[contains(text(), 'already enrolled')]/strong/span/text()").get(default="0")

        ratings = response.xpath(
            "//div[contains(@aria-label,'stars')]//text()"
        ).get(default="0")

        num_reviews = response.xpath(
            "//div[contains(@aria-label,'stars')]/parent::*/following-sibling::p/text()"
        ).get(default="0")

        learners_liked = response.xpath("//div[contains(text(), 'learners liked this course')]/preceding-sibling::div/div/span/text()").get(default="0")

        what_to_learn = response.xpath(
            "//div[@data-track-component='what_you_will_learn_section']//span/text()"
        ).getall()

        skills_covered = response.css("ul.css-yk0mzy li a::text").getall()

        assignment_details = response.xpath(
            "//div[contains(text(), 'Assessments')]/following-sibling::p[1]/text()").get()

        level_required = response.xpath("//div[@data-e2e='key-information']//div[contains(text(), 'level')]/text()").get(default="N/A")

        language_taught = response.xpath("//div[span[contains(text(), 'Taught in')]]/span/text()").get()


        certificate = response.xpath("//div[@class='css-1qfxccv']/text()").get(default="None")

        modules = response.xpath("//div[@data-track-component='syllabus']/div/div/div//h3/text()").getall()

        module_description = response.xpath("//div[@data-track-component='syllabus']/div/div/div//p/text()").getall()

        time_to_complete = response.xpath("//div[@data-track-component='syllabus']//div[@class='css-chglhw']//span/text()").getall()

        # Reviews page URL
        review_url = response.url + "/reviews"

        # Pass course metadata to the reviews page
        yield response.follow(
            review_url,
            callback=self.parse_reviews,
            meta={
                "company": company,
                "title": title,
                "instructor": instructor,
                "num_enrolled": num_enrolled,
                "ratings": ratings,
                "num_reviews": num_reviews,
                "learners_liked": learners_liked,
                "what_to_learn": what_to_learn,
                "skills_covered": skills_covered,
                "assignment_details": assignment_details,
                "course_url": response.url,
                "level_required": level_required,
                "language_taught": language_taught,
                "certificate": certificate,
                "modules": modules,
                "module_description": module_description,
                "time_to_complete": time_to_complete,
                "about": None,  # "About" will be fetched from the reviews page
                "reviews": [],  # Collect all reviews across pages
            },
        )

    def parse_reviews(self, response):
        # Retrieve course metadata
        course_metadata = response.meta

        # Scrape reviews from the current reviews page
        review_elements = response.xpath(
            "//div[@class='cds-9 css-o7qc23 cds-11 cds-grid-item cds-80']"
        )
        for review in review_elements:
            review_date = review.xpath(
                ".//p[@class='dateOfReview p-x-1s css-vac8rf']/text()"
            ).get(default="N/A")
            review_text = review.xpath(
                ".//div[@class='reviewText']//span/text()"
            ).get(default="No review text provided.")
            rating = review.xpath(".//span[@class='_13xsef79 d-inline-block']//text()").getall()
            rating = rating.count("Filled Star")

            # Append each review to the list of reviews in `meta`
            course_metadata["reviews"].append(
                {
                    "review_date": review_date,
                    "rating": rating,
                    "review_text": review_text,
                }
            )

        # Extract the "About" section (if available)
        if course_metadata["about"] is None:  # Only fetch "About" once
            course_metadata["about"] = response.xpath(
                "//div[@class='m-b-2']//span/text()"
            ).get(default="N/A")

        # Handle pagination for reviews
        next_page = response.xpath("//a[@aria-label='Go to next page']/@href").get()
        if next_page:
            yield response.follow(
                response.urljoin(next_page),
                callback=self.parse_reviews,
                meta=course_metadata,
            )
        else:
            # No more pages, yield the course item
            course_item = CourseItem()
            # Assign extracted data to the corresponding fields in the CourseItem
            course_item["title"] = course_metadata["title"]
            course_item["company"] = course_metadata["company"]
            course_item["instructor"] = course_metadata["instructor"]
            course_item["num_enrolled"] = course_metadata["num_enrolled"]
            course_item["ratings"] = course_metadata["ratings"]
            course_item["num_reviews"] = course_metadata["num_reviews"]
            course_item["learners_liked"] = course_metadata["learners_liked"]
            course_item["what_to_learn"] = json.dumps(course_metadata["what_to_learn"])
            course_item["skills_covered"] = json.dumps(course_metadata["skills_covered"])
            course_item["assignment_details"] = json.dumps(course_metadata["assignment_details"])
            course_item["about"] = course_metadata["about"]
            course_item["url"] = course_metadata["course_url"]
            course_item["certificate"] = course_metadata["certificate"]
            course_item["modules"] = json.dumps(course_metadata["modules"])
            course_item["modules_desc"] = json.dumps(course_metadata["module_description"])
            course_item["time_to_complete"] = json.dumps(course_metadata["time_to_complete"])
            course_item["level_required"] = course_metadata["level_required"]
            course_item["language_taught"] = course_metadata["language_taught"]
            course_item["learner_review_date"] = json.dumps([
                review["review_date"] for review in course_metadata["reviews"]
            ])
            course_item["learner_review_rating"] = json.dumps([
                review["rating"] for review in course_metadata["reviews"]
            ])
            course_item["learner_reviews"] = json.dumps([
                review["review_text"] for review in course_metadata["reviews"]
            ])

            # Yield the course item
            yield course_item
