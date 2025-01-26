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
            if field_name not in ["what_to_learn", "skills_covered", "modules", "module_desc", "time_to_complete"]:
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

        # Process 'time_to_complete' field
        # time_to_complete = adapter.get("time_to_complete")  # The list you have described
        # if time_to_complete:
        #     # Step 1: We need to extract module names and their times in a robust manner
        #     modules_with_times = []
        #     for i in range(0, len(time_to_complete), 4):  # Every 4 elements form a module and its time
        #         module_name = time_to_complete[i]  # "Module 1"
        #         time = time_to_complete[i + 2]  # "2 hours" or "1 hour"
        #         if module_name.startswith('Module') and time:
        #             modules_with_times.append(f"{module_name} - {time}")
            
        #     # Step 2: Save the formatted result in the item
        #     adapter["time_to_complete"] = modules_with_times

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
            CREATE TABLE IF NOT EXISTS last_fetch (
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
                assignment_details VARCHAR(255),
                course_url VARCHAR(255),
                certificate VARCHAR(255),
                modules TEXT,
                modules_desc TEXT,
                time_to_complete TEXT,
                level_required VARCHAR(255),
                language_taught VARCHAR(255)              
            );
        """)

    def process_item(self, item, spider):
        # Prepare the SQL INSERT statement
        insert_query = """
            INSERT INTO remaining_courses_2 (
                title, company, instructor, num_enrolled, ratings, num_reviews, learners_liked, 
                what_to_learn, skills_covered, assignment_details, course_url, certificate, modules, 
                modules_desc, time_to_complete, level_required, language_taught
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """

        
        # Extract values from the item
        values = (
            item.get('title'),
            item.get('company'),
            item.get('instructor'),
            item.get('num_enrolled'),
            item.get('ratings'),
            item.get('num_reviews'),
            item.get('learners_liked'),
            str(item.get('what_to_learn')),
            str(item.get('skills_covered')),
            item.get('assignment_details'),
            item.get('url'),
            item.get('certificate'),
            str(item.get('modules')),
            str(item.get('modules_desc')),
            str(item.get('time_to_complete')),
            item.get('level_required'),
            item.get('language_taught')
        )

        
        # Execute the insert query
        self.cur.execute(insert_query, values)
        
        # Commit the transaction to save the data
        self.conn.commit()

        return item
    
    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()

