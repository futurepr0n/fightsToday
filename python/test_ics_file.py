from lxml import html, etree
from ics import Calendar, Event
import io
import datetime
import django
from django.utils.encoding import smart_str
django.utils.encoding.smart_text = smart_str
from pyquery import PyQuery as pq
import requests
import MySQLdb
import os

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
    
    if event_date == "":
        return
    
    try:
        dt = datetime.datetime.strptime(event_date, "%B %d, %Y")
    except ValueError:
        dt = datetime.datetime.strptime(event_date, "%b %d, %Y")
    except ValueError: 
        dt = datetime.datetime.strptime(event_date, "%d %B %Y")
    
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
