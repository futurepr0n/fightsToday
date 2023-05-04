
from lxml import html, etree
import io
from django.utils.encoding import smart_str, smart_text
from pyquery import PyQuery as pq
import requests
import MySQLdb
import time

def scrapeEvent(event_url, event_org):

    page = requests.get('%s' % (event_url))
    tree = html.fromstring(page.content)

    d = pq("<html></html>")
    d = pq(etree.fromstring("<html></html>"))
    d = pq(url='%s' % (event_url))

    p = d("#mw-content-text table tr")

    row_len = len(p)

    return;

db = MySQLdb.connect(host="192.168.1.69", user="root", passwd="fttesting", port=3308, db="mark5463_ft_prod", charset="utf8")
cur = db.cursor()

# This section will query the database and return all data in the table
cur.execute("SELECT event_id, event_fight_card_url, event_name, event_date, event_org, wiki_event_id, event_past FROM wiki_mma_events WHERE event_org = 'UFC'")

# initialize the arrays
g_event_name = []
g_event_id = []
g_event_fight_card_url = []
g_event_date = []
g_event_org = []
g_wiki_event_id = []
g_event_past = []

# load our arrays with all of our event data.
for row in cur.fetchall():
    g_event_id.append(row[0])
    g_event_fight_card_url.append(row[1])
    g_event_name.append(row[2])
    g_event_date.append(row[3])
    g_event_org.append(row[4])
    g_wiki_event_id.append(row[5])
    g_event_past.append(str(row[6]))

# set up the fighter arrays
g_fighter_one = []
g_fighter_two = []
g_fighter_one_url = []
g_fighter_two_url = []
g_fight_card_org = []
# fight card specific arrays
g_fight_card_event_name = []
g_fight_card_event_url = []
g_fight_card_event_id = []
g_fight_card_event_past = []
g_fight_card_wiki_event_id = []

x_range = len(g_event_name)

db = MySQLdb.connect(host="markpereira.com",  user="mark5463_ft_test", passwd="fttesting", db="mark5463_ft_prod",charset="utf8") 
cur = db.cursor()
cur.execute("TRUNCATE wiki_mma_fight_cards")


# This loops for every entry of event in the database to build our fight card information
for x in range(0, x_range - 1):  # prev 0, 533
    # bring in the url information
    event_main_event_url = g_event_fight_card_url[x]
    page = requests.get('%s' % (event_main_event_url))
    tree = html.fromstring(page.content)

    this_event_name = g_event_name[x]
    this_event_org = g_event_org[x]
    this_event_id = g_event_id[x]
    this_event_past = g_event_past[x]
    this_wiki_event_id = g_wiki_event_id[x]

    g_fight_card_event_name.append(this_event_name)
    g_fight_card_event_url.append(event_main_event_url)
    g_fight_card_org.append(this_event_org)
    g_fight_card_event_id.append(str(this_event_id))
    g_fight_card_event_past.append(str(this_event_past))
    g_fight_card_wiki_event_id.append(this_wiki_event_id)
    print(str(this_event_past))

    d = pq("<html></html>")
    d = pq(etree.fromstring("<html></html>"))
    d = pq(url='%s' % (event_main_event_url))

    p = d('#mw-content-text > div.mw-parser-output > table.toccolours > tbody > tr')

    row_len = len(p) + 1
    


    for z in range(3, row_len):
        fighter_one_array = tree.xpath('//*[@id="mw-content-text"]/div[1]/table[2]/tbody/tr[%i]/td[2]/a/text()' % (z))
        newstr3 = ''.join(fighter_one_array) 
        asccii_string3 = smart_str(newstr3)
        g_fighter_one.append(asccii_string3)
        fighter_one_url_array = tree.xpath('//*[@id="mw-content-text"]/div[1]/table[2]/tbody/tr[%i]/td[2]/a/@href' % (z))
        fgtr1_wbst = 'https://en.wikipedia.org', ''.join(fighter_one_url_array)
        g_fighter_one_url.append(fgtr1_wbst)
        fighter_two_array = tree.xpath('//*[@id="mw-content-text"]/div[1]/table[2]/tbody/tr[%i]/td[4]/a/text()' % (z))
        newstr4 = ''.join(fighter_two_array)
        asccii_string4 = smart_str(newstr4)
        g_fighter_two.append(asccii_string4)
        fighter_two_url_array = tree.xpath('//*[@id="mw-content-text"]/div[1]/table[2]/tbody/tr[%i]/td[4]/a/@href' % (z))
        fgtr2_wbst = 'https://en.wikipedia.org', ''.join(fighter_two_url_array)
        g_fighter_two_url.append(fgtr2_wbst)
        fight_method_array = tree.xpath('//*[@id="mw-content-text"]/div[1]/table[2]/tbody/tr[%i]/td[5]/text()' % (z))
        new_fight_method_string = ''.join(fight_method_array)
        ascii_fight_method = smart_str(new_fight_method_string)
        fight_round_array = tree.xpath('//*[@id="mw-content-text"]/div[1]/table[2]/tbody/tr[%i]/td[6]/text()' % (z))
        new_fight_round_string = ''.join(fight_round_array)
        ascii_fight_round = smart_str(new_fight_round_string)
        fight_time_array = tree.xpath('//*[@id="mw-content-text"]/div[1]/table[2]/tbody/tr[%i]/td[7]/text()' % (z))
        new_fight_time_string = ''.join(fight_time_array)
        ascii_fight_time = smart_str(new_fight_time_string)        
        fight_notes_array = tree.xpath('//*[@id="mw-content-text"]/div[1]/table[2]/tbody/tr[%i]/td[8]/text()' % (z))
        new_fight_notes_string = ''.join(fight_notes_array)
        ascii_fight_notes = smart_str(new_fight_notes_string)
        fight_weightclass_array = tree.xpath('//*[@id="mw-content-text"]/div[1]/table[2]/tbody/tr[%i]/td[1]/text()' % (z))
        new_fight_weightclass_string = ''.join(fight_weightclass_array)
        ascii_fight_weightclass = smart_str(new_fight_weightclass_string)        
        g_fight_card_event_name.append(this_event_name)
        g_fight_card_event_url.append(event_main_event_url)
        g_fight_card_org.append(this_event_org)
        g_fight_card_wiki_event_id.append(this_wiki_event_id)
        g_fight_card_event_past.append(str(this_event_past))
        e_name = ''.join(this_event_name)
        e_f1 = ''.join(asccii_string3)
        e_f1_url = ''.join(fgtr1_wbst)
        e_f2 = ''.join(asccii_string4)
        e_f2_url = ''.join(fgtr2_wbst)
        e_fc_url = ''.join(event_main_event_url)
        e_org = ''.join(this_event_org)
        # e_ei = ''.join(g_fight_card_event_id[y])
        e_wei = ''.join(this_wiki_event_id)
        e_ep = ''.join(str(this_event_past))
        db_ep_int = int(e_ep)
        query = "INSERT INTO wiki_mma_fight_cards (event_name, fighter_one, fighter_one_url, fighter_two, fighter_two_url, event_url, event_org, wiki_event_id, event_past, method, notes, time, round, weightclass) VALUES (\"%s\",\"%s\",\"%s\",\"%s\",\"%s\", \"%s\", \"%s\", \"%s\", %i, \"%s\", \"%s\", \"%s\", \"%s\", \"%s\")" % (e_name, e_f1, e_f1_url, e_f2, e_f2_url, e_fc_url, e_org, e_wei, db_ep_int, ascii_fight_method, ascii_fight_notes,ascii_fight_time, ascii_fight_round, ascii_fight_weightclass)
        cur.execute(query)

