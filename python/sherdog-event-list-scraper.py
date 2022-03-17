##################
# FILE HAS BEEN TESTED SUCCESSFULLY
# This File is READY for First Run in Prod

import MySQLdb
import requests
import io
from django.utils.encoding import smart_str
from lxml import html, etree
from pyquery import PyQuery as pq



def loadData(event_url, event_org, thisflag):
    # set up the lxml, load url to scrape
    hdr = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    page = requests.get('%s' % (event_url))
    tree = html.fromstring(page.content)

    # set up PyQuery section, load the url to scrape
    d = pq("<html></html>")
    d = pq(etree.fromstring("<html></html>"))
    d = pq(url='%s' % (event_url),headers=hdr)

    # get the row length by querying the event table on table rows
    # p = d(".event tr")
    if thisflag == 1:
        print("Setting Scrape to RECENT TAB")
        vtabnm = 'recent_tab'
        p = d("#recent_tab tr")
    else:
        print("Setting Scrape to UPCOMING TAB")
        vtabnm = 'upcoming_tab'
        p = d("#upcoming_tab tr")
    # set the row length
    row_len = len(p)

    # run through every row in the table
    for x in range(2, row_len + 1):
        # scrape ufc event name
        event_name_array = tree.xpath('//*[@id="%s"]/table/tr[%i]/td[2]/a/span/text()' % (vtabnm,x))
        # event_parse = re.sub('[-.]', '', event_name_array)
        g_event_name.append(event_name_array)

        # scrape event month
        event_month_array = tree.xpath('//*[@id="%s"]/table/tr[%i]/td[1]/div/div[1]/text()' % (vtabnm,x))

        g_event_month.append(event_month_array)

        # scrape event day
        event_day_array = tree.xpath('//*[@id="%s"]/table/tr[%i]/td[1]/div/div[2]/text()' % (vtabnm,x))

        g_event_day.append(event_day_array)

        # scrape event year
        event_year_array = tree.xpath('//*[@id="%s"]/table/tr[%i]/td[1]/div/div[3]/text()' % (vtabnm,x))

        g_event_year.append(event_year_array)

        # scrape event fight card URL
        event_fight_card_url_array = tree.xpath('//*[@id="%s"]/table/tr[%i]/td[2]/a/@href' % (vtabnm,x))
                                                 
        ev_fc_wbst = 'http://www.sherdog.com', ''.join(event_fight_card_url_array)
        g_event_fight_card_url.append(ev_fc_wbst)

        # scrape event location
        event_location_array = tree.xpath('//*[@id="%s"]/table/tr[%i]/td[3]/text()' % (vtabnm,x))
        
        newstr = ''.join(event_location_array)
        asccii_string = smart_str(newstr)
        g_event_location.append(asccii_string)
    return row_len;


def insertRows(row_len, total_event, prev_row_ptr, array_pos):
    # set the array position
    array_pos = array_pos + prev_row_ptr
    event_id = total_event - 1

    # loop through all the rows
    for loopid in range(0, row_len - 1):
        # set the event id

        print('***********************************************************************************************')
        db_e_en = ''.join(g_event_name[array_pos])
        db_e_ev = ''.join(g_event_month[array_pos])
        db_e_ed = ''.join((g_event_day[array_pos]))
        db_e_ey = ''.join((g_event_year[array_pos]))
        db_e_fc = ''.join(g_event_fight_card_url[array_pos])
        db_e_lc = ''.join(g_event_location[array_pos])
        db_sd_ev_id = g_event_org + str(event_id)
        print('Adding event: %s ...' % db_e_en)
        print('Event ID: \t\t %i ' % event_id)
        print('Event Org: \t\t %s' % g_event_org)
        print('Event Date: \t', db_e_ed,'-', db_e_ev, '-', db_e_ey)
        print('Event Location: \t %s' % db_e_lc)
        print('Event URL: \t\t %s' % db_e_fc)
        print('Event Unique ID: \t ', db_sd_ev_id)
        print('***********************************************************************************************')
        query = "INSERT INTO sd_mma_events (event_name, event_month, event_day, event_year, event_id, event_fight_card_url, event_org, event_location, sd_event_id) VALUES (\"%s\",\'%s\',%s,%s,%i,\"%s\",\"%s\",\"%s\", \"%s\")" % (db_e_en, db_e_ev, db_e_ed, db_e_ey, event_id, db_e_fc, g_event_org, db_e_lc, db_sd_ev_id)
        # print(query) # -- This is so we can see the query, Commented out
        print('***********************************************************************************************')
        # commenting out the query since we are loaded in the db right now
        print('Query Executed...')
        cur.execute(query)
        print('Success!...')
        print('***********************************************************************************************')
        array_pos = (array_pos) + 1
        event_id = event_id - 1
    prev_row_ptr = prev_row_ptr + row_len

    return;


# Database Connection
# db = MySQLdb.connect(host="markpereira.com", user="mark5463_ft_test", passwd="fttesting", db="mark5463_ft_prod")
db = MySQLdb.connect(host="dev-mysql.markpereira.com", user="root", passwd="fttesting", db="mark5463_ft_prod")


# Cursor object. It will let you execute the queries
cur = db.cursor()

# This section will delete the information on the table, for a clean run.
print("clear the table")
cur.execute("TRUNCATE sd_mma_events")

# Scrape UFC Information
# initialize our arrays. our Arrays.
g_event_name = []
g_event_month = []
g_event_day = []
g_event_year = []
g_event_location = []
g_event_fight_card_url = []
prev_row_ptr = 0
array_pos = 0
ufc_total_events = 0
bellator_total_events = 0

print("*********************************************")
print("UFC Section Scrape Page 7...")
print("*********************************************")
# set the event organization to UFC
g_event_org = 'UFC'
# set the event url to sherdog ufc section
# event_url = 'http://www.sherdog.com/organizations/Ultimate-Fighting-Championship-2'
g_event_url = 'http://www.sherdog.com/organizations/Ultimate-Fighting-Championship-2/recent-events/7'
# reset the event id
g_event_id = 0

ufc_row_len = loadData(g_event_url, g_event_org, 1)
ufc_total_events = ufc_total_events + ufc_row_len
print(" ---- Inserts ----")

# insertRows(ufc_row_len, prev_row_ptr, array_pos)
insertRows(ufc_row_len, ufc_total_events, prev_row_ptr, array_pos)

prev_row_ptr = ufc_row_len + prev_row_ptr - 1

print("*********************************************")
print("UFC Section Scrape Page 6...")
print("*********************************************")
# set the event organization to UFC
g_event_org = 'UFC'
# set the event url to sherdog ufc section
# event_url = 'http://www.sherdog.com/organizations/Ultimate-Fighting-Championship-2'
g_event_url = 'http://www.sherdog.com/organizations/Ultimate-Fighting-Championship-2/recent-events/6'
# reset the event id
g_event_id = 0

ufc_row_len = loadData(g_event_url, g_event_org, 1)
ufc_total_events = ufc_total_events + ufc_row_len
print(" ---- Inserts ----")

# insertRows(ufc_row_len, prev_row_ptr, array_pos)
insertRows(ufc_row_len, ufc_total_events, prev_row_ptr, array_pos)

prev_row_ptr = ufc_row_len + prev_row_ptr - 1


print("*********************************************")
print("UFC Section Scrape Page 5...")
print("*********************************************")
# set the event organization to UFC
g_event_org = 'UFC'
# set the event url to sherdog ufc section
# event_url = 'http://www.sherdog.com/organizations/Ultimate-Fighting-Championship-2'
g_event_url = 'http://www.sherdog.com/organizations/Ultimate-Fighting-Championship-2/recent-events/5'
# reset the event id
g_event_id = 0

ufc_row_len = loadData(g_event_url, g_event_org, 1)
ufc_total_events = ufc_total_events + ufc_row_len
print(" ---- Inserts ----")

# insertRows(ufc_row_len, prev_row_ptr, array_pos)
insertRows(ufc_row_len, ufc_total_events, prev_row_ptr, array_pos)

prev_row_ptr = ufc_row_len + prev_row_ptr - 1

# set the prev_row_ptrgth pointer

print("*********************************************")
print("UFC Section Scrape Page 4...")
print("*********************************************")
# set the event organization to UFC
g_event_org = 'UFC'
# set the event url to sherdog ufc section
# event_url = 'http://www.sherdog.com/organizations/Ultimate-Fighting-Championship-2'
g_event_url = 'http://www.sherdog.com/organizations/Ultimate-Fighting-Championship-2/recent-events/4'
# reset the event id
# event_id = 0

ufc_row_len = loadData(g_event_url, g_event_org, 1)
ufc_total_events = ufc_total_events + ufc_row_len
print(" ---- Inserts ----")
# insertRows(ufc_row_len, prev_row_ptr, array_pos)
insertRows(ufc_row_len, ufc_total_events, prev_row_ptr, array_pos)

# set the prev_row_ptrgth pointer
prev_row_ptr = ufc_row_len + prev_row_ptr - 1

print("*********************************************")
print("UFC Section Scrape Page 3...")
print("*********************************************")
# set the event organization to UFC
g_event_org = 'UFC'
# set the event url to sherdog ufc section
# event_url = 'http://www.sherdog.com/organizations/Ultimate-Fighting-Championship-2'
g_event_url = 'http://www.sherdog.com/organizations/Ultimate-Fighting-Championship-2/recent-events/3'
# reset the event id
# event_id = 0

ufc_row_len = loadData(g_event_url, g_event_org, 1)
ufc_total_events = ufc_total_events + ufc_row_len
print(" ---- Inserts ----")
# insertRows(ufc_row_len, prev_row_ptr, array_pos)
insertRows(ufc_row_len, ufc_total_events, prev_row_ptr, array_pos)

# set the prev_row_ptrgth pointer
prev_row_ptr = ufc_row_len + prev_row_ptr - 1

print("*********************************************")
print("UFC Section Scrape Page 2 ...")
print("*********************************************")
# set the event organization to UFC
g_event_org = 'UFC'
# set the event url to sherdog ufc section
# event_url = 'http://www.sherdog.com/organizations/Ultimate-Fighting-Championship-2'
g_event_url = 'http://www.sherdog.com/organizations/Ultimate-Fighting-Championship-2/recent-events/2'
# reset the event id
# event_id = 0

ufc_row_len = loadData(g_event_url, g_event_org, 1)
ufc_total_events = ufc_total_events + ufc_row_len
print(" ---- Inserts ----")
# insertRows(ufc_row_len, prev_row_ptr, array_pos)
insertRows(ufc_row_len, ufc_total_events, prev_row_ptr, array_pos)

# set the prev_row_ptrgth pointer
prev_row_ptr = ufc_row_len + prev_row_ptr - 1

print("*********************************************")
print("UFC Section Scrape Page 1...")
print("*********************************************")
# set the event organization to UFC
g_event_org = 'UFC'
# set the event url to sherdog ufc section
# event_url = 'http://www.sherdog.com/organizations/Ultimate-Fighting-Championship-2'
g_event_url = 'http://www.sherdog.com/organizations/Ultimate-Fighting-Championship-2/recent-events/1'
# reset the event id
# event_id = 0

ufc_row_len = loadData(g_event_url, g_event_org, 1)
ufc_total_events = ufc_total_events + ufc_row_len
print(" ---- Inserts ----")
# insertRows(ufc_row_len, prev_row_ptr, array_pos)
insertRows(ufc_row_len, ufc_total_events, prev_row_ptr, array_pos)

# set the prev_row_ptrgth pointer
prev_row_ptr = ufc_row_len + prev_row_ptr - 1

print("*********************************************")
print("UFC Section Upcoming Events Scrape...")
print("*********************************************")
# set the event organization to UFC
g_event_org = 'UFC'
# set the event url to sherdog ufc section
# event_url = 'http://www.sherdog.com/organizations/Ultimate-Fighting-Championship-2'
g_event_url = 'http://www.sherdog.com/organizations/Ultimate-Fighting-Championship-2/upcoming-events/1'
# reset the event id
# event_id = 0
ufc_row_len = loadData(g_event_url, g_event_org, 0)
ufc_total_events = ufc_total_events + ufc_row_len
print(" ---- Inserts ----")
# insertRows(ufc_row_len, prev_row_ptr, array_pos)
insertRows(ufc_row_len, ufc_total_events, prev_row_ptr, array_pos)

# set the prev_row_ptrgth pointer
prev_row_ptr = ufc_row_len + prev_row_ptr - 1

# Start Bellator Section
print("*********************************************")
print("Bellator Section Scrape Page 3...")
print("*********************************************")
# reset the event id
# event_id = 0
# set the event url to sherdog bellator section
g_event_url = 'https://www.sherdog.com/organizations/Bellator-MMA-1960/recent-events/3'
# set the event organization to Bellator
g_event_org = 'Bellator'

# Load the Bellator Data
bellator_row_len = loadData(g_event_url, g_event_org, 1)
bellator_total_events = bellator_row_len + bellator_total_events
# insert the Bellator Data
insertRows(bellator_row_len, bellator_total_events, prev_row_ptr, array_pos)
# set the prev_row_ptrgth pointer
prev_row_ptr = bellator_row_len + prev_row_ptr - 1

print("*********************************************")
print("Bellator Section Scrape Page 2...")
print("*********************************************")
# reset the event id
# event_id = 0
# set the event url to sherdog bellator section
g_event_url = 'https://www.sherdog.com/organizations/Bellator-MMA-1960/recent-events/2'
# set the event organization to Bellator
g_event_org = 'Bellator'

# Load the Bellator Data
bellator_row_len = loadData(g_event_url, g_event_org, 1)
bellator_total_events = bellator_row_len + bellator_total_events
# insert the Bellator Data
insertRows(bellator_row_len, bellator_total_events, prev_row_ptr, array_pos)
# set the prev_row_ptrgth pointer
prev_row_ptr = bellator_row_len + prev_row_ptr - 1

print("*********************************************")
print("Bellator Section Scrape Page 1...")
print("*********************************************")
# reset the event id
# event_id = 0
# set the event url to sherdog bellator section
g_event_url = 'https://www.sherdog.com/organizations/Bellator-MMA-1960/recent-events/1'
# set the event organization to Bellator
g_event_org = 'Bellator'
# Load the Bellator Data
bellator_row_len = loadData(g_event_url, g_event_org, 1)
bellator_total_events = bellator_row_len + bellator_total_events
# insert the Bellator Data
insertRows(bellator_row_len, bellator_total_events, prev_row_ptr, array_pos)
# set the prev_row_ptrgth pointer
prev_row_ptr = bellator_row_len + prev_row_ptr - 1

print("*********************************************")
print("Bellator Upcoming Section Scrape...")
print("*********************************************")
# set the event organization to UFC
g_event_org = 'Bellator'
g_event_url = 'https://www.sherdog.com/organizations/Bellator-1960/upcoming-events/1'
# reset the event id
# # event_id = 0
bellator_row_len = loadData(g_event_url, g_event_org, 0)
bellator_total_events = bellator_row_len + bellator_total_events
# insert the Bellator Data
insertRows(bellator_row_len, bellator_total_events, prev_row_ptr, array_pos)
# set the prev_row_ptrgth pointer
prev_row_ptr = ufc_row_len + prev_row_ptr - 1
