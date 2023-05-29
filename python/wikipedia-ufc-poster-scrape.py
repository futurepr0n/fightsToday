##################
# FILE HAS BEEN TESTED SUCCESSFULLY
# updated for prod db
#

from lxml import html, etree
import io
import time
from django.utils.encoding import smart_str, smart_text
from pyquery import PyQuery as pq
import requests
import MySQLdb


##### The JQuery for "The Ultimate Fighter" Posters is:

#mw-content-text > table:nth-child(52) > tbody > tr:nth-child(2) > td

def loadPosterData (event_url):
    #set up the lxml, load url to scrape
    page = requests.get('%s'%(event_url))
    tree = html.fromstring(page.content)

    #set up PyQuery section, load the url to scrape
    d = pq("<html></html>")
    d = pq(etree.fromstring("<html></html>"))
    d = pq(url='%s'%(event_url))

    poster_url_array = tree.xpath('//*[@id="mw-content-text"]/div/table[1]/tbody/tr[2]/td/a/img/@src')

    # If the poster is not found, we might want to try this xpath: //*[@id="mw-content-text"]/table[5]/tr[2]/td/a/img


    ev_fc_poster_wbst = str(poster_url_array).strip('[\'\']')
    newstr = ev_fc_poster_wbst
    ev_fp_wbst = "https:%s"%(newstr)

    return ev_fp_wbst;

def insertRows (poster_url, event_id, event_fight_card_url, event_date, event_name, event_org):
    print('+++++++++++++++++++++++++++++')
    db_e_poster_url = ''.join(poster_url)
    w_e_p_i = event_org + str(event_id)
    print('Adding poster URL to the Database: ', db_e_poster_url)
    print('+++++++++++++++++++++++++++++')
    print('+++++++++++++++++++++++++++++')
    query = """
    INSERT INTO wiki_mma_events_poster
    (event_fight_poster_url, event_id, event_fight_card_url, event_date, event_name, event_org, wiki_event_poster_id)
    VALUES
    (%s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
    event_fight_poster_url = VALUES(event_fight_poster_url),
    event_fight_card_url = VALUES(event_fight_card_url),
    event_date = VALUES(event_date),
    event_name = VALUES(event_name),
    event_org = VALUES(event_org)
    """

    values = (db_e_poster_url, event_id, event_fight_card_url, event_date, event_name, event_org, w_e_p_i)

    cur.execute(query, values)

    return;

# Database Connection
#db = MySQLdb.connect(host="markpereira.com", # your host, usually localhost
#                     user="mark5463_ft_test", # your username
#                      passwd="fttesting", # your password
#                      db="mark5463_ft_prod") # name of the data base

# db = MySQLdb.connect(host="dev-mysql.markpereira.com", user="root", passwd="fttesting", db="mark5463_ft_prod", charset="utf8")
# local docker mysql
#db = MySQLdb.connect(host="192.168.1.96", user="root", passwd="fttesting", port=3308, db="mark5463_ft_prod", charset="utf8")

#prodlike mysql
db = MySQLdb.connect(host="markpereira.com",  user="mark5463_ft_test", passwd="fttesting", db="mark5463_ft_prod",charset="utf8") 


# Cursor object. It will let you execute the queries
cur = db.cursor()

# This section will delete the information on the table, for a clean run.
#cur.execute("TRUNCATE wiki_mma_events_poster ")

# This section will query the database and return all data in the table
cur.execute("SELECT event_name, event_id, event_fight_card_url, event_org, event_date FROM wiki_mma_events where event_org = 'UFC' ORDER BY event_id ASC")

# initialize the arrays
g_event_name = []
g_event_id = []
g_event_fight_card_url = []
g_event_org = []
g_event_date = []

#fight poster specific arrays
#fight_card_poster = []
g_fight_card_poster_url = []
g_fight_card_org = []

# load our arrays with all of our event data.
for row in cur.fetchall() :
    g_event_name.append(row[0])
    g_event_id.append(row[1])
    g_event_fight_card_url.append(row[2])
    g_event_org.append(row[3])
    g_event_date.append(row[4])
    print('***********************************************************************************************')
    print('Loading event Name: \t\t\t %s ...' % row[0])
    print('Loading event ID: \t\t %s ' % row[1])
    print('Loading event Org: \t\t %s' % row[3])
    print('Loading event Date: \t\t', row[4])
    print('Loading event URL: \t\t %s' % row[2])
    print('***********************************************************************************************')


x_range = len(g_event_name)

# This loops for every entry of event in the database to build our fight card information
for x in range(0, x_range):  # prev 0, 533
  #bring in the url information
  wiki_url = g_event_fight_card_url[x]
  this_event_poster = loadPosterData(wiki_url)
  #fight_card_event_name.append(this_event_name)
  g_fight_card_poster_url.append(this_event_poster)
  insertRows(this_event_poster, x + 1, g_event_fight_card_url[x], g_event_date[x], g_event_name[x], g_event_org[x])

  # time.sleep(5)

'''
# Scrape UFC Information
# initialize our arrays. our Arrays.

# event_month = []
# event_day = []
# event_year = []
# event_location = []

# event_location= []
prev_row_ptr = 0
array_pos = 0

print "*********************************************"
print "List of UFC Events Wikipedia Page URL Scrape..."
print "*********************************************"
# set the event organization to UFC
event_org = 'UFC'
# set the event url to sherdog ufc section
event_url = 'https://en.wikipedia.org/wiki/UFC_1'
#reset the event id
event_id = 0

poster_url = loadPosterData(event_url, event_org)
print " ---- Inserts ----"
print "------------------"
insertRows(poster_url)


'''
