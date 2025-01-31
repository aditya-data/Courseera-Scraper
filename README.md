# Scrapy Course Scraper

This repository contains a Scrapy-based web scraper designed to crawl and scrape metadata and textual reviews for courses from https://www.coursera.org/ in a specific field (e.g., Data Analytics). The scraped data is stored in a database for further analysis and use.

## Features
- Scrapes course metadata such as title, description, rating, instructor, number of learners liked, skills covered in the course, modules, etc.
- Extracts user reviews over several pages per course.
- Utilizes `.env` files to securely manage API keys and sensitive information.
- Supports integration with proxies to avoid blocking during large-scale scraping.
- Stores scraped data in a structured database.
- Dockerized for easy deployment and usage.

## Installation

### Option 1: Local Setup (Without Docker)

1. Clone the repository:
   ```bash
   git clone https://github.com/aditya-data/Courseera-Scraper.git
   cd coursescraper
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a .env file in the root directory to store sensitive data:
   ```bash
   SCRAPEOPS_API_KEY=your_scrapeops_api_key (Use your own API KEY here)
   DATABASE_URL=your_database_connection_string
   ```
5. Database Configuration ()
Update the DATABASE Connection settings in the pipeline file with your database connection string. Example for PostgreSQL:

   ```bash
   DATABASE_URL=postgresql://username:password@localhost:5432/database_name
   ```

6. Run the Scrapy spider:
   ```bash
   scrapy crawl coursespider
   ```

#### The scraped data will be stored in the configured database.

### Option 2: Dockerized Setup
This project is containerized with Docker, allowing for easy deployment and parallel scraping.

1. Pull the Docker Image: If you don’t have the Docker image yet, pull it from Docker Hub:

   ```bash
   docker pull adityadata/scrape
   ```
2. Run the Docker Container: Once the image is pulled, run the container with the necessary environment variables. You can use the following command (replace your_database_name with your actual database name and provide the necessary file paths for your URLs and JSON):

   ```bash
   docker run -v "$(pwd)/data:/usr/src/app/data" \
       -e DB_FILE="/usr/src/app/data/{web_development.db}" \
       -e JSON_FILE="/usr/src/app/data/{web_development.json}" \
       -e TABLE_NAME="{web_development}" \
       -e START_URL="{https://www.coursera.org/courses?query=web%20development}" \
       adityadata/scrapescrape
   ```
3. Replace the items inside curly braces with the appropriate values

4. Container Logs: The scraping process will run inside the container, and logs will be shown in the console. Check for any errors or successful scraping messages.

## Project Structure

## Description of Files and Folders

- **coursescraper/**: The main folder for the Scrapy project.
- **spiders/**: Contains the spiders that define the crawling logic.
- **middlewares.py**: Custom middleware for processing requests and responses.
- **pipelines.py**: Handles data processing and storage in a database.
- **settings.py**: Configuration settings for the Scrapy project.
- **.env**: Environment variables file, not tracked in Git for security reasons.
- **requirements.txt**: Lists the Python dependencies required for the project.
- **Dockerfile**: Instructions for building the container image for deployment.
- **README.md**: Documentation for understanding and using the project.


## Customization
- **Proxies:** Add proxy settings to avoid getting blocked during scraping. Use the `DOWNLOADER_MIDDLEWARES` in `settings.py`.
- **Fields to Scrape:** Modify the `parse` method in your spider to extract additional data fields.
## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request.
## License
This project is licensed under the MIT License.
## Contact
For any queries or suggestions, feel free to contact.