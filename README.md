# Scrapy Course Scraper

This repository contains a Scrapy-based web scraper designed to crawl and scrape metadata and textual reviews for courses from https://www.coursera.org/ in a specific field (e.g., Data Analytics). The scraped data is stored in a database for further analysis and use.

## Features
- Scrapes course metadata such as title, description, rating, instructor, number of learners liked, skills covered in the course, modules and so on.
- Extracts user reviews over several pages per course.
- Utilizes `.env` files to securely manage API keys and sensitive information.
- Supports integration with proxies to avoid blocking during large-scale scraping.
- Stores scraped data in a structured database.

## Installation
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

4. Create a `.env` file in the root directory to store sensitive data:
   ```
   SCRAPEOPS_API_KEY=your_scrapeops_api_key (Use your own API KEY here)
   ```

## Usage
1. Modify the `spiders` to define the target URLs and scraping logic.
2. Run the Scrapy spider:
   ```bash
   scrapy crawl coursespider
   ```
3. The scraped data will be stored in the configured database.

## Project Structure
```
.
├── coursescraper/             # Main Scrapy project folder
│   ├── spiders/               # Spiders folder containing crawling logic
│   ├── middlewares.py         # Custom middlewares
│   ├── pipelines.py           # Data processing and database storage
│   ├── settings.py            # Scrapy settings
├── .env                       # Environment variables file (not tracked in Git)
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
```

## Database Configuration
Update the `DATABASE_URL` in the `.env` file with your database connection string. Example for PostgreSQL:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/database_name
```

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
