from lxml import html, etree
import io
#from django.utils.encoding import smart_str, smart_text
import django
from django.utils.encoding import smart_str
django.utils.encoding.smart_text = smart_str
from pyquery import PyQuery as pq
import requests
import MySQLdb
import time
import os

def scrapeEvent(event_url, event_org):

    page = requests.get('%s' % (event_url))
    tree = html.fromstring(page.content)

    d = pq("<html></html>")
    d = pq(etree.fromstring("<html></html>"))
    d = pq(url='%s' % (event_url))

    p = d("#mw-content-text table tr")

    row_len = len(p)

    return;

#local docker mysql
#db = MySQLdb.connect(host="192.168.1.96", user="root", passwd="fttesting", port=3308, db="mark5463_ft_prod", charset="utf8")

#prodlike mysql
db = MySQLdb.connect(
    host=os.environ['MYSQL_HOST'],
    user=os.environ['MYSQL_ID'],
    passwd=os.environ['MYSQL_PASSWORD'],
    db="mark5463_ft_prod",
    charset="utf8"
)

cur = db.cursor()

new_query = '''
SELECT event_id, event_fight_card_url, event_name, event_date, event_org, wiki_event_id, event_past
FROM wiki_mma_events
WHERE event_org = 'UFC' AND event_past = 0

UNION ALL

SELECT event_id, event_fight_card_url, event_name, event_date, event_org, wiki_event_id, event_past
FROM wiki_mma_events
WHERE event_org = 'UFC' AND event_past = 1 AND event_id = (
    SELECT MAX(event_id)
    FROM wiki_mma_events
    WHERE event_org = 'UFC' AND event_past = 1
)
ORDER BY event_id;
'''
# This section will query the database and return all data in the table
# this is useful for first time run. But if you are running perpetually, we can shorten this by only looking for upcoming events
cur.execute(new_query)
# Here we will add event_past = 0 - that way when we select we are only going to scrape upcoming events from ufc, our database is loaded with the previous ones.
#cur.execute("SELECT event_id, event_fight_card_url, event_name, event_date, event_org, wiki_event_id, event_past FROM wiki_mma_events WHERE event_org = 'UFC' AND event_fight_card_url NOT LIKE '%The_Ultimate_Fighter%' AND event_fight_card_url NOT LIKE '%_in_UFC#%' AND event_fight_card_url NOT LIKE '%UFC_on_Fox%' AND event_past = 0")

# initialize the arrays
g_event_name = []
g_event_id = []
g_event_fight_card_url = []
g_event_date = []
g_event_org = []
g_wiki_event_id = []
g_event_past = []

# load our arrays with all of our event data.
#for row in cur.fetchall():
#    g_event_id.append(row[0])
#    g_event_fight_card_url.append(row[1])
#    g_event_name.append(row[2])
#    g_event_date.append(row[3])
#    g_event_org.append(row[4])
#    g_wiki_event_id.append(row[5])
#    g_event_past.append(str(row[6]))

for row in cur.fetchall():
    g_event_id.append(row[0])
    print("Event ID:", row[0])
    
    g_event_fight_card_url.append(row[1])
    print("Event Fight Card URL:", row[1])
    
    g_event_name.append(row[2])
    print("Event Name:", row[2])
    
    g_event_date.append(row[3])
    print("Event Date:", row[3])
    
    g_event_org.append(row[4])
    print("Event Org:", row[4])
    
    g_wiki_event_id.append(row[5])
    print("Wiki Event ID:", row[5])
    
    g_event_past.append(str(row[6]))
    print("Event Past:", str(row[6]))
    
    print("------------------------------")


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

fight_iterator = 1

x_range = len(g_event_name)


db = MySQLdb.connect(
    host=os.environ['MYSQL_HOST'],
    user=os.environ['MYSQL_ID'],
    passwd=os.environ['MYSQL_PASSWORD'],
    db="mark5463_ft_prod",
    charset="utf8"
)

cur = db.cursor()
#first we are deleting the events which are upcoming, so we don't get duplicate fights
cur.execute("DELETE FROM `wiki_mma_fight_cards` WHERE event_past = 0")
print("X Range is: ")
print(x_range)

# This loops for every entry of event in the database to build our fight card information
for x in range(0, x_range):  # prev 0, 533
    print("variable X is : ")
    print(x)
    print("X Range is: ")
    print(x_range)
    # bring in the url information
    ##time.sleep(3) #introducing sleep to prevent ddos and ip ban
    event_main_event_url = g_event_fight_card_url[x]
    print(event_main_event_url)
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
    # print(str(this_event_past))

    d = pq("<html></html>")
    d = pq(etree.fromstring("<html></html>"))
    d = pq(url='%s' % (event_main_event_url))

    p = d('#mw-content-text > div.mw-parser-output > table.toccolours > tbody > tr')

    row_len = len(p) + 1
    fight_iterator = 1
    for z in range(3, row_len):
        #asccii_string3 = ''
        #fgtr1_wbst = ''
        #asccii_string4 = ''
        #fgtr2_wbst = ''
        #ascii_fight_weightclass = ''
        #ascii_fight_method = ''
        #ascii_fight_time = ''
        #ascii_fight_round = ''
        
        
        fighter_one_array = None
        for xpath in ['//*[@id="mw-content-text"]/div[1]/table[2]/tbody/tr[%i]/td[2]/a/text()',
                            '//*[@id="mw-content-text"]/div[1]/table[2]/tbody/tr[%i]/td[2]/text()',
                            '//*[@id="mw-content-text"]/div[1]/table[2]/body/tr[%i]/td[2]/text()',
                            '//*[@id="mw-content-text"]/div[1]/table[3]/tbody/tr[%i]/td[2]/a/text()',
                            '//*[@id="mw-content-text"]/div[1]/table[3]/tbody/tr[%i]/td[2]/text()',
                            '//*[@id="mw-content-text"]/div[1]/table[3]/body/tr[%i]/td[2]/text()',
                            '//*[@id="mw-content-text"]/div[1]/table[2]/tr[%i]/td[2]/a/text()',
                            '//*[@id="mw-content-text"]/div[1]/table[2]/tr[%i]/td[2]/text()',
                            '//*[@id="mw-content-text"]/div[1]/table[3]/tr[%i]/td[2]/a/text()',
                            '//*[@id="mw-content-text"]/div[1]/table[3]/tr[%i]/td[2]/text()']:
            fighter_one_array = tree.xpath(xpath % z)
            if fighter_one_array:
                break

        if fighter_one_array:
            newstr3 = ''.join(fighter_one_array).strip() 
            asccii_string3 = smart_str(newstr3)
            g_fighter_one.append(asccii_string3)
        else:
            g_fighter_one.append('')
        # Try and get the fighter one url
        fighter_one_url_array = None
        for xpath in ['//*[@id="mw-content-text"]/div[1]/table[2]/tbody/tr[%i]/td[2]/a/@href',
                            '//*[@id="mw-content-text"]/div[1]/table[3]/tbody/tr[%i]/td[2]/a/@href',
                            '//*[@id="mw-content-text"]/div[1]/table[2]/tr[%i]/td[2]/a/@href',
                            '//*[@id="mw-content-text"]/div[1]/table[3]/tr[%i]/td[2]/a/@href']:
            fighter_one_url_array = tree.xpath(xpath % z)
            if fighter_one_url_array:
                break

        if fighter_one_url_array:
            fgtr1_wbst = 'https://en.wikipedia.org', ''.join(fighter_one_url_array).strip()
            g_fighter_one_url.append(fgtr1_wbst)
        else:
            fgtr1_wbst = 'https://en.wikipedia.org', ''.join(fighter_one_url_array).strip()
            g_fighter_one_url.append(fgtr1_wbst)
                
            '''
            fighter_one_url_array = tree.xpath('//*[@id="mw-content-text"]/div[1]/table[2]/tbody/tr[%i]/td[2]/a/@href' % (z))
            fgtr1_wbst = 'https://en.wikipedia.org', ''.join(fighter_one_url_array)
            g_fighter_one_url.append(fgtr1_wbst)
            '''
        fighter_two_array = None
        for xpath in ['//*[@id="mw-content-text"]/div[1]/table[2]/tbody/tr[%i]/td[4]/a/text()',
                            '//*[@id="mw-content-text"]/div[1]/table[2]/tbody/tr[%i]/td[4]/text()',
                            '//*[@id="mw-content-text"]/div[1]/table[2]/body/tr[%i]/td[4]/text()',
                            '//*[@id="mw-content-text"]/div[1]/table[3]/tbody/tr[%i]/td[4]/a/text()',
                            '//*[@id="mw-content-text"]/div[1]/table[3]/tbody/tr[%i]/td[4]/text()',
                            '//*[@id="mw-content-text"]/div[1]/table[3]/body/tr[%i]/td[4]/text()',
                            '//*[@id="mw-content-text"]/div[1]/table[2]/tr[%i]/td[4]/a/text()',
                            '//*[@id="mw-content-text"]/div[1]/table[2]/tr[%i]/td[4]/text()',
                            '//*[@id="mw-content-text"]/div[1]/table[3]/tr[%i]/td[4]/a/text()',
                            '//*[@id="mw-content-text"]/div[1]/table[3]/tr[%i]/td[4]/text()']:
            fighter_two_array = tree.xpath(xpath % z)
            if fighter_two_array:
                break

        if fighter_two_array:
            newstr4 = ''.join(fighter_two_array).strip() 
            asccii_string4 = smart_str(newstr4)
            g_fighter_two.append(asccii_string4)
        else:
            g_fighter_two.append('')

                # Try and get the fighter two url
        fighter_two_url_array = None
        for xpath in ['//*[@id="mw-content-text"]/div[1]/table[2]/tbody/tr[%i]/td[4]/a/@href',
                            '//*[@id="mw-content-text"]/div[1]/table[3]/tbody/tr[%i]/td[4]/a/@href',
                            '//*[@id="mw-content-text"]/div[1]/table[2]/tr[%i]/td[4]/a/@href',
                            '//*[@id="mw-content-text"]/div[1]/table[3]/tr[%i]/td[4]/a/@href']:
            fighter_two_url_array = tree.xpath(xpath % z)
            if fighter_two_url_array:
                break

        if fighter_two_url_array:
            fgtr2_wbst = 'https://en.wikipedia.org', ''.join(fighter_two_url_array).strip()
            g_fighter_two_url.append(fgtr2_wbst)
        else:
            fgtr2_wbst = 'https://en.wikipedia.org', ''.join(fighter_two_url_array).strip()
            g_fighter_two_url.append(fgtr2_wbst)
            '''
            fighter_two_url_array = tree.xpath('//*[@id="mw-content-text"]/div[1]/table[2]/tbody/tr[%i]/td[4]/a/@href' % (z))
            fgtr2_wbst = 'https://en.wikipedia.org', ''.join(fighter_two_url_array)
            g_fighter_two_url.append(fgtr2_wbst)
            '''
        fight_method_array = None
        
        for xpath in ['//*[@id="mw-content-text"]/div[1]/table[2]/tbody/tr[%i]/td[5]/text()',
                            '//*[@id="mw-content-text"]/div[1]/table[2]/body/tr[%i]/td[5]/text()',
                            '//*[@id="mw-content-text"]/div[1]/table[3]/tbody/tr[%i]/td[5]/text()',
                            '//*[@id="mw-content-text"]/div[1]/table[3]/body/tr[%i]/td[5]/text()',
                            '//*[@id="mw-content-text"]/div[1]/table[2]/tr[%i]/td[5]/text()',
                            '//*[@id="mw-content-text"]/div[1]/table[3]/tr[%i]/td[5]/text()']:
            fight_method_array = tree.xpath(xpath % z)
            if fight_method_array:
                break

        if fight_method_array:
            new_fight_method_string = ''.join(fight_method_array).strip()
            ascii_fight_method = smart_str(new_fight_method_string)
        else:
            new_fight_method_string = ''
            ascii_fight_method = smart_str(new_fight_method_string)
                
            '''    
            fight_method_array = tree.xpath('//*[@id="mw-content-text"]/div[1]/table[2]/tbody/tr[%i]/td[5]/text()' % (z))
            new_fight_method_string = ''.join(fight_method_array)
            ascii_fight_method = smart_str(new_fight_method_string)
            '''
        fight_round_array = None
     
        for xpath in ['//*[@id="mw-content-text"]/div[1]/table[2]/tbody/tr[%i]/td[6]/text()',
                            '//*[@id="mw-content-text"]/div[1]/table[2]/body/tr[%i]/td[6]/text()',
                            '//*[@id="mw-content-text"]/div[1]/table[3]/tbody/tr[%i]/td[6]/text()',
                            '//*[@id="mw-content-text"]/div[1]/table[3]/body/tr[%i]/td[6]/text()',
                            '//*[@id="mw-content-text"]/div[1]/table[2]/tr[%i]/td[6]/text()',
                            '//*[@id="mw-content-text"]/div[1]/table[3]/tr[%i]/td[6]/text()']:
            fight_round_array = tree.xpath(xpath % z)
            if fight_round_array:
                break

        if fight_round_array:
            new_fight_round_string = ''.join(fight_round_array).strip()
            ascii_fight_round = smart_str(new_fight_round_string)
        else:
            new_fight_round_string = ''
            ascii_fight_round = smart_str(new_fight_round_string)
            
            '''
            fight_round_array = tree.xpath('//*[@id="mw-content-text"]/div[1]/table[2]/tbody/tr[%i]/td[6]/text()' % (z))
            new_fight_round_string = ''.join(fight_round_array)
            ascii_fight_round = smart_str(new_fight_round_string)
            '''
        fight_time_array = None
       
        for xpath in ['//*[@id="mw-content-text"]/div[1]/table[2]/tbody/tr[%i]/td[7]/text()',
                            '//*[@id="mw-content-text"]/div[1]/table[2]/body/tr[%i]/td[7]/text()',
                            '//*[@id="mw-content-text"]/div[1]/table[3]/tbody/tr[%i]/td[7]/text()',
                            '//*[@id="mw-content-text"]/div[1]/table[3]/body/tr[%i]/td[7]/text()',
                            '//*[@id="mw-content-text"]/div[1]/table[2]/tr[%i]/td[7]/text()',
                            '//*[@id="mw-content-text"]/div[1]/table[3]/tr[%i]/td[7]/text()']:
            fight_time_array = tree.xpath(xpath % z)
            if fight_time_array:
                    break

        if fight_time_array:
            new_fight_time_string = ''.join(fight_time_array).strip()
            ascii_fight_time = smart_str(new_fight_time_string)
        else:
            new_fight_time_string = ''
            ascii_fight_time = smart_str(new_fight_time_string)
                    
            '''
            fight_time_array = tree.xpath('//*[@id="mw-content-text"]/div[1]/table[2]/tbody/tr[%i]/td[7]/text()' % (z))
            new_fight_time_string = ''.join(fight_time_array)
            ascii_fight_time = smart_str(new_fight_time_string)
            
            fight_notes_array = tree.xpath('//*[@id="mw-content-text"]/div[1]/table[2]/tbody/tr[%i]/td[8]/text()' % (z))
            new_fight_notes_string = ''.join(fight_notes_array)
            ascii_fight_notes = smart_str(new_fight_notes_string)
            '''
        fight_weightclass_array = None
        for xpath in ['//*[@id="mw-content-text"]/div[1]/table[2]/tbody/tr[%i]/td[1]/text()',
                      '//*[@id="mw-content-text"]/div[1]/table[2]/body/tr[%i]/td[1]/text()',
                      '//*[@id="mw-content-text"]/div[1]/table[3]/tbody/tr[%i]/td[1]/text()',
                      '//*[@id="mw-content-text"]/div[1]/table[3]/body/tr[%i]/td[1]/text()',
                      '//*[@id="mw-content-text"]/div[1]/table[2]/tr[%i]/td[1]/text()',
                      '//*[@id="mw-content-text"]/div[1]/table[3]/tr[%i]/td[1]/text()']:
            fight_weightclass_array = tree.xpath(xpath % z)
            if fight_weightclass_array:
                break

        if fight_weightclass_array:
            new_fight_weightclass_string = ''.join(fight_weightclass_array).strip()
            ascii_fight_weightclass = smart_str(new_fight_weightclass_string)
        else:
            new_fight_weightclass_string = ''
            ascii_fight_weightclass = smart_str(new_fight_weightclass_string)
            
            '''    
            fight_weightclass_array = tree.xpath('//*[@id="mw-content-text"]/div[1]/table[2]/tbody/tr[%i]/td[1]/text()' % (z))
            new_fight_weightclass_string = ''.join(fight_weightclass_array)
            ascii_fight_weightclass = smart_str(new_fight_weightclass_string)        
            '''
        
        g_fight_card_event_name.append(this_event_name)
        g_fight_card_event_url.append(event_main_event_url)
        g_fight_card_org.append(this_event_org)
        g_fight_card_wiki_event_id.append(this_wiki_event_id)
        g_fight_card_event_past.append(str(this_event_past))
        e_name = ''.join(this_event_name).strip()
        e_f1 = ''.join(asccii_string3).strip()
        e_f1_url = ''.join(fgtr1_wbst).strip()
        e_f2 = ''.join(asccii_string4).strip()
        e_f2_url = ''.join(fgtr2_wbst).strip()
        e_fc_url = ''.join(event_main_event_url).strip()
        e_org = ''.join(this_event_org).strip()
         # e_ei = ''.join(g_fight_card_event_id[y])
        e_wei = ''.join(this_wiki_event_id).strip()
        e_ep = ''.join(str(this_event_past))
        db_ep_int = int(e_ep)
        w_fight_id = str(e_wei) + "Fight" + str(fight_iterator)
        if e_f1 and e_f2 and ascii_fight_weightclass:
            query = """
                INSERT INTO wiki_mma_fight_cards
                (event_name, fighter_one, fighter_one_url, fighter_two, fighter_two_url, event_url, event_org, wiki_event_id, event_past, method, time, round, weightclass, wiki_fight_id)
                VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                event_name = VALUES(event_name),
                fighter_one = VALUES(fighter_one),
                fighter_one_url = VALUES(fighter_one_url),
                fighter_two = VALUES(fighter_two),
                fighter_two_url = VALUES(fighter_two_url),
                event_url = VALUES(event_url),
                event_org = VALUES(event_org),
                wiki_event_id = VALUES(wiki_event_id),
                event_past = VALUES(event_past),
                method = VALUES(method),
                time = VALUES(time),
                round = VALUES(round),
                weightclass = VALUES(weightclass)
            """
            values = (e_name, e_f1, e_f1_url, e_f2, e_f2_url, e_fc_url, e_org, e_wei, db_ep_int, ascii_fight_method, ascii_fight_time, ascii_fight_round, ascii_fight_weightclass, w_fight_id)
            cur.execute(query, values)
            print(values)
            fight_iterator = fight_iterator + 1
        else:
            print("Not all required variables have a value. Skipping database insertion.")
            print(e_name,e_f1,e_f2,ascii_fight_weightclass,e_wei,w_fight_id)

    
cur.close()
db.close()
