# LinkedIn Job Scraper

## Overview
A Python-based LinkedIn job scraper with an interactive Streamlit dashboard for visualizing job data. The project scrapes job listings from LinkedIn and provides comprehensive data analysis through an intuitive web interface.

## Project Architecture

### Core Components
- **Scraper Scripts**: Multiple Python scripts for scraping LinkedIn job listings
  - `linkedin_job_scraper.py` - Main scraper entry point
  - `scraper_bot.py` and variants - Different scraping implementations
  - Uses Selenium with Chrome WebDriver for automation
  
- **Streamlit Dashboard** (`streamlit_dashboard.py`)
  - Interactive web interface for data visualization
  - File upload and CSV selection capabilities
  - Company, location, and job title analysis
  - Filter and search functionality

### Tech Stack
- **Language**: Python 3.11
- **Web Scraping**: Selenium, BeautifulSoup4
- **Data Processing**: pandas, numpy
- **Visualization**: matplotlib
- **Web Framework**: Streamlit
- **Browser Automation**: webdriver-manager (Chrome)

## Replit Environment Setup

### Development
- **Workflow**: Streamlit Dashboard on port 5000
- **Config**: `.streamlit/config.toml` configured for Replit's proxy environment
  - Server binds to `0.0.0.0:5000`
  - Browser config allows proxy connections (no serverAddress override)
  
### Deployment
- **Target**: Autoscale deployment (stateless)
- **Port**: Uses dynamic `$PORT` environment variable
- **Command**: `streamlit run streamlit_dashboard.py --server.address=0.0.0.0 --server.port=$PORT --server.headless=true`

## Recent Changes (2025-10-10)
- ✅ Created Streamlit dashboard (was missing from repository)
- ✅ Added Python 3.11 with all dependencies
- ✅ Configured Streamlit for Replit environment
- ✅ Fixed browser config to work with Replit's proxy
- ✅ Set up autoscale deployment with dynamic port
- ✅ Added comprehensive .gitignore for Python

## Data Structure
CSV files contain:
- Job Title
- Company
- Location  
- Post Date
- Link
- Search Keywords (optional)
- Search Location (optional)

## Usage
1. **View Dashboard**: The Streamlit dashboard runs automatically and displays job data
2. **Upload Data**: Use the file uploader to analyze new CSV files
3. **Run Scraper**: Execute `python linkedin_job_scraper.py` to scrape new data (requires LinkedIn credentials)

## Notes
- The scraper requires Chrome browser (handled by webdriver-manager)
- LinkedIn credentials needed for scraping (stored in .env file)
- Dashboard works with existing CSV files from previous scraping sessions
- For educational purposes - comply with LinkedIn's Terms of Service
