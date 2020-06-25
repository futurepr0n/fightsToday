from lxml import html, etree
from ics import Calendar, Event
import io
from django.utils.encoding import smart_str, smart_text
from pyquery import PyQuery as pq
import requests
import MySQLdb


##### The JQuery for "The Ultimate Fighter" Posters is:

# mw-content-text > table:nth-child(52) > tbody > tr:nth-child(2) > td
def month_converter(month):
    return {
        'Jan': '01',
        'Feb': '02',
        'Mar': '03',
        'Apr': '04',
        'May': '05',
        'Jun': '06',
        'Jul': '07',
        'Aug': '08',
        'Sep': '09',
        'Oct': '10',
        'Nov': '11',
        'Dec': '12'
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


def createEvents(event_day, event_fight_card_url, event_location, event_month, event_name, event_org, event_year):
    print('+++++++++++++++++++++++++++++')
    e = Event()
    e.name = event_name

    newMonth = month_converter(event_month)
    newDay = day_converter(event_day)
    newDayEnd = end_day_converter(event_day,newMonth)
    newMonthEnd = month_end_converter(event_day,newMonth)

    print(newMonth, '  <---- this is my month value')
    print(newDay, '  <---- this is my day value')
    print(newDayEnd, '  <---- this is my end day value')

    e.begin = "%s-%s-%s 22:00" % (event_year, newMonth, newDay)
    e.end = "%s-%s-%s 03:59" % (event_year, newMonthEnd, newDayEnd)
    e.url = event_fight_card_url
    e.location = event_location

    MMACalendar.events.add(e)
    print(MMACalendar.events)
    return;


# Database Connection
db = MySQLdb.connect(host="markpereira.com",  # your host, usually localhost
                     user="mark5463_ft_test",  # your username
                     passwd="fttesting",  # your password
                     db="mark5463_ft_prod")  # name of the data base

# Cursor object. It will let you execute the queries
cur = db.cursor()

# This section will delete the information on the table, for a clean run.


# This section will query the database and return all data in the table
cur.execute("SELECT event_day, event_fight_card_url, event_id, event_location, event_month, event_name, event_org, event_year FROM sd_mma_events")

# initialize the arrays
event_day = []
event_fight_card_url = []
event_id = []
event_location = []
event_month = []
event_name = []
event_org = []
event_year = []

MMACalendar = Calendar()

# fight poster specific arrays
# fight_card_poster = []
fight_card_poster_url = []

# load our arrays with all of our event data.
for row in cur.fetchall():
    event_day.append(row[0])
    event_fight_card_url.append(row[1])
    event_id.append(row[2])
    event_location.append(row[3])
    event_month.append(row[4])
    event_name.append(row[5])
    event_org.append(row[6])
    event_year.append(row[7])

x_range = len(event_name)

# This loops for every entry of event in the database to build our fight card information
for x in range(0, x_range):  # prev 0, 533
    # bring in the url information

    createEvents(event_day[x], event_fight_card_url[x], event_location[x], event_month[x], event_name[x], event_org[x],
                 event_year[x])

    # time.sleep(5)

with open('all_events.ics', 'w') as f:
    f.writelines(MMACalendar)

