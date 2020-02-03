##################
# FILE HAS BEEN TESTED SUCCESSFULLY
# updated for prod db
#


import io
import MySQLdb
import requests
from django.utils.encoding import smart_str, smart_text
from lxml import html, etree
from pyquery import PyQuery as pq
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
    p = d(".content table tr")

    # set the row length
    row_len = len(p)

    return;


# Database Connection
db = MySQLdb.connect(host="markpereira.com",  # your host, usually localhost
                     user="mark5463_ft_test",  # your username
                     passwd="fttesting",  # your password
                     db="mark5463_ft_prod")  # name of the data base

#  you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()

# This section will query the database and return all data in the table
cur.execute("SELECT * FROM sd_mma_events")

# initialize the arrays
event_name = []
event_id = []
event_fight_card_url = []
event_org = []
event_month = []
event_day = []
event_year = []

# fight card specific arrays
fight_card_event_name = []
fight_card_event_url = []
fight_card_event_org = []
fight_card_event_id = []

# load our arrays with all of our event data.
for row in cur.fetchall():
    event_name.append(row[0])
    event_id.append(row[4])
    event_fight_card_url.append(row[5])
    event_org.append(row[6])
    event_month.append(row[1])
    event_day.append(row[2])
    event_year.append(row[3])

# set up the fighter arrays
fighter_one = []
fighter_two = []
fighter_one_url = []
fighter_two_url = []

x_range = len(event_name)

# This loops for every entry of event in the database to build our fight card information
for x in range(0, x_range - 1):  # prev 0, 533
    # bring in the url information
    event_main_event_url = event_fight_card_url[x]
    page = requests.get('%s' % (event_main_event_url))
    tree = html.fromstring(page.content)

    this_event_name = event_name[x]
    this_event_org = event_org[x]
    this_event_id = event_id[x]

    fight_card_event_name.append(this_event_name)
    fight_card_event_org.append(this_event_org)
    fight_card_event_id.append(this_event_id)
    fight_card_event_url.append(event_main_event_url)

    # time.sleep(35)
    # debug info
    # print("this is the main event url")
    # print(event_main_event_url)
    # print("---------------------")

    d = pq("<html></html>")
    d = pq(etree.fromstring("<html></html>"))
    d = pq(url='%s' % (event_main_event_url))
    # --get the row length by querying the event table on table rows
    p = d(".content table tr")
    # p = d(".content table tr")
    # --set the row length
    row_len = len(p)

    # debug info
    # print("this is the row length:")
    # print(row_len)
    # print("---------------------")

    # set up the array
    # scrape main event event name
    main_event_fighter_one_array = tree.xpath(
        '/html/body/div[2]/div[2]/div[1]/section[1]/div/div[2]/div[2]/div[1]/h3/a/span/text()')

    newstr = ''.join(main_event_fighter_one_array)
    asccii_string = smart_str(newstr)

    # debug info
    # print("main event fighter one name:")
    # print(asccii_string)
    # print("---------------------")

    fighter_one.append(asccii_string)

    main_event_fighter_one_url_array = tree.xpath(
        '/html/body/div[2]/div[2]/div[1]/section[1]/div/div[2]/div[2]/div[1]/h3/a/@href')

    me_fgtr1_wbst = 'http://www.sherdog.com', ''.join(main_event_fighter_one_url_array)

    # debug info
    # print("main event fighter one website: ")
    # print(me_fgtr1_wbst)
    # print("---------------------")
    fighter_one_url.append(me_fgtr1_wbst)

    main_event_fighter_two_array = tree.xpath(
        '/html/body/div[2]/div[2]/div[1]/section[1]/div/div[2]/div[2]/div[2]/h3/a/span/text()')

    newstr2 = ''.join(main_event_fighter_two_array)
    asccii_string2 = smart_str(newstr2)

    # debug info
    # print("main event fighter 2 name: ")
    # print(asccii_string2)
    # print("---------------------")

    fighter_two.append(asccii_string2)

    main_event_fighter_two_url_array = tree.xpath(
        '/html/body/div[2]/div[2]/div[1]/section[1]/div/div[2]/div[2]/div[2]/h3/a/@href')

    me_fgtr2_wbst = 'http://www.sherdog.com', ''.join(main_event_fighter_two_url_array)

    # debug info
    # print("main event fighter 2 website:")
    # print(me_fgtr2_wbst)
    # print("---------------------")

    fighter_two_url.append(me_fgtr2_wbst)
    ###### WORKING ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    for z in range(2, row_len):
        # print("Z is = to: ")
        # print(z)
        # scrape fighter one name
        ##fighter_one_array = tree.xpath('/html/body/div[2]/div[2]/div[1]/section[2]/div/div/table/tbody/tr[%i]/td[2]/a/span/text()' % (z))
        fighter_one_array = tree.xpath(
            '/html/body/div[2]/div[2]/div[1]/section[2]/div/div/table/tbody/tr[%i]/td[2]/div/a/span/text()' % (z))


        # scrape fighter one name
        # fighter_one_array = tree.xpath('/html/body/div[3]/div[2]/div[1]/section[2]/div/div/table/tbody/tr[%i]/td[2]/div/a/span/name/text()' % (z))

        newstr3 = ''.join(fighter_one_array)
        asccii_string3 = smart_str(newstr3)
        # print debug stuff
        #    print("this is the next fighter one:")
        #   print(asccii_string3)
        #  print("========================")
        fighter_one.append(asccii_string3)

        # scrape fighter one URL
        fighter_one_url_array = tree.xpath(
            '/html/body/div[2]/div[2]/div[1]/section[2]/div/div/table/tbody/tr[%i]/td[2]/div/a/@href' % (z))

        fgtr1_wbst = 'http://www.sherdog.com', ''.join(fighter_one_url_array)
        # print("this is the fighter 1 website")
        # print(fgtr1_wbst)
        # print("========================")
        fighter_one_url.append(fgtr1_wbst)
        # scrape fighter two name
        fighter_two_array = tree.xpath(
            '/html/body/div[2]/div[2]/div[1]/section[2]/div/div/table/tbody/tr[%i]/td[4]/div/a/span/text()' % (z))

        newstr4 = ''.join(fighter_two_array)
        asccii_string4 = smart_str(newstr4)

        # print(asccii_string4)
        # print("========================")
        fighter_two.append(asccii_string4)
        # scrape fighter two URL
        fighter_two_url_array = tree.xpath(
            '/html/body/div[2]/div[2]/div[1]/section[2]/div/div/table/tbody/tr[%i]/td[4]/div/a/@href' % (z))

        fgtr2_wbst = 'http://www.sherdog.com', ''.join(fighter_two_url_array)
        # print("this is the fighter 2 website")
        # print(fgtr2_wbst)
        # print("========================")
        fighter_two_url.append(fgtr2_wbst)
        fight_card_event_name.append(this_event_name)
        fight_card_event_url.append(event_main_event_url)
        fight_card_event_org.append(this_event_org)

fighterloop = len(fighter_one)

# print "the length of fighter array is also"
# print "the fighter loop variable:"
# print(fighterloop)

# db = MySQLdb.connect(host="markpereira.com", # your host, usually localhost
#                     user="mark5463_crawler", # your username
#                      passwd="mmacrawl", # your password
#                      db="mark5463_mma") # name of the data base

db = MySQLdb.connect(host="markpereira.com",  # your host, usually localhost
                     user="mark5463_ft_test",  # your username
                     passwd="fttesting",  # your password
                     db="mark5463_ft_prod")
                     # db="mark5463_ft_testdb")  # name of the data base

#  you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()

# This section will delete the information on the table, for a clean run.
cur.execute("TRUNCATE sd_mma_fight_cards")

for y in range(0, fighterloop - 1):
    e_name = ''.join(fight_card_event_name[y])
    e_f1 = ''.join(fighter_one[y])
    e_f1_url = ''.join(fighter_one_url[y])
    e_f2 = ''.join(fighter_two[y])
    e_f2_url = ''.join(fighter_two_url[y])
    e_fc_url = ''.join(fight_card_event_url[y])
    e_mma_org = ''.join(fight_card_event_org[y])
    e_mma_event_id = ''.join(fight_card_event_id[y])
    query = "INSERT INTO sd_mma_fight_cards (event_name, fighter_one, fighter_one_url, fighter_two, fighter_two_url, event_url, event_org, event_id ) VALUES (\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")" % \
            (e_name, e_f1, e_f1_url, e_f2, e_f2_url, e_fc_url, e_mma_org, e_mma_event_id)
    cur.execute(query)

    # cur.execute("INSERT INTO mma_fight_cards (event_name, fighter_one, fighter_one_url, fighter_two, fighter_two_url, event_url) VALUES (\"%s\",\"%s\",\"%s\",\"%s\",\"%s\", \"%s\")" % \
    #        (e_name, e_f1, e_f1_url, e_f2, e_f2_url, e_fc_url))
    print(query)
    # Query not needed after first load

