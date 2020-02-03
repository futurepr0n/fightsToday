##################
# FILE HAS BEEN TESTED SUCCESSFULLY
# this file is ready for prod
#

from lxml import html, etree
import io
from django.utils.encoding import smart_str, smart_text
from pyquery import PyQuery as pq
import requests
import MySQLdb

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

    # JQUERY STUFF --  THIS will calculate the rows for Upcoming Events (Scheduled Events)
    # $("#Scheduled_events tr").length

    # THIS will query against the table for Past Event Info
    # $("table:nth-child(16) tr").length

    #set the row length
    row_len = len(p)

    #run through every row in the table
    for x in range (2, row_len+1):

      event_name_array = tree.xpath('//*[@id="mw-content-text"]/div/table/tbody/tr[%i]/td[2]/a/text()'%(x))
      newstr = ''.join(event_name_array)
      asccii_string = smart_str(newstr)

      if asccii_string == '':
        event_name_array = tree.xpath('//*[@id="mw-content-text"]/div/table/tbody/tr[%i]/td[2]/i/a/text()'%(x))
        newstr = ''.join(event_name_array)
        asccii_string = smart_str(newstr)
        event_name.append(asccii_string)
      else:
        event_name.append(asccii_string)

      # scrape wikipedia ufc fight card url
      event_fight_card_url_array = tree.xpath('//*[@id="mw-content-text"]/div/table/tbody/tr[%i]/td[2]/a/@href'%(x))
      newstr2 = ''.join(event_fight_card_url_array)
      asccii_string2 = smart_str(newstr2)

      if asccii_string2 == '':
        event_fight_card_url_array = tree.xpath('//*[@id="mw-content-text"]/div/table/tbody/tr[%i]/td[2]/i/a/@href'%(x))
        newstr2 = ''.join(event_fight_card_url_array)
        asccii_string2 = smart_str(newstr2)
        ev_fc_wbst = 'http://en.wikipedia.org', ''.join(asccii_string2)
        event_fight_card_url.append(ev_fc_wbst)
      else:
        ev_fc_wbst = 'http://en.wikipedia.org', ''.join(asccii_string2)
        event_fight_card_url.append(ev_fc_wbst)

      event_date_array = tree.xpath('//*[@id="mw-content-text"]/div/table/tbody/tr[%i]/td[3]/span/text()'%(x))
      event_date.append(event_date_array)


    return row_len;

def insertRows (row_len, prev_row_ptr, array_pos):
    # set the array position
    array_pos = array_pos + prev_row_ptr
    event_id = prev_row_ptr + row_len
    event_id = event_id - 1

    # loop through all the rows
    for loopid in range (2,row_len-22):
      print('***********************************************************************************************')
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
      query = "INSERT INTO wiki_mma_events (event_name, event_id, event_fight_card_url, event_org, event_date, wiki_event_id) VALUES (\"%s\",%i,\"%s\",\"%s\",\"%s\",\"%s\")" % (db_e_en, event_id - 22, db_e_fc, event_org, db_e_fd, w_e_id)
      print (query)
      print('***********************************************************************************************')
      print('Query Executed...')
      cur.execute(query)
      print('Success!...')
      print('***********************************************************************************************')
      array_pos = (array_pos) + 1
      event_id = event_id - 1
    prev_row_ptr = prev_row_ptr + row_len

    return;

# Database Connection
db = MySQLdb.connect(host="markpereira.com", user="mark5463_ft_test", passwd="fttesting", db="mark5463_ft_prod")

# Cursor object. It will let you execute the queries
cur = db.cursor()
cur.execute("TRUNCATE wiki_mma_events")
# Scrape UFC Information
# initialize our arrays. our Arrays.
event_name = []
event_fight_card_url = []
event_date = []

prev_row_ptr = 0
array_pos = 0

print("********************************************************")
print("* List of Bellator Events Wikipedia Page URL Scrape... *")
print("********************************************************")
# set the event organization & url, reset event ID
event_org = 'Bellator'
event_url = 'https://en.wikipedia.org/wiki/List_of_Bellator_MMA_events'
event_id = 0
print("****************** ---- Inserts ---- *******************")
bellator_row_len = loadEventsData(event_url, event_org)
insertRows(bellator_row_len, prev_row_ptr, array_pos)

# set the prev_row_ptr
prev_row_ptr = bellator_row_len + prev_row_ptr - 1