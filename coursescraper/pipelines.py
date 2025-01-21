# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import re
from itemadapter import ItemAdapter

class CoursescraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        field_names = adapter.field_names()

        # Strip whitespace for all fields except certain ones
        for field_name in field_names:
            if field_name not in ["learner_review_rating", "learner_review_date", "learner_reviews", "what_to_learn", "skills_covered"]:
                value = adapter.get(field_name)
                if isinstance(value, str):
                    adapter[field_name] = value.strip()

        # Process 'num_enrolled' field
        value = adapter.get("num_enrolled")  # e.g., "542,222"
        if value:
            adapter["num_enrolled"] = int(value.replace(",", ""))

        # Process 'ratings' field
        value = adapter.get("ratings")  # e.g., "4.8 stars"
        if value:
            match = re.search(r"(\d+\.\d+)", value)  # Extract float number
            if match:
                adapter["ratings"] = float(match.group(1))

        # Process 'num_reviews' field
        value = adapter.get("num_reviews")  # e.g., "(16,419 reviews)"
        if value:
            match = re.search(r"(\d[\d,]*)", value)  # Extract numbers with commas
            if match:
                adapter["num_reviews"] = int(match.group(1).replace(",", ""))

        # Process 'learners_liked' field
        value = adapter.get("learners_liked")  # e.g., "99%"
        if value:
            adapter["learners_liked"] = float(value.replace("%", ""))

        return item
    
import mysql.connector

class saveToMySQLPipeline:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345678",
            database="Courses"
        )

        self.cur = self.conn.cursor()

        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS course_data (
                id INT AUTO_INCREMENT PRIMARY KEY,  -- Use AUTO_INCREMENT for primary key in MySQL
                title VARCHAR(255) NOT NULL,
                company VARCHAR(255),
                instructor VARCHAR(255),
                num_enrolled INT,
                ratings FLOAT,
                num_reviews INT,
                learners_liked FLOAT,
                what_to_learn TEXT,
                skills_covered TEXT,
                assignment_details TEXT,
                course_url VARCHAR(255),
                about TEXT,
                learner_review_date LONGTEXT,  -- Store as comma-separated list or JSON
                learner_review_rating LONGTEXT,  -- Store as comma-separated list or JSON
                learner_reviews LONGTEXT  -- Store as comma-separated list or JSON
            );
        """)

    def process_item(self, item, spider):
        # Prepare the SQL INSERT statement
        insert_query = """
            INSERT INTO course_data (
                title, company, instructor, num_enrolled, ratings, num_reviews, learners_liked, 
                what_to_learn, skills_covered, assignment_details, course_url, about, learner_review_date, 
                learner_review_rating, learner_reviews
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        
        # Extract values from the item
        values = (
            item['title'],
            item['company'],
            item['instructor'],
            item['num_enrolled'],
            item['ratings'],
            item['num_reviews'],
            item['learners_liked'],
            str(item['what_to_learn']),
            str(item['skills_covered']),
            item['assignment_details'],
            item['url'],
            item['about'],
            str(item['learner_review_date']),  # Convert lists to string or JSON as needed
            str(item['learner_review_rating']),
            str(item['learner_reviews'])
        )
        
        # Execute the insert query
        self.cur.execute(insert_query, values)
        
        # Commit the transaction to save the data
        self.conn.commit()

        return item
    
    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()

