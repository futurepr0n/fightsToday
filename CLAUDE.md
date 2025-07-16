# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

fightsToday is a web scraping and data aggregation system for MMA (Mixed Martial Arts) events. It collects event information from multiple sources (Sherdog, Wikipedia) and generates HTML pages and ICS calendar files.

## Key Commands

### Environment Setup
```bash
# Install Python dependencies using pipenv
pipenv install -r requirements.txt

# For deployment/CI environments
pipenv install -r requirements.txt --deploy --skip-lock
```

### Data Collection Pipeline
Execute scrapers in this specific order:
```bash
# 1. Sherdog scrapes
pipenv run python python/sherdog-event-list-scraper.py
pipenv run python python/sherdog-fight-card-scrape.py

# 2. Wikipedia scrapes  
pipenv run python python/wikipedia-bellator-event-scrape.py
pipenv run python python/wikipedia-ufc-event-scrape.py
pipenv run python python/wikipedia-ufc-poster-scrape.py
pipenv run python python/wikipedia-fight-card-scrape.py

# Additional PFL scrapes if needed
pipenv run python python/wikipedia-pfl-event-scrape.py
pipenv run python python/wikipedia-pfl-fight-card-scrape.py
pipenv run python python/wikipedia-pfl-poster-scrape.py
```

### HTML and ICS Generation
```bash
# Generate HTML page (requires UTF-8 encoding afterward)
pipenv run python python/generate-html.py > index.html

# Generate ICS calendar file
pipenv run python python/generate-ics.py
```

## Architecture

### Data Flow
1. **Scrapers** → Extract event data from Sherdog and Wikipedia
2. **MySQL Database** → Store scraped data in normalized tables
3. **Generators** → Create HTML pages and ICS calendar files from DB data

### Database Structure
- **sd_mma_events**: Sherdog event data (event details, dates, locations)
- **sd_mma_fight_cards**: Sherdog fight card matchups
- **wiki_mma_events**: Wikipedia event data
- **wiki_mma_events_poster**: Event poster URLs from Wikipedia
- **wiki_mma_fight_cards**: Wikipedia fight card matchups

### Database Connection
All scrapers use the same connection pattern:
```python
db = MySQLdb.connect(
    host="markpereira.com",
    user="mark5463_ft_test", 
    passwd="fttesting",
    db="mark5463_ft_testdb"
)
```

### Key Technologies
- **Python 3.7+** with pipenv for dependency management
- **MySQL/MariaDB** for data storage
- **Web scraping**: lxml, PyQuery, requests
- **Calendar generation**: ics library
- **CI/CD**: Jenkins with Docker containers

## Important Patterns

### Scraper Structure
All scrapers follow a similar pattern:
1. Connect to MySQL database
2. Truncate target tables (to ensure fresh data)
3. Fetch and parse HTML using lxml/PyQuery
4. Extract data using XPath selectors
5. Insert data into appropriate tables
6. Handle organization-specific logic (UFC, Bellator, PFL)

### Error Handling Considerations
- Scrapers retry on connection failures
- Empty fight cards are handled specially for PFL events
- Fighter names/URLs may be missing and need validation

### Jenkins Pipeline
The Jenkinsfile orchestrates the entire build process:
1. Prepares Python environment
2. Spins up MySQL Docker container for testing
3. Loads database schema
4. Executes scrapers in sequence
5. Generates output files

## Current Limitations & TODOs
- HTML output requires manual UTF-8 encoding
- No automated tests yet
- Wikipedia and Sherdog data merging via SQL Views not yet implemented
- ICS generation needs poster integration
- Need system for updating only upcoming events (not full historical scrape)