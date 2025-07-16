from lxml import html, etree
from ics import Calendar, Event
import io
import datetime
import calendar
import logging
import django
from django.utils.encoding import smart_str
django.utils.encoding.smart_text = smart_str
from pyquery import PyQuery as pq
import requests
import MySQLdb
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Output to console
        logging.FileHandler('test_ics_generation.log')  # Output to file
    ]
)

def parse_event_date(event_date):
    """
    Parse event date string with support for various formats including incomplete dates.
    
    Args:
        event_date (str): The date string to parse
        
    Returns:
        datetime.datetime: Parsed date object, or None if parsing fails
    """
    if not event_date or event_date.strip() == "":
        return None
    
    # Strip whitespace
    event_date = event_date.strip()
    
    # List of date formats to try, in order of preference
    date_formats = [
        "%B %d, %Y",      # January 15, 2025
        "%b %d, %Y",      # Jan 15, 2025
        "%d %B %Y",       # 15 January 2025
        "%B %Y",          # January 2025 (incomplete - will default to 1st)
        "%b %Y",          # Jan 2025 (incomplete - will default to 1st)
        "%Y-%m-%d",       # 2025-01-15
        "%m/%d/%Y",       # 01/15/2025
        "%d/%m/%Y",       # 15/01/2025
    ]
    
    for date_format in date_formats:
        try:
            dt = datetime.datetime.strptime(event_date, date_format)
            # For month-only formats, the day will be 1 by default
            logging.info(f"Successfully parsed date '{event_date}' using format '{date_format}'")
            return dt
        except ValueError:
            continue
    
    # If no format worked, log the error and return None
    logging.warning(f"Unable to parse date: '{event_date}'. Skipping this event.")
    return None

def createEvents(event_date, event_fight_card_url, event_name, event_org, event_description):
    print('+++++++++++++++++++++++++++++')
    print('Event Date: ')
    print(event_date)
    print('Event_fight_card_url: ')
    print(event_fight_card_url)
    print('Event Name: ')
    print(event_name)
    if event_name == "Bellator 3":
        return

    if event_name == "":
        return

    print('Event org: ')
    print(event_org)
    e = Event()
    e.name = event_name
    
    # Parse the event date using our robust date parser
    dt = parse_event_date(event_date)
    
    # If date parsing failed, skip this event
    if dt is None:
        logging.warning(f"Skipping event '{event_name}' due to unparseable date: '{event_date}'")
        return
    
    print(dt.month)
    print(dt.day)
    print(dt.year)
    
    e.begin = dt
    e.make_all_day()  # Make it an all-day event
    e.url = event_fight_card_url
    e.description = event_description

    MMACalendar.events.add(e)
    return

def getFightBreakdown(event_name, wiki_event_id, cursor):
    query = """
    SELECT weightclass, fighter_one, fighter_two, event_past, method
    FROM wiki_mma_fight_cards
    WHERE event_name = %s AND wiki_event_id = %s
    ORDER BY CAST(SUBSTRING(wiki_fight_id, LOCATE('Fight', wiki_fight_id) + 5) AS UNSIGNED)
    """
    cursor.execute(query, (event_name, wiki_event_id))
    fight_breakdowns = cursor.fetchall()
    if fight_breakdowns and fight_breakdowns[0][3] == 1:  # Check if event_past is 1
        description = "Fight Card:\n"
        for fight in fight_breakdowns:
            weightclass, fighter_one, fighter_two, event_past, method = fight
            description += f"{weightclass} - {fighter_one} defeated {fighter_two} via {method}\n"
    else:
        description = "Fight Card:\n"
        for fight in fight_breakdowns:
            weightclass, fighter_one, fighter_two, event_past, method = fight
            description += f"{weightclass} - {fighter_one} vs {fighter_two}\n"
    return description

# Database Connection
db = MySQLdb.connect(
    host=os.environ['MYSQL_HOST'],
    user=os.environ['MYSQL_ID'],
    passwd=os.environ['MYSQL_PASSWORD'],
    db="mark5463_ft_prod",
    charset="utf8"
)

# Cursor object. It will let you execute the queries
cur = db.cursor()

# This section will query the database and return all data in the table
cur.execute("SELECT event_name, event_id, event_fight_card_url, event_org, event_date, wiki_event_id FROM wiki_mma_events")

# initialize the arrays
event_name = []
event_id = []
event_fight_card_url = []
event_org = []
event_date = []
wiki_event_id = []

MMACalendar = Calendar()

# load our arrays with all of our event data.
for row in cur.fetchall():
    event_name.append(row[0])
    event_id.append(row[1])
    event_fight_card_url.append(row[2])
    event_org.append(row[3])
    event_date.append(row[4])
    wiki_event_id.append(row[5])

x_range = len(event_name)

# This loops for every entry of event in the database to build our fight card information
for x in range(0, x_range):
    description = getFightBreakdown(event_name[x], wiki_event_id[x], cur)
    createEvents(event_date[x], event_fight_card_url[x], event_name[x], event_org[x], description)

with open('all_events.ics', 'w') as f:
    f.writelines(MMACalendar)
