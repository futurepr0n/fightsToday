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
    d = pq(url='%s' % event_url)

    # get the row length by querying the event table on table rows
    p = d(".content table tr")

    # set the row length
    row_len = len(p)

    return;


# Database Connection
# db = MySQLdb.connect(host="markpereira.com",  # your host, usually localhost
#                     user="mark5463_ft_test",  # your username
#                     passwd="fttesting",  # your password
#                     db="mark5463_ft_prod")  # name of the data base
db = MySQLdb.connect(host="135.23.254.253", user="root", passwd="fttesting", db="mark5463_ft_prod")


#  you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()

# This section will delete the information on the table, for a clean run.
print('CLEAN the Tables')
cur.execute("TRUNCATE sd_mma_fight_cards")

# This section will query the database and return all data in the table
cur.execute("SELECT event_name, event_month, event_day, event_year, event_id, event_fight_card_url, event_org FROM sd_mma_events")

# initialize the arrays
g_event_name = []
g_event_id = []
g_event_fight_card_url = []
g_event_org = []
g_event_month = []
g_event_day = []
g_event_year = []

# load our arrays with all of our event data.
for row in cur.fetchall():
    g_event_name.append(row[0])
    g_event_month.append(row[1])
    g_event_day.append(row[2])
    g_event_year.append(row[3])
    g_event_id.append(row[4])
    g_event_fight_card_url.append(row[5])
    g_event_org.append(row[6])
    print('***********************************************************************************************')
    print('Loading event: \t\t\t %s ...' % row[0])
    print('Loading event ID: \t\t %s ' % row[4])
    print('Loading event Org: \t\t %s' % row[6])
    print('Loading event Date: \t\t', row[1], row[2], row[3])
    print('Loading event URL: \t\t %s' % row[5])
    # print('Loading event Unique ID: \t ', w_e_id)
    print('***********************************************************************************************')


# set up the fighter arrays
g_fighter_one = []
g_fighter_two = []
g_fighter_one_url = []
g_fighter_two_url = []
# fight card specific arrays
g_fight_card_event_name = []
g_fight_card_event_url = []
g_fight_card_event_org = []
g_fight_card_event_id = []

x_range = len(g_event_name)

# This loops for every entry of event in the database to build our fight card information
for x in range(0, x_range - 1):  # prev 0, 533
    print('***********************************************************************************************')
    # bring in the url information
    event_main_event_url = g_event_fight_card_url[x]
    page = requests.get('%s' % event_main_event_url)
    tree = html.fromstring(page.content)
    g_fight_card_event_url.append(event_main_event_url)
    print('Fight_card_event_url = %s ' % event_main_event_url)
    this_event_name = g_event_name[x]
    g_fight_card_event_name.append(this_event_name)
    print('Fight_card_event_name = %s ' % this_event_name)
    this_event_org = g_event_org[x]
    g_fight_card_event_org.append(this_event_org)
    print('Fight_card_event_org = %s ' % this_event_org)
    this_event_id = g_event_id[x]
    g_fight_card_event_id.append(this_event_id)
    print('Fight_card_event_id = %s ' % this_event_id)

    d = pq("<html></html>")
    d = pq(etree.fromstring("<html></html>"))
    d = pq(url='%s' % event_main_event_url)
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
    main_event_fighter_one_array = tree.xpath('/html/body/div[2]/div[2]/div[1]/section[1]/div/div[2]/div[2]/div[1]/h3/a/span/text()')
    newstr = ''.join(main_event_fighter_one_array)
    asccii_string = smart_str(newstr)
    # print("Main event fighter one name: ", asccii_string)
    g_fighter_one.append(asccii_string)

    main_event_fighter_one_url_array = tree.xpath('/html/body/div[2]/div[2]/div[1]/section[1]/div/div[2]/div[2]/div[1]/h3/a/@href')
    me_fgtr1_wbst_string = 'http://www.sherdog.com', ''.join(main_event_fighter_one_url_array)
    me_fgtr1_wbst = ''.join(me_fgtr1_wbst_string)
    # print("Main event fighter one website: ", me_fgtr1_wbst)
    g_fighter_one_url.append(me_fgtr1_wbst)

    main_event_fighter_two_array = tree.xpath('/html/body/div[2]/div[2]/div[1]/section[1]/div/div[2]/div[2]/div[2]/h3/a/span/text()')
    newstr2 = ''.join(main_event_fighter_two_array)
    asccii_string2 = smart_str(newstr2)
    # print("main event fighter 2 name: ", asccii_string2)
    g_fighter_two.append(asccii_string2)

    main_event_fighter_two_url_array = tree.xpath('/html/body/div[2]/div[2]/div[1]/section[1]/div/div[2]/div[2]/div[2]/h3/a/@href')
    me_fgtr2_wbst_string = 'http://www.sherdog.com', ''.join(main_event_fighter_two_url_array)
    me_fgtr2_wbst = ''.join(me_fgtr2_wbst_string)
    # print("main event fighter 2 website:", me_fgtr2_wbst)
    g_fighter_two_url.append(me_fgtr2_wbst)
    print('***********************************************************************************************')
    print("**\tMain event fighter one name:\t\t", asccii_string, "main event fighter two name: \t**", asccii_string2)
    main_event_query = "INSERT INTO sd_mma_fight_cards (event_name, fighter_one, fighter_one_url, fighter_two, fighter_two_url, event_url, event_org, event_id ) VALUES (\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")" % (this_event_name, asccii_string, me_fgtr1_wbst, asccii_string2, me_fgtr2_wbst, event_main_event_url, this_event_org, this_event_id)
    # print(main_event_query) # -- This is the query printed so we can see it. Commented out bc its not necessary.
    print('Query Executed...')
    cur.execute(main_event_query)
    print('Success!...')


    for z in range(2, row_len):
        # scrape fighter one name
        fighter_one_array = tree.xpath('/html/body/div[2]/div[2]/div[1]/section[2]/div/div/table/tbody/tr[%i]/td[2]/div/a/span/text()' % (z))
        newstr3 = ''.join(fighter_one_array)
        asccii_string3 = smart_str(newstr3)
        # print("this is match ", z, " fighter one: \t", asccii_string3)
        g_fighter_one.append(asccii_string3)

        # scrape fighter one URL
        fighter_one_url_array = tree.xpath('/html/body/div[2]/div[2]/div[1]/section[2]/div/div/table/tbody/tr[%i]/td[2]/div/a/@href' % (z))
        # fgtr1_wbst = 'http://www.sherdog.com', ''.join(fighter_one_url_array)
        fgtr1_wbst_string = 'http://www.sherdog.com', ''.join(fighter_one_url_array)
        fgtr1_wbst = ''.join(fgtr1_wbst_string)
        # print("this is the fighter 1 website", fgtr1_wbst)
        g_fighter_one_url.append(fgtr1_wbst)

        # scrape fighter two name
        fighter_two_array = tree.xpath('/html/body/div[2]/div[2]/div[1]/section[2]/div/div/table/tbody/tr[%i]/td[4]/div/a/span/text()' % (z))
        newstr4 = ''.join(fighter_two_array)
        asccii_string4 = smart_str(newstr4)
        # print("this is match ", z, " fighter two: \t", asccii_string4)
        g_fighter_two.append(asccii_string4)

        # scrape fighter two URL
        fighter_two_url_array = tree.xpath('/html/body/div[2]/div[2]/div[1]/section[2]/div/div/table/tbody/tr[%i]/td[4]/div/a/@href' % (z))
        fgtr2_wbst_string = 'http://www.sherdog.com', ''.join(fighter_two_url_array)
        fgtr2_wbst = ''.join(fgtr2_wbst_string)
        # print("this is the fighter 2 website", fgtr2_wbst)
        g_fighter_two_url.append(fgtr2_wbst)

        print("**\tFight ", z, "\tfighter one: ", asccii_string3, "\tfighter two: \t**", asccii_string4)

        undercard_query = "INSERT INTO sd_mma_fight_cards (event_name, fighter_one, fighter_one_url, fighter_two, fighter_two_url, event_url, event_org, event_id ) VALUES (\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")" % (this_event_name, asccii_string3, fgtr1_wbst, asccii_string4, fgtr2_wbst, event_main_event_url, this_event_org, this_event_id)
        # print(undercard_query) # commented out bc we do not need to see the full query unless debug
        print('Query Executing...')
        cur.execute(undercard_query)
        print('Success!...')

        g_fight_card_event_name.append(this_event_name)
        g_fight_card_event_url.append(event_main_event_url)
        g_fight_card_event_org.append(this_event_org)
        g_fight_card_event_id.append(this_event_id)


fighterloop = len(g_fighter_one)

#db = MySQLdb.connect(host="markpereira.com",  # your host, usually localhost
#                     user="mark5463_ft_test",  # your username
#                     passwd="fttesting",  # your password
#                     db="mark5463_ft_prod")
                     # db="mark5463_ft_testdb")  # name of the data base

db = MySQLdb.connect(host="135.23.254.253", user="root", passwd="fttesting", db="mark5463_ft_prod")


#  you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()

# This section will delete the information on the table, for a clean run.
# print('CLEAN the Tables')
# cur.execute("TRUNCATE sd_mma_fight_cards")

# for y in range(0, fighterloop - 1):
#     print('***********************************************************************************************')
#     e_name = ''.join(fight_card_event_name[y])
#     e_f1 = ''.join(fighter_one[y])
#     e_f1_url = ''.join(fighter_one_url[y])
#     e_f2 = ''.join(fighter_two[y])
#     e_f2_url = ''.join(fighter_two_url[y])
#     e_fc_url = ''.join(fight_card_event_url[y])
#     e_mma_org = ''.join(fight_card_event_org[y])
#     e_ev_id = ''.join(str(fight_card_event_id[y]))
#     print('Adding Event: %s ...' % e_name)
#     print('Fighter One: \t\t %i ' % e_f1)
#     print('Fighter One URL: \t\t %s' % e_f1_url)
#     print('Fighter Two: \t\t %i ' % e_f2)
#     print('Fighter Two URL: \t\t %s' % e_f2_url)
#     print('Event Org: \t', e_mma_org)
#     print('Event URL: \t\t %s' % e_fc_url)
#     print('Event ID: \t ', e_ev_id)
#     print('***********************************************************************************************')
#     query = "INSERT INTO sd_mma_fight_cards (event_name, fighter_one, fighter_one_url, fighter_two, fighter_two_url, event_url, event_org, event_id ) VALUES (\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")" % (e_name, e_f1, e_f1_url, e_f2, e_f2_url, e_fc_url, e_mma_org, e_ev_id)
#     print(query)
#     print('***********************************************************************************************')
#     print('Query Executed...')
#     cur.execute(query)
#     print('Success!...')
#     print('***********************************************************************************************')

    # Query not needed after first load

