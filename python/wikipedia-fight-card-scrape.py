##################
# FILE HAS BEEN TESTED SUCCESSFULLY
#

from lxml import html, etree
import io
from django.utils.encoding import smart_str, smart_text
from pyquery import PyQuery as pq
import requests
import MySQLdb
import time


def scrapeEvent(event_url, event_org):
    # set up the lxml, load url to scrape
    page = requests.get('%s' % (event_url))
    tree = html.fromstring(page.content)

    # set up PyQuery section, load the url to scrape
    d = pq("<html></html>")
    d = pq(etree.fromstring("<html></html>"))
    d = pq(url='%s' % (event_url))

    # get the row length by querying the event table on table rows
    p = d("#mw-content-text table tr")

    # set the row length
    row_len = len(p)

    return;


# Database Connection
db = MySQLdb.connect(host="markpereira.com",  # your host, usually localhost
                     user="mark5463_ft_test",  # your username
                     passwd="fttesting",  # your password
                     db="mark5463_ft_prod", 
                     charset="utf8")  # name of the data base

#  you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()

# This section will query the database and return all data in the table
cur.execute("SELECT * FROM wiki_mma_events_poster")

# initialize the arrays
g_event_name = []
g_event_id = []
g_event_fight_card_url = []
g_event_date = []
g_event_fight_poster_url = []
g_event_org = []



# load our arrays with all of our event data.
for row in cur.fetchall():
    g_event_fight_poster_url.append(row[0])
    g_event_id.append(row[1])
    g_event_fight_card_url.append(row[2])
    g_event_name.append(row[3])
    g_event_date.append(row[4])
    g_event_org.append(row[5])
    print('***********************************************************************************************')
    print('Loading event Name: \t\t\t %s ...' % row[3])
    print('Loading event Poster URL: \t\t\t %s ...' % row[0])
    print('Loading event ID: \t\t %s ' % row[1])
    print('Loading event Org: \t\t %s' % row[5])
    print('Loading event Date: \t\t', row[4])
    print('Loading event URL: \t\t %s' % row[2])
    print('***********************************************************************************************')

# set up the fighter arrays
g_fighter_one = []
g_fighter_two = []
g_fighter_one_url = []
g_fighter_two_url = []
g_fight_card_org = []
# fight card specific arrays
g_fight_card_event_name = []
g_fight_card_event_url = []

x_range = len(g_event_name)

# This loops for every entry of event in the database to build our fight card information
for x in range(0, x_range - 1):  # prev 0, 533
    # bring in the url information
    event_main_event_url = g_event_fight_card_url[x]
    page = requests.get('%s' % (event_main_event_url))
    tree = html.fromstring(page.content)

    this_event_name = g_event_name[x]
    this_event_org = g_event_org[x]

    g_fight_card_event_name.append(this_event_name)
    g_fight_card_event_url.append(event_main_event_url)
    g_fight_card_org.append(this_event_org)

    # time.sleep(5)
    # debug info
    #print("this is the main event url")
    #print(event_main_event_url)
    #print("---------------------")

    d = pq("<html></html>")
    d = pq(etree.fromstring("<html></html>"))
    d = pq(url='%s' % (event_main_event_url))
    # --get the row length by querying the event table on table rows
    p = d("#mw-content-text table tr")
    # p = d(".content table tr")
    # --set the row length
    # row_len = len(p)
    row_len = 15

    # debug info
    #print("this is the row length:")
    #print(row_len)
    #print("---------------------")

    # set up the array
    # scrape main event event name
    main_event_fighter_one_array = tree.xpath('//*[@id="mw-content-text"]/div/table[2]/tbody/tr[2]/td[2]/a/text()')

    newstr = ''.join(main_event_fighter_one_array)
    asccii_string = smart_str(newstr)

    # debug info
    #print("fighter one name:")
    #print(asccii_string)
    #print("---------------------")

    g_fighter_one.append(asccii_string)

    main_event_fighter_one_url_array = tree.xpath('//*[@id="mw-content-text"]/div/table[2]/tbody/tr[2]/td[2]/a/@href')

    me_fgtr1_wbst = 'https://en.wikipedia.org', ''.join(main_event_fighter_one_url_array)

    # debug info
    #print("fighter one website: ")
    #print(me_fgtr1_wbst)
    #print("---------------------")
    g_fighter_one_url.append(me_fgtr1_wbst)

    main_event_fighter_two_array = tree.xpath('//*[@id="mw-content-text"]/div/table[2]/tbody/tr[2]/td[4]/a/text()')

    newstr2 = ''.join(main_event_fighter_two_array)
    asccii_string2 = smart_str(newstr2)

    # debug info
    #print("fighter 2 name: ")
    #print(asccii_string2)
    #print("---------------------")

    g_fighter_two.append(asccii_string2)

    main_event_fighter_two_url_array = tree.xpath('//*[@id="mw-content-text"]/div/table[2]/tbody/tr[2]/td[4]/a/@href')

    me_fgtr2_wbst = 'https://en.wikipedia.org', ''.join(main_event_fighter_two_url_array)

    # debug info
    print('***********************************************************************************************')
    print("Event Name: ", this_event_name)
    print("MAIN EVENT fighter one name: ", asccii_string, "\tfighter two name: \t", asccii_string2)
    print("fighter 1 website", me_fgtr1_wbst, "fighter 2 website", me_fgtr2_wbst)
    print("Event URL: ", event_main_event_url)
    print("This is the fighter org", this_event_org)
    #print("fighter 2 website:")
    #print(me_fgtr2_wbst)
    #print("---------------------")

    g_fighter_two_url.append(me_fgtr2_wbst)
    ###### WORKING ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    for z in range(2, row_len):
        # print("Z is = to: ")
        # print(z)
        # scrape fighter one name
        fighter_one_array = tree.xpath('//*[@id="mw-content-text"]/div/table[2]/tbody/tr[%i]/td[2]/a/text()' % (z))
        newstr3 = ''.join(fighter_one_array)
        asccii_string3 = smart_str(newstr3)
        g_fighter_one.append(asccii_string3)
        # scrape fighter one URL
        fighter_one_url_array = tree.xpath('//*[@id="mw-content-text"]/div/table[2]/tbody/tr[%i]/td[2]/a/@href' % (z))
        fgtr1_wbst = 'https://en.wikipedia.org', ''.join(fighter_one_url_array)
        g_fighter_one_url.append(fgtr1_wbst)
        # scrape fighter two name
        fighter_two_array = tree.xpath('//*[@id="mw-content-text"]/div/table[2]/tbody/tr[%i]/td[4]/a/text()' % (z))
        newstr4 = ''.join(fighter_two_array)
        asccii_string4 = smart_str(newstr4)
        g_fighter_two.append(asccii_string4)
        # scrape fighter two URL
        fighter_two_url_array = tree.xpath('//*[@id="mw-content-text"]/div/table[2]/tbody/tr[%i]/td[4]/a/@href' % (z))
        fgtr2_wbst = 'https://en.wikipedia.org', ''.join(fighter_two_url_array)
        g_fighter_two_url.append(fgtr2_wbst)

        print("Fight ", z, "\tfighter one: ", asccii_string3, "\tfighter two: \t", asccii_string4)
        print("fighter 1 website", fgtr1_wbst, "fighter 2 website", fgtr2_wbst)
        print('***********************************************************************************************')
        # print("This is the fighter org", this_event_org)
        g_fight_card_event_name.append(this_event_name)
        g_fight_card_event_url.append(event_main_event_url)
        g_fight_card_org.append(this_event_org)




fighterloop = len(g_fighter_one)

# print "the length of fighter array is also"
# print "the fighter loop variable:"
# print fighterloop

db = MySQLdb.connect(host="markpereira.com",  # your host, usually localhost
                     user="mark5463_ft_test",  # your username
                     passwd="fttesting",  # your password
                     db="mark5463_ft_prod",
                     charset="utf8")  # name of the data base

#  you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()

# This section will delete the information on the table, for a clean run.
cur.execute("TRUNCATE wiki_mma_fight_cards")

for y in range(0, fighterloop - 1):
    print('***********************************************************************************************')
    e_name = ''.join(g_fight_card_event_name[y])
    e_f1 = ''.join(g_fighter_one[y])
    e_f1_url = ''.join(g_fighter_one_url[y])
    e_f2 = ''.join(g_fighter_two[y])
    e_f2_url = ''.join(g_fighter_two_url[y])
    e_fc_url = ''.join(g_fight_card_event_url[y])
    e_org = ''.join(g_fight_card_org[y])
    print('Adding event: %s ...' % e_name)
    print('Fighter One: \t\t %s ' % e_f1)
    print('Fighter One URL: \t\t %s' % e_f1_url)
    print('Fighter Two: \t\t %s ' % e_f2)
    print('Fighter Two URL: \t\t %s' % e_f2_url)
    print('Event URL: \t\t %s' % e_fc_url)
    print('Event Org: \t\t %s' % e_org)
    print('***********************************************************************************************')
    # print('Query ...')
    query = "INSERT INTO wiki_mma_fight_cards (event_name, fighter_one, fighter_one_url, fighter_two, fighter_two_url, event_url, event_org) VALUES (\"%s\",\"%s\",\"%s\",\"%s\",\"%s\", \"%s\", \"%s\")" % (e_name, e_f1, e_f1_url, e_f2, e_f2_url, e_fc_url, e_org)
    # print (query) #only necessary for debugging
    ## Query not needed after first load
    print('Query Executed...')
    cur.execute(query)
    print('Success!...')
    print('***********************************************************************************************')
