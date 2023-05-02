##################
# FILE HAS BEEN TESTED SUCCESSFULLY
# this file is ready for prod
#

from lxml import html, etree
import io
import time
from django.utils.encoding import smart_str, smart_text
from pyquery import PyQuery as pq
import requests
import MySQLdb

pe_num = 0
se_num = 0
te_num = 0 


def loadPastEventsData (event_url, event_org):
    #set up the lxml, load url to scrape
    page = requests.get('%s'%(event_url))
    tree = html.fromstring(page.content)

    #set up PyQuery section, load the url to scrape
    d = pq("<html></html>")
    d = pq(etree.fromstring("<html></html>"))
    d = pq(url='%s'%(event_url))

    ### First thing I am going to try doing is query through the past events.
    ### We will get their Event Names, Event URL, Event ID

    #get the row length by querying the event table on table rows
    p = d("#Past_events tr")

    # JQUERY STUFF --  THIS will calculate the rows for Upcoming Events (Scheduled Events)
    # $("#Scheduled_events tr").length

    # THIS will query against the table for Past Event Info
    # $("table:nth-child(16) tr").length

    #set the row length
    row_len = len(p)

    # ***** Creating the Files for autonomous runs *****
    pe_num = row_len - 1
    pe_string = "PAST_EVENTS = %i" %(pe_num)
    past_events = [pe_string]
 
    outF_pe = open("python/pastevents.py", "w")

    for line in past_events:
      print(line, file=outF_pe)
      #print >>outF_pe, line
    outF_pe.close()


    #run through every row in the table
    for x in range (2, row_len+1):

      # event_name_array = tree.xpath('//*[@id="mw-content-text"]/table[2]/tr[%i]/td[2]/a/text()'%(x))
      event_name_array = tree.xpath('//*[@id="Past_events"]/tbody/tr[%i]/td[2]/a/text()'%(x))
      newstr = ''.join(event_name_array)
      asccii_string = smart_str(newstr)

      if asccii_string == '':
        #event_name_array = tree.xpath('//*[@id="Past_events"]/table[2]/tr[%i]/td[2]/span[2]/a/text()'%(x))
        event_name_array = tree.xpath('//*[@id="Past_events"]/tbody/tr[%i]/td[2]/span/a/text()'%(x))
        newstr = ''.join(event_name_array)
        asccii_string = smart_str(newstr)
        event_name.append(asccii_string)
      else:
        event_name.append(asccii_string)

      # scrape wikipedia ufc fight card url
      #event_fight_card_url_array = tree.xpath('//*[@id="Past_events"]/table[2]/tr[%i]/td[2]/span[2]/a/@href'%(x))
      event_fight_card_url_array = tree.xpath('//*[@id="Past_events"]/tbody/tr[%i]/td[2]/span/a/@href'%(x))
      newstr2 = ''.join(event_fight_card_url_array)
      asccii_string2 = smart_str(newstr2)

      if asccii_string2 == '':
        #event_fight_card_url_array = tree.xpath('//*[@id="Past_events"]/table[2]/tr[%i]/td[2]/a/@href'%(x))
        event_fight_card_url_array = tree.xpath('//*[@id="Past_events"]/tbody/tr[%i]/td[2]/a/@href'%(x))
        newstr2 = ''.join(event_fight_card_url_array)
        asccii_string2 = smart_str(newstr2)
        ev_fc_wbst = 'http://en.wikipedia.org', ''.join(asccii_string2)
        event_fight_card_url.append(ev_fc_wbst)
      else:
        ev_fc_wbst = 'http://en.wikipedia.org', ''.join(asccii_string2)
        event_fight_card_url.append(ev_fc_wbst)

      #event_date_array = tree.xpath('//*[@id="Past_events"]/table[2]/tr[%i]/td[3]/span[2]/text()'%(x))
      event_date_array = tree.xpath('//*[@id="Past_events"]/tbody/tr[%i]/td[3]/span/text()'%(x))
      event_date.append(event_date_array)
      ep_b = True
      db_ep_int = int(ep_b)
      event_past.append(db_ep_int)


    return row_len;

def loadUpcomingEventsData (event_url, event_org):
    #set up the lxml, load url to scrape
    page = requests.get('%s'%(event_url))
    tree = html.fromstring(page.content)

    #set up PyQuery section, load the url to scrape
    d = pq("<html></html>")
    d = pq(etree.fromstring("<html></html>"))
    d = pq(url='%s'%(event_url))


    ### First thing I am going to try doing is query through the past events.
    ### We will get their Event Names, Event URL, Event ID

    #get the row length by querying the event table on table rows
    p = d("#Scheduled_events tr")

    # JQUERY STUFF --  THIS will calculate the rows for Upcoming Events (Scheduled Events)
    # $("#Scheduled_events tr").length

    # THIS will query against the table for Past Event Info
    # $("table:nth-child(16) tr").length

    #set the row length
    row_len = len(p)

    # Creating the Files for autonomous runs *****")
    se_num = row_len - 1
    se_string = "SCHED_EVENTS = %i" %(se_num)
    sched_events = [se_string]

    outF_se = open("python/schedevents.py", "w")

    for line in sched_events:
      print(line, file=outF_se)
      #print >>outF_se, line
    outF_se.close()


    #run through every row in the table
    for x in range (2, row_len+1):


      event_name_array = tree.xpath('//*[@id="Scheduled_events"]/tbody/tr[%i]/td[1]/a/text()'%(x))
      newstr = ''.join(event_name_array)
      asccii_string = smart_str(newstr)

      if asccii_string == '':
        event_name_array = tree.xpath('//*[@id="Scheduled_events"]/tbody/tr[%i]/td[1]/a/span/text()'%(x))
        newstr = ''.join(event_name_array)
        asccii_string = smart_str(newstr)
        event_name.append(asccii_string)
      else:
        event_name.append(asccii_string)

      # scrape wikipedia ufc fight card url
      event_fight_card_url_array = tree.xpath('//*[@id="Scheduled_events"]/tbody/tr[%i]/td[1]/a/@href'%(x))
      newstr2 = ''.join(event_fight_card_url_array)
      asccii_string2 = smart_str(newstr2)

      #if asccii_string2 == '':
      #  event_fight_card_url_array = tree.xpath('//[@id="Scheduled_events"]/tr[%i]/td[1]/a/@href'%(x))
      #  newstr2 = ''.join(event_fight_card_url_array)
      #  asccii_string2 = smart_str(newstr2)
      ev_fc_wbst = 'http://en.wikipedia.org', ''.join(asccii_string2)
      event_fight_card_url.append(ev_fc_wbst)
      #else:
      #  ev_fc_wbst = 'http://en.wikipedia.org', ''.join(asccii_string2)
      #  event_fight_card_url.append(ev_fc_wbst)

      #event_date_array = tree.xpath('//*[@id="Scheduled_events"]/tbody/tr[%i]/td[2]/text()'%(x))
      event_date_array = tree.xpath('//*[@id="Scheduled_events"]/tbody/tr[%i]/td[2]/span/text()'%(x))
      newstr3 = ''.join(event_date_array)
      ascii_string3 = smart_str(newstr3)

      if ascii_string3 == '':
        #event_date_array = tree.xpath('//*[@id="Scheduled_events"]/tbody/tr[%i]/td[2]/span/text()'%(x))
        event_date_array = tree.xpath('//*[@id="Scheduled_events"]/tbody/tr[%i]/td[2]/text()'%(x))
        newstr3 = ''.join(event_date_array)
        ascii_string3 = smart_str(newstr3)
        event_date.append(ascii_string3)
      else:
        event_date.append(ascii_string3)
        
      ep_b = False
      db_ep_int = int(ep_b)
      event_past.append(db_ep_int)    

    return row_len;

def insertRows (row_len, prev_row_ptr, array_pos, pe_b):
    # set the array position
    array_pos = array_pos + prev_row_ptr
    # event_id = row_len - 1
    event_id = prev_row_ptr + row_len
    event_id = event_id - 1

    # loop through all the rows
    for loopid in range (0,row_len-1):
      print('***********************************************************************************************')
      # set the event id
     # print '+++++++++++++++++++++++++++++'
      db_e_en = ''.join(event_name[array_pos])
      # db_e_ev = ''.join(event_month[array_pos])
      # db_e_ed = ''.join((event_day[array_pos]))
      # db_e_ey = ''.join((event_year[array_pos]))
      db_e_fc = ''.join(event_fight_card_url[array_pos])
      # db_e_lc = ''.join(event_location[array_pos])
      db_e_fd = ''.join(event_date[array_pos])
      w_e_id = event_org + str(event_id)
      db_e_p = pe_b
      db_int_ep = int(db_e_p)
      print('Adding event: %s ...' % db_e_en)
      print('Event ID: \t\t %i ' % event_id)
      print('Event Org: \t\t %s' % event_org)
      print('Event Date: \t', db_e_fd)
      print('Event URL: \t\t %s' % db_e_fc)
      print('Event Unique ID: \t %s', w_e_id)
      print('Event in the past?:\t %s', str(db_e_pw))
      print('***********************************************************************************************')
      query = "INSERT INTO wiki_mma_events (event_name, event_id, event_fight_card_url, event_org, event_date, wiki_event_id, event_past) VALUES (\"%s\",%i,\"%s\",\"%s\",\"%s\",\"%s\",\"%i\")"%(db_e_en, event_id, db_e_fc, event_org,db_e_fd, w_e_id,db_int_ep)
      # print (query) # only need to print during debug
      print('***********************************************************************************************')
      print('Query Executing...')
      cur.execute(query)
      print('Success!...')
      print('***********************************************************************************************')
      # commenting out the query since we are loaded in the db right now
      #cur.execute(query)
      array_pos = (array_pos) + 1
      event_id = event_id - 1
    prev_row_ptr = prev_row_ptr + row_len

    return;

# Database Connection
# db = MySQLdb.connect(host="markpereira.com", user="mark5463_ft_test", passwd="fttesting", db="mark5463_ft_prod", charset="utf8")
# db = MySQLdb.connect(host="dev-mysql.markpereira.com", user="root", passwd="fttesting", db="mark5463_ft_prod", charset="utf8")
db = MySQLdb.connect(host="192.168.1.69", user="root", passwd="fttesting", port=3308, db="mark5463_ft_prod", charset="utf8")


# Cursor object. It will let you execute the queries
cur = db.cursor()

# Scrape UFC Information
# initialize our arrays. our Arrays.
event_name = []
# event_month = []
# event_day = []
# event_year = []
# event_location = []
event_fight_card_url = []
event_date = []
# event_location= []
prev_row_ptr = 0
array_pos = 0
event_past = []

print("*********************************************")
print("List of UFC Events Wikipedia Page URL Scrape...")
print("*********************************************")
# set the event organization to UFC
event_org = 'UFC'
# set the event url to sherdog ufc section
event_url = 'https://en.wikipedia.org/wiki/List_of_UFC_events'
#reset the event id
event_id = 0


ufc_row_len = loadPastEventsData(event_url, event_org)
pe2_num = ufc_row_len-1
print(" ---- Inserts ----")
insertRows(ufc_row_len, prev_row_ptr, array_pos, True)

#set the prev_row_ptrgth pointer
prev_row_ptr = ufc_row_len + prev_row_ptr - 1


ufc_row_len2 = loadUpcomingEventsData(event_url, event_org)
se2_num = ufc_row_len2-1
print(" ---- Inserts ----")
insertRows(ufc_row_len2, prev_row_ptr, array_pos, False)

# Creating the Files for autonomous runs *****

print("The SE NUM = %i" %(se2_num))
print("The PE NUM = %i" %(pe2_num))
te_num = pe2_num + se2_num
te_string = "TOTAL_EVENTS = %i" %(te_num)
total_events = [te_string]
print("The TE num = %i" %(te_num))
outF_te = open("python/totalevents.py", "w")

for line in total_events:
  print(line, file=outF_te)
  # print >>outF_te, line
outF_te.close()
