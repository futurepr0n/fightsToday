##################
# FILE HAS not been TESTED SUCCESSFULLY
# this is attempting to add logic to the bellator side
#

from lxml import html, etree
import io
#from django.utils.encoding import smart_str, smart_text
import django
from django.utils.encoding import smart_str
django.utils.encoding.smart_text = smart_str
from pyquery import PyQuery as pq
from datetime import datetime, date
import requests
import MySQLdb
import os

bellator_pe_num = 0
bellator_se_num = 0
bellator_te_num = 0 

def loadEventsData (event_url, event_org):
    #set up the lxml, load url to scrape
    page = requests.get('%s'%(event_url))
    tree = html.fromstring(page.content)

    #set up PyQuery section, load the url to scrape
    d = pq("<html></html>")
    d = pq(etree.fromstring("<html></html>"))
    d = pq(url='%s'%(event_url))

    ### First thing I am going to try doing is query through the past events.
    ### We will get their Event Names, Event URL, Event ID

    # get the row length by querying the event table on table rows
    p = d("#mw-content-text tr")
    #p = d("#mw-content-text > div.mw-parser-output > table > tbody >")
    

    # JQUERY STUFF --  THIS will calculate the rows for Upcoming Events (Scheduled Events)
    # $("#Scheduled_events tr").length

    # THIS will query against the table for Past Event Info
    # $("table:nth-child(16) tr").length

    #set the row length
    row_len = len(p)

    print('The Row Length is %i'%(row_len))
    for x in range (1, row_len-33):
      event_name_array = tree.xpath('//*[@id="mw-content-text"]/div[1]/table[1]/tbody/tr[%i]/td[1]/a/text()'%(x))
      new_event_name_str = ''.join(event_name_array)
      ascii_event_name_string = smart_str(new_event_name_str)
      print('event td[2]: %s ...' % ascii_event_name_string)
    
      event_fight_card_url_array = tree.xpath('//*[@id="mw-content-text"]/div[1]/table[1]/tbody/tr[%i]/td[1]/a/@href'%(x))
      new_fight_card_url_str = ''.join(event_fight_card_url_array)
      ascii_fight_card_url_string = smart_str(new_fight_card_url_str)
      print('Event URL: \t\t %s' % ascii_fight_card_url_string)

      if ascii_event_name_string == '':  # Try the italic version
        print('Since I found no event name, I am now trying another field - italicized td2')
        event_name_array = tree.xpath('//*[@id="mw-content-text"]/div[1]/table[1]/tbody/tr[%i]/td[1]/i/a/text()'%(x))
        new_event_name_str = ''.join(event_name_array)
        ascii_event_name_string = smart_str(new_event_name_str)
        print('event td[2]/i: %s ...' % ascii_event_name_string)
        
        event_fight_card_url_array = tree.xpath('//*[@id="mw-content-text"]/div[1]/table[1]/tbody/tr[%i]/td[1]/i/a/@href'%(x))
        new_fight_card_url_str = ''.join(event_fight_card_url_array)
        ascii_fight_card_url_string = smart_str(new_fight_card_url_str)
        print('Event URL: \t\t %s' % ascii_fight_card_url_string)
        
        if ascii_event_name_string == '' and not event_name_array: # Check if event_name_array is empty
          print('Trying the scenario //*[@id="mw-content-text"]/div[1]/table[1]/tbody/tr[%i]/td[1]/i/text()' % x)
          event_name_array = tree.xpath('//*[@id="mw-content-text"]/div[1]/table[1]/tbody/tr[%i]/td[1]/i/text()' % x)
          new_event_name_str = ''.join(event_name_array)
          ascii_event_name_string = smart_str(new_event_name_str)
          print('event td[1]/i: %s ...' % ascii_event_name_string)
        
          if ascii_event_name_string == '': # Try the td 1 flavor
            print('Since I was not able to find td2 ital, I am going to try td1')
            event_name_array = tree.xpath('//*[@id="mw-content-text"]/div[1]/table[1]/tbody/tr[%i]/td[1]/a/text()'%(x))
            new_event_name_str = ''.join(event_name_array)
            ascii_event_name_string = smart_str(new_event_name_str)
            print('event td[1]: %s ...' % ascii_event_name_string)
            
            event_fight_card_url_array = tree.xpath('//*[@id="mw-content-text"]/div[1]/table[1]/tbody/tr[%i]/td[1]/a/@href'%(x))
            new_fight_card_url_str = ''.join(event_fight_card_url_array)
            ascii_fight_card_url_string = smart_str(new_fight_card_url_str)
            print('Event URL: \t\t %s' % ascii_fight_card_url_string)
            
            if ascii_event_name_string == '': # Try the td 1 flavor with italic
              print('this is my last attempt - I am now trying another field - italicized td1')
              event_name_array = tree.xpath('//*[@id="mw-content-text"]/div[1]/table[1]/tbody/tr[%i]/td[1]/i/a/text()'%(x))
              new_event_name_str = ''.join(event_name_array)
              ascii_event_name_string = smart_str(new_event_name_str)
              print('event td[1]/i: %s ...' % ascii_event_name_string)
                
              event_fight_card_url_array = tree.xpath('//*[@id="mw-content-text"]/div[1]/table[1]/tbody/tr[%i]/td[1]/i/a/@href'%(x))
              new_fight_card_url_str = ''.join(event_fight_card_url_array)
              ascii_fight_card_url_string = smart_str(new_fight_card_url_str)
              print('Event URL: \t\t %s' % ascii_fight_card_url_string)
                
              print('I am appending the event Name in the Block that means I found it in td1 italicized')
              event_name.append(ascii_event_name_string)
              ev_fc_wbst = 'http://en.wikipedia.org', ''.join(ascii_fight_card_url_string)
              event_fight_card_url.append(ev_fc_wbst)
            else:
              print('I am appending the event Name in the Else Block that means I found it in td1')
              event_name.append(ascii_event_name_string)
              ev_fc_wbst = 'http://en.wikipedia.org', ''.join(ascii_fight_card_url_string)
              event_fight_card_url.append(ev_fc_wbst)
          else:
            print('I am appending the event Name in the Else Block that means I found it in td2 italicized') 
            event_name.append(ascii_event_name_string)
            ev_fc_wbst = 'http://en.wikipedia.org', ''.join(ascii_fight_card_url_string)
            event_fight_card_url.append(ev_fc_wbst)
        else:
          print('I am appending the event Name in the Else Block that means I found it in td2')
          event_name.append(ascii_event_name_string)
          ev_fc_wbst = 'http://en.wikipedia.org', ''.join(ascii_fight_card_url_string)
          event_fight_card_url.append(ev_fc_wbst)
        #######################################################################
        event_date_array = tree.xpath('//*[@id="mw-content-text"]/div[1]/table[1]/tbody/tr[%i]/td[3]/span/text()'%(x))
        new_event_date = ''.join(event_date_array)
        ascii_event_date = smart_str(new_event_date)

        if ascii_event_date == '':
          event_date_array = tree.xpath('//*[@id="mw-content-text"]/div[1]/table[1]/tbody/tr[%i]/td[2]/span/text()'%(x))
          new_event_date = ''.join(event_date_array)
          ascii_event_date = smart_str(new_event_date)
          event_date.append(ascii_event_date)
        else:                      
          event_date.append(ascii_event_date)
          print('Event Date: \t', ascii_event_date)
     
    return row_len-33;

def insertRows (row_len, prev_row_ptr, array_pos):
    # set the array position
    array_pos = array_pos + prev_row_ptr
    event_id = prev_row_ptr + row_len
    event_id = event_id - 4
    

    # loop through all the rows
    for loopid in range (1,row_len-1):
      # print('***********************************************************************************************')
      db_e_en = ''.join(event_name[array_pos])
      db_e_fc = ''.join(event_fight_card_url[array_pos])
      db_e_fd = ''.join(event_date[array_pos])
      w_e_id = event_org + str(event_id)
      print('Adding event: %s ...' % db_e_en)
      print('Event ID: \t\t %i ' % event_id)
      print('Event Org: \t\t %s' % event_org)
      print('Event Date: \t', db_e_fd)
      print('Event URL: \t\t %s' % db_e_fc)
      print('Event Unique ID: \t ', w_e_id)
      print('***********************************************************************************************')
      #setting event_date1 so we can compare
      if db_e_en == "Bellator 3":
        db_e_fd = "April 17, 2009"
        event_date1 = "April 17, 2009"
      else: 
        event_date1 = db_e_fd
      
      if db_e_en == "":
        return;

      event_date_str = event_date1
      today_date = datetime.now()
      event_date_compare = datetime.strptime(event_date_str, "%B %d, %Y")
      if event_date_compare > today_date:
          db_ep = False
          db_ep_int = int(db_ep)
      else:
          db_ep = True
          db_ep_int = int(db_ep)
          
      # Check if the row already exists in the table
      query_select = "SELECT wiki_event_id FROM wiki_mma_events WHERE wiki_event_id = %s"
      cur.execute(query_select, (w_e_id,))
      existing_row = cur.fetchone()
      
      if existing_row:
          # Update the existing row
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
          values_update = (db_e_en, event_id, db_e_fc, event_org, db_e_fd, db_ep_int, w_e_id)
          cur.execute(query_update, values_update)
      else:
          # Insert a new row
          query_insert = """
              INSERT INTO wiki_mma_events (event_name, event_id, event_fight_card_url, event_org, event_date, wiki_event_id, event_past)
              VALUES (%s, %s, %s, %s, %s, %s, %s)
          """
          values_insert = (db_e_en, event_id, db_e_fc, event_org, db_e_fd, w_e_id, db_ep_int)
          cur.execute(query_insert, values_insert)
      print('Success!...')
      print('***********************************************************************************************')
      array_pos = (array_pos) + 1
      event_id = event_id - 1
      
      

    prev_row_ptr = prev_row_ptr + row_len
    print("the prev row ptr is")
    print(str(prev_row_ptr))


    return;

# Do the Event Organization and writing to files
def countPastEvents(row_len, prev_row_ptr, array_pos):
    bellator_te = 0
    bellator_pe = 0
    bellator_se = 0

    array_pos = array_pos + prev_row_ptr

    for loopid in range(1, row_len - 2):
        db_e_en = ''.join(event_name[array_pos])
        db_e_fc = ''.join(event_fight_card_url[array_pos])
        db_e_fd = ''.join(event_date[array_pos])

        if not db_e_fd:  # Check if the date string is empty
            # print("Empty date string found. Skipping event.")
            array_pos += 1
            continue

        try:
            d1 = datetime.strptime(db_e_fd, '%B %d, %Y').strftime("%d/%m/%Y")
        except ValueError as e:
            # print(f"Error parsing date: {db_e_fd}. Skipping event. Error: {e}")
            array_pos += 1
            continue

        current_time = datetime.now()
        month_formatted = datetime.strptime(str(current_time.month), "%m").strftime("%m")
        
        cd1 = "%s/%s/%s" % (current_time.day, month_formatted, current_time.year)
        
        event_date1_breakdown = d1.split("/")
        event_date1_breakdown_day, event_date1_breakdown_month, event_date1_breakdown_year = map(int, event_date1_breakdown)

        compare_date_1 = date(event_date1_breakdown_year, event_date1_breakdown_month, event_date1_breakdown_day)
        compare_date_today = date(current_time.year, int(month_formatted), current_time.day)

        if compare_date_today > compare_date_1:
            bellator_pe += 1
        else:
            if compare_date_today.month > compare_date_1.month:
                bellator_pe += 1
            else:
                if compare_date_today.month < compare_date_1.month:
                    bellator_se += 1
                else:
                    if compare_date_today.day > compare_date_1.day:
                        bellator_pe += 1
                    else:
                        bellator_se += 1

        bellator_te += 1
        array_pos += 1

    prev_row_ptr += row_len
    print("Total Events is %i, Past events is %i, and Scheduled events is %i" % (bellator_te, bellator_pe, bellator_se))

    # Creating the Files for autonomous runs *****
    pe_string = "BELLATOR_PAST_EVENTS = %i" % bellator_pe
    past_events = [pe_string]

    outF_pe = open("python/bellator_pastevents.py", "w")
    for line in past_events:
        print(line, file=outF_pe)
    outF_pe.close()

    se_string = "BELLATOR_SCHED_EVENTS = %i" % bellator_se
    sched_events = [se_string]

    outF_se = open("python/bellator_schedevents.py", "w")
    for line in sched_events:
        print(line, file=outF_se)
    outF_se.close()

    te_string = "BELLATOR_TOTAL_EVENTS = %i" % bellator_te
    total_events = [te_string]

    outF_te = open("python/bellator_totalevents.py", "w")
    for line in total_events:
        print(line, file=outF_te)
    outF_te.close()

    return

""" def countScheduledEvents (row_len, prev_row_ptr, array_pos):
    # set the array position
    array_pos = array_pos + prev_row_ptr
    
    # loop through all the rows
    for loopid in range (3,row_len-22):
      print('***********************************************************************************************')
      db_e_en = ''.join(event_name[array_pos])
      db_e_fc = ''.join(event_fight_card_url[array_pos])
      db_e_fd = ''.join(event_date[array_pos])
      print('Event Name: %s ...' % db_e_en)
      print('Event Org: \t\t %s' % event_org)
      print('Event Date: \t', db_e_fd)
      print('***********************************************************************************************')
      print('Check the dates for past and scheduled events')
      #setting event_date1 so we can compare
      if db_e_en == "Bellator 3":
        event_date1 = "April 17, 2009"
      else: 
        event_date1 = db_e_fd
      
      if db_e_en == "":
        return;
      #getting current time
      current_time = datetime.now()
      print('The attributes of now() are: ')
      print ("Year : ", end = "")
      print (current_time.year) 
      print ("Month : ", end = "")
      print (current_time.month)
      print ("Day : ", end = "") 
      print (current_time.day)
      d1 = datetime.strptime(event_date1, '%B %d, %Y').strftime("%d/%m/%Y")
      month_formatted = datetime.strptime(str(current_time.month), "%m").strftime("%m")
      print("This is event_date_1 ", d1)
      print("this is today date %s/%s/%s"%(current_time.day,current_time.month,current_time.year))
      print("This is the month formatted", month_formatted )
      print("this is today date %s/%s/%s"%(current_time.day,month_formatted,current_time.year))
      #LOGIC FOR Seeing if a date is is in the Past or Upcoming.
      event_date1_breakdown = d1.split("/")
      event_date1_breakdown_day = event_date1_breakdown[0]
      event_date1_breakdown_month = event_date1_breakdown[1]
      event_date1_breakdown_year = event_date1_breakdown[2]
      compare_date_1 = date(int(event_date1_breakdown_year), int(event_date1_breakdown_month), int(event_date1_breakdown_day))
      compare_date_today = date(current_time.year, int(month_formatted), current_time.day)
      print(event_date1_breakdown_day, event_date1_breakdown_month, event_date1_breakdown_year)
      # Comparing the dates will return
      # either True or False
      try:
        if compare_date_1 > compare_date_today is True:
            bellator_se_num =+ 1
            print(bellator_se_num)
        else:
            bellator_pe_num =+ 1
            print(bellator_pe_num)
      except:
            bellator_pe_num =+ 1
            print(bellator_pe_num)
      bellator_te_num =+ 1
      print(bellator_te_num)
    prev_row_ptr = prev_row_ptr + row_len
    # Creating the Files for autonomous runs *****
    pe_string = "BELLATOR_PAST_EVENTS = %i" %(bellator_pe_num)
    past_events = [pe_string]
 
    outF_pe = open("python/bellator_pastevents.py", "w")

    for line in past_events:
      print(line, file=outF_pe)
      #print >>outF_pe, line
    outF_pe.close()

    se_string = "BELLATOR_SCHED_EVENTS = %i" %(bellator_se_num)
    sched_events = [se_string]

    outF_se = open("python/bellator_schedevents.py", "w")

    for line in sched_events:
      print(line, file=outF_se)
      #print >>outF_se, line
    outF_se.close()

    print("The SE NUM = %i" %(bellator_se_num))
    print("The PE NUM = %i" %(bellator_pe_num))
    te_string = "BELLATOR_TOTAL_EVENTS = %i" %(bellator_te_num)
    total_events = [te_string]
    print("The TE num = %i" %(bellator_te_num))
    outF_te = open("python/bellator_totalevents.py", "w")

    for line in total_events:
      print(line, file=outF_te)
      # print >>outF_te, line
    outF_te.close()


    return;

def countTotalEvents (row_len, prev_row_ptr, array_pos):
    # set the array position
    array_pos = array_pos + prev_row_ptr
    
    # loop through all the rows
    for loopid in range (3,row_len-22):
      print('***********************************************************************************************')
      db_e_en = ''.join(event_name[array_pos])
      db_e_fc = ''.join(event_fight_card_url[array_pos])
      db_e_fd = ''.join(event_date[array_pos])
      print('Event Name: %s ...' % db_e_en)
      print('Event Org: \t\t %s' % event_org)
      print('Event Date: \t', db_e_fd)
      print('***********************************************************************************************')
      print('Check the dates for past and scheduled events')
      #setting event_date1 so we can compare
      if db_e_en == "Bellator 3":
        event_date1 = "April 17, 2009"
      else: 
        event_date1 = db_e_fd
      
      if db_e_en == "":
        return;
      #getting current time
      current_time = datetime.now()
      print('The attributes of now() are: ')
      print ("Year : ", end = "")
      print (current_time.year) 
      print ("Month : ", end = "")
      print (current_time.month)
      print ("Day : ", end = "") 
      print (current_time.day)
      d1 = datetime.strptime(event_date1, '%B %d, %Y').strftime("%d/%m/%Y")
      month_formatted = datetime.strptime(str(current_time.month), "%m").strftime("%m")
      print("This is event_date_1 ", d1)
      print("this is today date %s/%s/%s"%(current_time.day,current_time.month,current_time.year))
      print("This is the month formatted", month_formatted )
      print("this is today date %s/%s/%s"%(current_time.day,month_formatted,current_time.year))
      #LOGIC FOR Seeing if a date is is in the Past or Upcoming.
      event_date1_breakdown = d1.split("/")
      event_date1_breakdown_day = event_date1_breakdown[0]
      event_date1_breakdown_month = event_date1_breakdown[1]
      event_date1_breakdown_year = event_date1_breakdown[2]
      compare_date_1 = date(int(event_date1_breakdown_year), int(event_date1_breakdown_month), int(event_date1_breakdown_day))
      compare_date_today = date(current_time.year, int(month_formatted), current_time.day)
      print(event_date1_breakdown_day, event_date1_breakdown_month, event_date1_breakdown_year)
      # Comparing the dates will return
      # either True or False
      try:
        if compare_date_1 > compare_date_today is True:
            bellator_se_num =+ 1
            print(bellator_se_num)
        else:
            bellator_pe_num =+ 1
            print(bellator_pe_num)
      except:
            bellator_pe_num =+ 1
            print(bellator_pe_num)
      bellator_te_num =+ 1
      print(bellator_te_num)
    prev_row_ptr = prev_row_ptr + row_len
    # Creating the Files for autonomous runs *****
    pe_string = "BELLATOR_PAST_EVENTS = %i" %(bellator_pe_num)
    past_events = [pe_string]
 
    outF_pe = open("python/bellator_pastevents.py", "w")

    for line in past_events:
      print(line, file=outF_pe)
      #print >>outF_pe, line
    outF_pe.close()

    se_string = "BELLATOR_SCHED_EVENTS = %i" %(bellator_se_num)
    sched_events = [se_string]

    outF_se = open("python/bellator_schedevents.py", "w")

    for line in sched_events:
      print(line, file=outF_se)
      #print >>outF_se, line
    outF_se.close()

    print("The SE NUM = %i" %(bellator_se_num))
    print("The PE NUM = %i" %(bellator_pe_num))
    te_string = "BELLATOR_TOTAL_EVENTS = %i" %(bellator_te_num)
    total_events = [te_string]
    print("The TE num = %i" %(bellator_te_num))
    outF_te = open("python/bellator_totalevents.py", "w")

    for line in total_events:
      print(line, file=outF_te)
      # print >>outF_te, line
    outF_te.close()


    return; """
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
#cur.execute("TRUNCATE wiki_mma_events")
# Scrape UFC Information
# initialize our arrays. our Arrays.
event_name = []
event_fight_card_url = []
event_date = []

prev_row_ptr = 0
array_pos = 0

new_prev_ptr = 0
new_array_pos = 0

# print("********************************************************")
# print("* List of Bellator Events Wikipedia Page URL Scrape... *")
# print("********************************************************")
# set the event organization & url, reset event ID
event_org = 'Bellator'
event_url = 'https://en.wikipedia.org/wiki/List_of_Bellator_MMA_events'
event_id = 0
# print("****************** ---- Inserts ---- *******************")
bellator_row_len = loadEventsData(event_url, event_org)
bellator_countEvents_row_len = bellator_row_len
insertRows(bellator_row_len, prev_row_ptr, array_pos)
countPastEvents(bellator_countEvents_row_len, new_prev_ptr, new_array_pos)
#countScheduledEvents(bellator_countEvents_row_len,0,0)
#countTotalEvents(bellator_countEvents_row_len,0,0)
# set the prev_row_ptr
prev_row_ptr = bellator_row_len + prev_row_ptr - 1
cur.close()
db.close()
