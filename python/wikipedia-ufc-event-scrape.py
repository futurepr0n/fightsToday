##################
# FILE HAS BEEN TESTED SUCCESSFULLY
# this file is ready for prod
#

from lxml import html, etree
import io
import time
import django
from django.utils.encoding import smart_str
django.utils.encoding.smart_text = smart_str
from pyquery import PyQuery as pq
import requests
import MySQLdb
import os

pe_num = 0
se_num = 0
te_num = 0

def get_db_connection(max_retries=3):
    for attempt in range(max_retries):
        try:
            return MySQLdb.connect(
                host=os.environ['MYSQL_HOST'],
                user=os.environ['MYSQL_ID'],
                passwd=os.environ['MYSQL_PASSWORD'],
                db="mark5463_ft_prod",
                charset="utf8"
            )
        except MySQLdb.OperationalError as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2)  # Wait 2 seconds before retrying

def execute_with_retry(cursor, query, params=None, max_retries=3):
    global db  # We need access to the global db connection
    for attempt in range(max_retries):
        try:
            # Execute the query
            if params:
                result = cursor.execute(query, params)
            else:
                result = cursor.execute(query)
            
            # Immediately commit the transaction
            db.commit()
            
            return result
            
        except (MySQLdb.OperationalError, MySQLdb.ProgrammingError) as e:
            if attempt == max_retries - 1:
                raise
            
            # For any database error, get a fresh connection
            try:
                cursor.close()
            except:
                pass
                
            db = get_db_connection()
            cursor = db.cursor()
            time.sleep(1)

def loadPastEventsData(event_url, event_org):
    #set up the lxml, load url to scrape
    page = requests.get('%s'%(event_url))
    tree = html.fromstring(page.content)

    #set up PyQuery section, load the url to scrape
    d = pq("<html></html>")
    d = pq(etree.fromstring("<html></html>"))
    d = pq(url='%s'%(event_url))

    #get the row length by querying the event table on table rows
    p = d("#Past_events tr")
    row_len = len(p)

    # ***** Creating the Files for autonomous runs *****
    pe_num = row_len - 1
    pe_string = "PAST_EVENTS = %i" %(pe_num)
    past_events = [pe_string]
 
    outF_pe = open("python/pastevents.py", "w")
    for line in past_events:
        print(line, file=outF_pe)
    outF_pe.close()

    #run through every row in the table
    for x in range(2, row_len+1):
        event_name_array = tree.xpath('//*[@id="Past_events"]/tbody/tr[%i]/td[2]/a/text()'%(x))
        newstr = ''.join(event_name_array)
        asccii_string = smart_str(newstr)

        if asccii_string == '':
            event_name_array = tree.xpath('//*[@id="Past_events"]/tbody/tr[%i]/td[2]/span/a/text()'%(x))
            newstr = ''.join(event_name_array)
            asccii_string = smart_str(newstr)
            event_name.append(asccii_string)
        else:
            event_name.append(asccii_string)

        event_fight_card_url_array = tree.xpath('//*[@id="Past_events"]/tbody/tr[%i]/td[2]/span/a/@href'%(x))
        newstr2 = ''.join(event_fight_card_url_array)
        asccii_string2 = smart_str(newstr2)

        if asccii_string2 == '':
            event_fight_card_url_array = tree.xpath('//*[@id="Past_events"]/tbody/tr[%i]/td[2]/a/@href'%(x))
            newstr2 = ''.join(event_fight_card_url_array)
            asccii_string2 = smart_str(newstr2)
            ev_fc_wbst = 'http://en.wikipedia.org', ''.join(asccii_string2)
            event_fight_card_url.append(ev_fc_wbst)
        else:
            ev_fc_wbst = 'http://en.wikipedia.org', ''.join(asccii_string2)
            event_fight_card_url.append(ev_fc_wbst)

        event_date_array = tree.xpath('//*[@id="Past_events"]/tbody/tr[%i]/td[3]/span/text()'%(x))
        event_date.append(event_date_array)
        ep_b = True
        db_ep_int = int(ep_b)
        event_past.append(db_ep_int)

    return row_len

def loadUpcomingEventsData(event_url, event_org):
    #set up the lxml, load url to scrape
    page = requests.get('%s'%(event_url))
    tree = html.fromstring(page.content)

    #set up PyQuery section, load the url to scrape
    d = pq("<html></html>")
    d = pq(etree.fromstring("<html></html>"))
    d = pq(url='%s'%(event_url))

    #get the row length by querying the event table on table rows
    p = d("#Scheduled_events tr")
    row_len = len(p)

    # Creating the Files for autonomous runs *****
    se_num = row_len - 1
    se_string = "SCHED_EVENTS = %i" %(se_num)
    sched_events = [se_string]

    outF_se = open("python/schedevents.py", "w")
    for line in sched_events:
        print(line, file=outF_se)
    outF_se.close()

    #run through every row in the table
    for x in range(2, row_len+1):
        event_name_array = None
        for xpath in ['//*[@id="Scheduled_events"]/tbody/tr[%i]/td[1]/a/text()',
                    '//*[@id="Scheduled_events"]/tbody/tr[%i]/td[1]/a/span/text()',
                    '//*[@id="Scheduled_events"]/tbody/tr[%i]/td[1]/text()',
                    '//*[@id="Scheduled_events"]/tbody/tr[%i]/td[1]/span/text()']:
            event_name_array = tree.xpath(xpath % x)
            if event_name_array:
                break

        if event_name_array:
            newstr = ''.join(event_name_array)
            asccii_string = smart_str(newstr)
            event_name.append(asccii_string)  
        else:
            event_name.append('UFC Event')  

        event_fight_card_url_array = tree.xpath('//*[@id="Scheduled_events"]/tbody/tr[%i]/td[1]/a/@href'%(x))
        newstr2 = ''.join(event_fight_card_url_array)
        asccii_string2 = smart_str(newstr2)
        ev_fc_wbst = 'http://en.wikipedia.org', ''.join(asccii_string2)
        event_fight_card_url.append(ev_fc_wbst)

        event_date_array = tree.xpath('//*[@id="Scheduled_events"]/tbody/tr[%i]/td[2]/span/text()'%(x))
        newstr3 = ''.join(event_date_array)
        ascii_string3 = smart_str(newstr3)

        if ascii_string3 == '':
            event_date_array = tree.xpath('//*[@id="Scheduled_events"]/tbody/tr[%i]/td[2]/text()'%(x))
            newstr3 = ''.join(event_date_array)
            ascii_string3 = smart_str(newstr3)
            event_date.append(ascii_string3)
        else:
            event_date.append(ascii_string3)
            
        ep_b = False
        db_ep_int = int(ep_b)
        event_past.append(db_ep_int)    

    return row_len

def insertRows(row_len, prev_row_ptr, array_pos, pe_b):
    global db, cur  # We need access to the global connection and cursor
    array_pos = array_pos + prev_row_ptr
    event_id = prev_row_ptr + row_len - 1

    for loopid in range(0, row_len-1):
        print('***********************************************************************************************')
        db_e_en = ''.join(event_name[array_pos])
        db_e_fc = ''.join(event_fight_card_url[array_pos])
        db_e_fd = ''.join(event_date[array_pos])
        w_e_id = event_org + str(event_id)
        db_e_p = pe_b
        db_int_ep = int(db_e_p)
        
        print('Adding event: %s ...' % db_e_en)
        print('Event ID: \t\t %i ' % event_id)
        print('Event Org: \t\t %s' % event_org)
        print('Event Date: \t', db_e_fd)
        print('Event URL: \t\t %s' % db_e_fc)
        print('Event Unique ID: \t', w_e_id)
        print('Event in the past?:\t', str(db_e_p))
        print('Event in the past as integer?: \t', db_int_ep)

        while True:  # Keep trying until successful or unrecoverable error
            try:
                # Check if the row exists
                query_select = "SELECT wiki_event_id FROM wiki_mma_events WHERE wiki_event_id = %s"
                execute_with_retry(cur, query_select, (w_e_id,))
                existing_row = cur.fetchone()
                
                if existing_row:
                    query_update = """
                        UPDATE wiki_mma_events
                        SET event_name = %s,
                            event_id = %s,
                            event_fight_card_url = %s,
                            event_org = %s,
                            event_date = %s,
                            event_past = %s
                        WHERE wiki_event_id = %s
                    """
                    values_update = (db_e_en, event_id, db_e_fc, event_org, db_e_fd, db_int_ep, w_e_id)
                    execute_with_retry(cur, query_update, values_update)
                else:
                    query_insert = """
                        INSERT INTO wiki_mma_events 
                        (event_name, event_id, event_fight_card_url, event_org, event_date, wiki_event_id, event_past)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """
                    values_insert = (db_e_en, event_id, db_e_fc, event_org, db_e_fd, w_e_id, db_int_ep)
                    execute_with_retry(cur, query_insert, values_insert)
                
                print('Success!...')
                break  # Exit the while loop if successful
                
            except (MySQLdb.OperationalError, MySQLdb.ProgrammingError) as e:
                print(f"Database error processing event {w_e_id}: {str(e)}")
                print("Attempting to reconnect...")
                # Get a fresh connection
                try:
                    cur.close()
                except:
                    pass
                try:
                    db.close()
                except:
                    pass
                    
                db = get_db_connection()
                cur = db.cursor()
                time.sleep(2)  # Wait before retrying
        except Exception as e:
            print(f"Error processing event {w_e_id}: {str(e)}")
            db.rollback()  # Rollback in case of error
            raise

        array_pos = (array_pos) + 1
        event_id = event_id - 1

    return

# Initialize our arrays
event_name = []
event_fight_card_url = []
event_date = []
prev_row_ptr = 0
array_pos = 0
event_past = []

print("*********************************************")
print("List of UFC Events Wikipedia Page URL Scrape...")
print("*********************************************")

# Set the event organization to UFC
event_org = 'UFC'
# Set the event url to wikipedia ufc section
event_url = 'https://en.wikipedia.org/wiki/List_of_UFC_events'
event_id = 0

# Initialize database connection
db = None
cur = None

try:
    db = get_db_connection()
    cur = db.cursor()

    # Process past events
    ufc_row_len = loadPastEventsData(event_url, event_org)
    pe2_num = ufc_row_len-1
    print(" ---- Inserts ----")
    insertRows(ufc_row_len, prev_row_ptr, array_pos, True)

    # Set the prev_row_ptr
    prev_row_ptr = ufc_row_len + prev_row_ptr - 1

    # Process upcoming events
    ufc_row_len2 = loadUpcomingEventsData(event_url, event_org)
    se2_num = ufc_row_len2-1
    print(" ---- Inserts ----")
    insertRows(ufc_row_len2, prev_row_ptr, array_pos, False)

    # Create the Files for autonomous runs
    print("The SE NUM = %i" %(se2_num))
    print("The PE NUM = %i" %(pe2_num))
    te_num = pe2_num + se2_num
    te_string = "TOTAL_EVENTS = %i" %(te_num)
    total_events = [te_string]
    print("The TE num = %i" %(te_num))
    
    outF_te = open("python/totalevents.py", "w")
    for line in total_events:
        print(line, file=outF_te)
    outF_te.close()

finally:
    if cur:
        cur.close()
    if db:
        db.close()
