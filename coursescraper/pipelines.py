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

    
import sqlite3
import json
import os

class SaveToSQLiteAndJSONPipeline:
    def __init__(self):
        # SQLite setup
        self.json_file_name = os.environ.get("JSON_FILE", "/usr/src/app/data/courses.json")
        self.db_file_name = os.environ.get("DB_FILE", "/usr/src/app/data/courses.db")


        # SQLite connection setup
        self.conn = sqlite3.connect(self.db_file_name)  # Creates or connects to SQLite database
        self.cur = self.conn.cursor()

        # Ensure that the table name is dynamic based on the input (e.g., spider name)
        self.table_name = os.environ.get("TABLE_NAME", "courses")  # Default to 'courses' if no table name is provided

        # Create the table dynamically based on the prompt or the provided table name
        self.cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                company TEXT,
                instructor TEXT,
                num_enrolled INTEGER,
                ratings REAL,
                num_reviews INTEGER,
                learners_liked REAL,
                what_to_learn TEXT,
                skills_covered TEXT,
                assignment_details TEXT,
                course_url TEXT,
                certificate TEXT,
                modules TEXT,
                modules_desc TEXT,
                time_to_complete TEXT,
                level_required TEXT,
                language_taught TEXT,
                about TEXT
            );
        """)

        # JSON file setup: Open the JSON file for appending data
        self.json_file = open(self.json_file_name, "w", encoding="utf-8")
        self.json_file.write("[")  # Start JSON array
        self.first_item = True  # To manage commas between JSON objects

    def process_item(self, item, spider):
        # Insert the course data into the dynamically-named SQLite database table
        insert_query = f"""
            INSERT INTO {self.table_name} (
                title, company, instructor, num_enrolled, ratings, num_reviews, learners_liked, 
                what_to_learn, skills_covered, assignment_details, course_url, certificate, modules, 
                modules_desc, time_to_complete, level_required, language_taught, about
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """

        values = (
            item.get('title'),
            item.get('company'),
            item.get('instructor'),
            item.get('num_enrolled'),
            item.get('ratings'),
            item.get('num_reviews'),
            item.get('learners_liked'),
            str(item.get('what_to_learn', "")),
            str(item.get('skills_covered', "")),
            item.get('assignment_details'),
            item.get('url'),
            item.get('certificate'),
            str(item.get('modules', "")),
            str(item.get('modules_desc', "")),
            str(item.get('time_to_complete', "")),
            item.get('level_required'),
            item.get('language_taught'),
            item.get("about")
        )

        self.cur.execute(insert_query, values)
        self.conn.commit()

        # Append the item to the JSON file
        if not self.first_item:
            self.json_file.write(",\n")  # Add a comma before the next JSON object
        self.json_file.write(json.dumps(dict(item), ensure_ascii=False, indent=4))
        self.first_item = False

        return item

    def close_spider(self, spider):
        # Close the SQLite connection
        self.cur.close()
        self.conn.close()

        # Close the JSON array properly
        self.json_file.write("\n]")  # Close the JSON array
        self.json_file.close()
