from lxml import html, etree
from ics import Calendar, Event
import io
import datetime
#from django.utils.encoding import smart_str, smart_text
import django
from django.utils.encoding import smart_str
django.utils.encoding.smart_text = smart_str
from pyquery import PyQuery as pq
import requests
import MySQLdb
import os


##### The JQuery for "The Ultimate Fighter" Posters is:

# mw-content-text > table:nth-child(52) > tbody > tr:nth-child(2) > td
def month_converter(month):
    return {
        '1': '01',
        '2': '02',
        '3': '03',
        '4': '04',
        '5': '05',
        '6': '06',
        '7': '07',
        '8': '08',
        '9': '09',
        '10': '10',
        '11': '11',
        '12': '12'
    }[month]


def day_converter(day):
    if day == 1:
        newday = '01'
    elif day == 2:
        newday = '02'
    elif day == 3:
        newday = '03'
    elif day == 4:
        newday = '04'
    elif day == 5:
        newday = '05'
    elif day == 6:
        newday = '06'
    elif day == 7:
        newday = '07'
    elif day == 8:
        newday = '08'
    elif day == 9:
        newday = '09'
    else:
        newday = day

    return newday;

def end_day_converter(day,mth):
    if day == 1:
        endday = '02'
    elif day == 2:
        endday = '03'
    elif day == 3:
        endday = '04'
    elif day == 4:
        endday = '05'
    elif day == 5:
        endday = '06'
    elif day == 6:
        endday = '07'
    elif day == 7:
        endday = '08'
    elif day == 8:
        endday = '09'
    elif day == 9:
        endday = '10'
    elif day == 28 and mth == '02':
        endday = '01' 
    elif (day == 30) and (mth == '04' or mth == '06' or mth == '09' or mth == '11'):
        endday = '01'
    elif (day == 31) and (mth == '01' or mth == '03' or mth == '05' or mth == '07' or mth == '08' or mth == '10' or mth == '12'):
        endday = '01'
    else:
        endday = day + 1

    return endday;

def month_end_converter(day,mth):
    
    if (day == 28 or day == 29) and mth == '02':
        endmth = '03' 
    elif (day == 30) and (mth == '04' or mth == '06' or mth == '09' or mth == '11'):
        if mth == '04':
            endmth = '05'
        elif mth == '06':
            endmth = '07'
        elif mth == '09':
            endmth = '10'
        else:
            endmth = 12
    elif (day == 31) and (mth == '01' or mth == '03' or mth == '05' or mth == '07' or mth == '08' or mth == '10' or mth == '12'):
        if mth == '01':
            endmth = '02'
        elif mth == '03':
            endmth = '04'
        elif mth == '05':
            endmth = '06'
        elif mth == '07':
            endmth = '08'
        elif mth == '08':
            endmth = '09'
        elif mth == '10':
            endmth = '11'
        else:
            endmth = '01'
    else:
        endmth = mth

    return endmth;


def createEvents(event_date, event_fight_card_url, event_name, event_org):
    print('+++++++++++++++++++++++++++++')
    print('Event Date: ')
    print(event_date)
    print('Event_fight_card_url: ')
    print(event_fight_card_url)
    print('Event Name: ')
    print(event_name)
    if event_name == "Bellator 3":
        return;
    
    if event_name == "":
        return;
        
        
    print('Event org: ')
    print(event_org)
    e = Event()
    e.name = event_name
    
    if event_date == "":
        return

    # Strip leading and trailing whitespace from event_date
    event_date = event_date.strip()

    
    try:
        dt = datetime.datetime.strptime(event_date, "%B %d, %Y")
    except ValueError:
        dt = datetime.datetime.strptime(event_date, "%b %d, %Y")
    except ValueError: 
        dt = datetime.datetime.strptime(event_date, "%d %B %Y")
    
    print(dt.month)
    print(dt.day)
    print(dt.year)
    
    event_month = str(dt.month)
    event_day = dt.day
    event_year = dt.year


    newMonth = month_converter(event_month)
    newDay = day_converter(event_day)
    newDayEnd = end_day_converter(event_day,newMonth)
    newMonthEnd = month_end_converter(event_day,newMonth)

    print(newMonth, '  <---- this is my month value')
    print(newDay, '  <---- this is my day value')
    print(newDayEnd, '  <---- this is my end day value')
    
    print("Do some logic to determine end of year being on Dec 31, if so then we must make the event end on Jan 1 of a new year")
    
    intMonth = int(newMonth)
    intDay = int(newDay)
    
    
    if intMonth == 12 and intDay == 31: 
        print("This is the special block")
        event_year_special = int(event_year) + 1
        strEventYearSpecial = str(event_year_special)
        e.begin = "%s-%s-%s 22:00" % (event_year, newMonth, newDay)
        e.end = "%s-%s-%s 03:59" % (strEventYearSpecial, newMonthEnd, newDayEnd)
    else:
        print("this is the normal block")
        e.begin = "%s-%s-%s 22:00" % (event_year, newMonth, newDay)
        e.end = "%s-%s-%s 03:59" % (event_year, newMonthEnd, newDayEnd)
        
    e.url = event_fight_card_url
    #e.location = event_location

    MMACalendar.events.add(e)
    #print(MMACalendar.events)
    return;



# Database Connection
#db = MySQLdb.connect(host="markpereira.com",  # your host, usually localhost
#                     user="mark5463_ft_test",  # your username
#                     passwd="fttesting",  # your password
#                     db="mark5463_ft_prod")  # name of the data base

#db = MySQLdb.connect(host="dev-mysql.markpereira.com", user="root", passwd="fttesting", db="mark5463_ft_prod")
#remote mysql
#db = MySQLdb.connect(host="192.168.1.96", user="root", passwd="fttesting", port=3308, db="mark5463_ft_prod", charset="utf8")
#prod
db = MySQLdb.connect(
    host=os.environ['MYSQL_HOST'],
    user=os.environ['MYSQL_ID'],
    passwd=os.environ['MYSQL_PASSWORD'],
    db="mark5463_ft_prod",
    charset="utf8"
)


# Cursor object. It will let you execute the queries
cur = db.cursor()

# This section will delete the information on the table, for a clean run.


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

# fight poster specific arrays
# fight_card_poster = []
#fight_card_poster_url = []

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
for x in range(0, x_range):  # prev 0, 533
    # bring in the url information

    createEvents(event_date[x], event_fight_card_url[x], event_name[x], event_org[x])

    # time.sleep(5)

with open('all_events_test.ics', 'w') as f:
    f.writelines(MMACalendar)

