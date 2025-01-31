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
Create a virtual environment and activate it:


python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies:


pip install -r requirements.txt
Create a .env file in the root directory to store sensitive data:


SCRAPEOPS_API_KEY=your_scrapeops_api_key (Use your own API KEY here)
DATABASE_URL=your_database_connection_string
Run the Scrapy spider:


scrapy crawl coursespider
The scraped data will be stored in the configured database.

Option 2: Dockerized Setup
This project is containerized with Docker, allowing for easy deployment and parallel scraping.

Pull the Docker Image: If you don’t have the Docker image yet, pull it from Docker Hub:


docker pull adityadata/scrape
Run the Docker Container: Once the image is pulled, run the container with the necessary environment variables. You can use the following command (replace your_database_name with your actual database name and provide the necessary file paths for your URLs and JSON):


docker run --env-file .env -v /path/to/urls:/app/urls -v /path/to/json:/app/json adityadata/scrape
Ensure the .env file contains all the necessary environment variables such as SCRAPEOPS_API_KEY and DATABASE_URL.
Replace /path/to/urls and /path/to/json with the appropriate file paths on your local system.
Container Logs: The scraping process will run inside the container, and logs will be shown in the console. Check for any errors or successful scraping messages.

Project Structure
.
├── coursescraper/             # Main Scrapy project folder
│   ├── spiders/               # Spiders folder containing crawling logic
│   ├── middlewares.py         # Custom middlewares
│   ├── pipelines.py           # Data processing and database storage
│   ├── settings.py            # Scrapy settings
├── .env                       # Environment variables file (not tracked in Git)
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Dockerfile to build the container image
├── README.md                  # Project documentation
Database Configuration
Update the DATABASE_URL in the .env file with your database connection string. Example for PostgreSQL:


DATABASE_URL=postgresql://username:password@localhost:5432/database_name
Customization
Proxies: Add proxy settings to avoid getting blocked during scraping. Use the DOWNLOADER_MIDDLEWARES in settings.py.
Fields to Scrape: Modify the parse method in your spider to extract additional data fields.
Contributing
Contributions are welcome! Please follow these steps:

Fork the repository.
Create a new branch for your feature or bug fix.
Submit a pull request.
License
This project is licensed under the MIT License.

Contact
For any queries or suggestions, feel free to contact.