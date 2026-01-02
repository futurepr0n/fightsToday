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
import db_utils

def scrapeEvent(event_url, event_org):

    page = requests.get('%s' % (event_url))
    tree = html.fromstring(page.content)

    d = pq("<html></html>")
    d = pq(etree.fromstring("<html></html>"))
    d = pq(url='%s' % (event_url))

    p = d("#mw-content-text table tr")

    row_len = len(p)

    return;
# local docker mysql
#db = MySQLdb.connect(host="192.168.1.96", user="root", passwd="fttesting", port=3308, db="mark5463_ft_prod", charset="utf8")

#production like database
db = MySQLdb.connect(
    host=os.environ['MYSQL_HOST'],
    user=os.environ['MYSQL_ID'],
    passwd=os.environ['MYSQL_PASSWORD'],
    db="mark5463_ft_prod",
    charset="utf8"
)


cur = db.cursor()

# This section will query the database and return all data in the table
#cur.execute("SELECT event_id, event_fight_card_url, event_name, event_date, event_org, wiki_event_id, event_past FROM wiki_mma_events WHERE event_fight_card_url LIKE '%%Bellator\_MMA%%' AND event_org = 'Bellator'")
# this query is for only upcoming events.
cur.execute("SELECT event_id, event_fight_card_url, event_name, event_date, event_org, wiki_event_id, event_past FROM wiki_mma_events WHERE event_fight_card_url LIKE '%%Bellator\_MMA%%' AND event_org = 'Bellator'")



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

cur.close()
db.close()

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

#db = MySQLdb.connect(
#    host=os.environ['MYSQL_HOST'],
#    user=os.environ['MYSQL_ID'],
#    passwd=os.environ['MYSQL_PASSWORD'],
#    db="mark5463_ft_prod",
#    charset="utf8"
#)
#cur = db.cursor()
#cur.execute("TRUNCATE wiki_mma_fight_cards")


# This loops for every entry of event in the database to build our fight card information
for x in range(0, x_range - 1):  # prev 0, 533
    # bring in the url information
    #time.sleep(3) #introducing sleep to prevent ddos and ip ban
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
    # print(str(this_event_past))

    d = pq("<html></html>")
    d = pq(etree.fromstring("<html></html>"))
    d = pq(url='%s' % (event_main_event_url))

    p = d('#mw-content-text > div.mw-parser-output > table.toccolours > tbody > tr')

    #Testing Query the max number of Tables in the article page
    #p_tables = d('#mw-content-text > div.mw-parser-output > table')

    # row_len = len(p) + 1
    #we are commenting it because we are just gonna use row_len = 30
    row_len = 30

    #table_len = len(p_tables)

    event_to_table_mod = {
    'https://en.wikipedia.org/wiki/2009_in_Bellator_MMA#Bellator_1': 3,
    'https://en.wikipedia.org/wiki/2009_in_Bellator_MMA#Bellator_2': 5,
    'https://en.wikipedia.org/wiki/2009_in_Bellator_MMA#Bellator_3': 7,
    'https://en.wikipedia.org/wiki/2009_in_Bellator_MMA#Bellator_4': 9,
    'https://en.wikipedia.org/wiki/2009_in_Bellator_MMA#Bellator_5': 11,
    'https://en.wikipedia.org/wiki/2009_in_Bellator_MMA#Bellator_6': 13,
    'https://en.wikipedia.org/wiki/2009_in_Bellator_MMA#Bellator_7/8': 15,
    'https://en.wikipedia.org/wiki/2009_in_Bellator_MMA#Bellator_9': 17,
    'https://en.wikipedia.org/wiki/2009_in_Bellator_MMA#Bellator_10': 19,
    'https://en.wikipedia.org/wiki/2009_in_Bellator_MMA#Bellator_11': 21,
    'https://en.wikipedia.org/wiki/2009_in_Bellator_MMA#Bellator_12': 23,
    'https://en.wikipedia.org/wiki/2010_in_Bellator_MMA#Bellator_13': 3,
    'https://en.wikipedia.org/wiki/2010_in_Bellator_MMA#Bellator_14': 5,
    'https://en.wikipedia.org/wiki/2010_in_Bellator_MMA#Bellator_15': 7,
    'https://en.wikipedia.org/wiki/2010_in_Bellator_MMA#Bellator_16': 9,
    'https://en.wikipedia.org/wiki/2010_in_Bellator_MMA#Bellator_17': 11,
    'https://en.wikipedia.org/wiki/2010_in_Bellator_MMA#Bellator_18': 13,
    'https://en.wikipedia.org/wiki/2010_in_Bellator_MMA#Bellator_19': 15,
    'https://en.wikipedia.org/wiki/2010_in_Bellator_MMA#Bellator_20': 17,
    'https://en.wikipedia.org/wiki/2010_in_Bellator_MMA#Bellator_21': 19,
    'https://en.wikipedia.org/wiki/2010_in_Bellator_MMA#Bellator_22': 21,
    'https://en.wikipedia.org/wiki/2010_in_Bellator_MMA#Bellator_23': 23,
    'https://en.wikipedia.org/wiki/2012_in_Bellator_MMA#Bellator_74': 37,
    'https://en.wikipedia.org/wiki/2012_in_Bellator_MMA#Bellator_75': 39,
    'https://en.wikipedia.org/wiki/2012_in_Bellator_MMA#Bellator_76': 41,
    'https://en.wikipedia.org/wiki/2012_in_Bellator_MMA#Bellator_77': 43,
    'https://en.wikipedia.org/wiki/2012_in_Bellator_MMA#Bellator_78': 45,
    'https://en.wikipedia.org/wiki/2012_in_Bellator_MMA#Bellator_79': 47,
    'https://en.wikipedia.org/wiki/2012_in_Bellator_MMA#Bellator_70': 49,
    'https://en.wikipedia.org/wiki/2012_in_Bellator_MMA#Bellator_71': 51,
    'https://en.wikipedia.org/wiki/2012_in_Bellator_MMA#Bellator_72': 53,
    'https://en.wikipedia.org/wiki/2012_in_Bellator_MMA#Bellator_73': 55,
    'https://en.wikipedia.org/wiki/2012_in_Bellator_MMA#Bellator_74': 57,
    'https://en.wikipedia.org/wiki/2013_in_Bellator_MMA#Bellator_85': 3,
    'https://en.wikipedia.org/wiki/2013_in_Bellator_MMA#Bellator_86': 5,
    'https://en.wikipedia.org/wiki/2013_in_Bellator_MMA#Bellator_87': 7,
    'https://en.wikipedia.org/wiki/2013_in_Bellator_MMA#Bellator_88': 9,
    'https://en.wikipedia.org/wiki/2013_in_Bellator_MMA#Bellator_89': 11,
    'https://en.wikipedia.org/wiki/2013_in_Bellator_MMA#Bellator_90': 13,
    'https://en.wikipedia.org/wiki/2013_in_Bellator_MMA#Bellator_91': 15,
    'https://en.wikipedia.org/wiki/2013_in_Bellator_MMA#Bellator_92': 17,
    'https://en.wikipedia.org/wiki/2013_in_Bellator_MMA#Bellator_93': 19,
    'https://en.wikipedia.org/wiki/2013_in_Bellator_MMA#Bellator_94': 21,
    'https://en.wikipedia.org/wiki/2013_in_Bellator_MMA#Bellator_95': 23,
    'https://en.wikipedia.org/wiki/2013_in_Bellator_MMA#Bellator_96': 30,
    'https://en.wikipedia.org/wiki/2013_in_Bellator_MMA#Bellator_97': 32,
    'https://en.wikipedia.org/wiki/2013_in_Bellator_MMA#Bellator_98': 37,
    'https://en.wikipedia.org/wiki/2013_in_Bellator_MMA#Bellator_99': 39,
    'https://en.wikipedia.org/wiki/2013_in_Bellator_MMA#Bellator_100': 41,
    'https://en.wikipedia.org/wiki/2013_in_Bellator_MMA#Bellator_101': 43,
    'https://en.wikipedia.org/wiki/2013_in_Bellator_MMA#Bellator_102': 45,
    'https://en.wikipedia.org/wiki/2013_in_Bellator_MMA#Bellator_103': 47,
    'https://en.wikipedia.org/wiki/2013_in_Bellator_MMA#Bellator_104': 49,
    'https://en.wikipedia.org/wiki/2013_in_Bellator_MMA#Bellator_105': 51,
    'https://en.wikipedia.org/wiki/2013_in_Bellator_MMA#Bellator_106': 53,
    'https://en.wikipedia.org/wiki/2013_in_Bellator_MMA#Bellator_107': 55,
    'https://en.wikipedia.org/wiki/2013_in_Bellator_MMA#Bellator_108': 57,
    'https://en.wikipedia.org/wiki/2013_in_Bellator_MMA#Bellator_109': 59,
    'https://en.wikipedia.org/wiki/2014_in_Bellator_MMA#Bellator_110': 3,
    'https://en.wikipedia.org/wiki/2014_in_Bellator_MMA#Bellator_111': 5,
    'https://en.wikipedia.org/wiki/2014_in_Bellator_MMA#Bellator_112': 7,
    'https://en.wikipedia.org/wiki/2014_in_Bellator_MMA#Bellator_113': 9,
    'https://en.wikipedia.org/wiki/2014_in_Bellator_MMA#Bellator_114': 11,
    'https://en.wikipedia.org/wiki/2014_in_Bellator_MMA#Bellator_115': 13,
    'https://en.wikipedia.org/wiki/2014_in_Bellator_MMA#Bellator_116': 15,
    'https://en.wikipedia.org/wiki/2014_in_Bellator_MMA#Bellator_117': 17,
    'https://en.wikipedia.org/wiki/2014_in_Bellator_MMA#Bellator_118': 19,
    'https://en.wikipedia.org/wiki/2014_in_Bellator_MMA#Bellator_119': 21,
    'https://en.wikipedia.org/wiki/2014_in_Bellator_MMA#Bellator_120': 23,
    'https://en.wikipedia.org/wiki/2014_in_Bellator_MMA#Bellator_121': 31,
    'https://en.wikipedia.org/wiki/2014_in_Bellator_MMA#Bellator_122': 33,
    'https://en.wikipedia.org/wiki/2014_in_Bellator_MMA#Bellator_123': 36,
    'https://en.wikipedia.org/wiki/2014_in_Bellator_MMA#Bellator_124': 38,
    'https://en.wikipedia.org/wiki/2014_in_Bellator_MMA#Bellator_125': 40,
    'https://en.wikipedia.org/wiki/2014_in_Bellator_MMA#Bellator_126': 42,
    'https://en.wikipedia.org/wiki/2014_in_Bellator_MMA#Bellator_127': 44,
    'https://en.wikipedia.org/wiki/2014_in_Bellator_MMA#Bellator_128': 46,
    'https://en.wikipedia.org/wiki/2014_in_Bellator_MMA#Bellator_129': 48,
    'https://en.wikipedia.org/wiki/2014_in_Bellator_MMA#Bellator_2014_Monster_Energy_Cup': 50,
    'https://en.wikipedia.org/wiki/2014_in_Bellator_MMA#Bellator_130': 52,
    'https://en.wikipedia.org/wiki/2014_in_Bellator_MMA#Bellator_131': 54,
    'https://en.wikipedia.org/wiki/2015_in_Bellator_MMA#Bellator_132': 3,
    'https://en.wikipedia.org/wiki/2015_in_Bellator_MMA#Bellator_133': 5,
    'https://en.wikipedia.org/wiki/2015_in_Bellator_MMA#Bellator_134': 7,
    'https://en.wikipedia.org/wiki/2015_in_Bellator_MMA#Bellator_135': 9,
    'https://en.wikipedia.org/wiki/2015_in_Bellator_MMA#Bellator_136': 11,
    'https://en.wikipedia.org/wiki/2015_in_Bellator_MMA#Bellator_137': 13,
    'https://en.wikipedia.org/wiki/2015_in_Bellator_MMA#Bellator_138': 15,
    'https://en.wikipedia.org/wiki/2015_in_Bellator_MMA#Bellator_139': 17,
    'https://en.wikipedia.org/wiki/2015_in_Bellator_MMA#Bellator_140': 19,
    'https://en.wikipedia.org/wiki/2015_in_Bellator_MMA#Bellator_141': 21,
    'https://en.wikipedia.org/wiki/Bellator_MMA_%26_Glory:_Dynamite_1': 2,
    'https://en.wikipedia.org/wiki/2015_in_Bellator_MMA#Bellator_143': 24,
    'https://en.wikipedia.org/wiki/2015_in_Bellator_MMA#Bellator_144': 26,
    'https://en.wikipedia.org/wiki/2015_in_Bellator_MMA#Bellator_145': 28,
    'https://en.wikipedia.org/wiki/2015_in_Bellator_MMA#Bellator_146': 30,
    'https://en.wikipedia.org/wiki/2015_in_Bellator_MMA#Bellator_147': 32,
    'https://en.wikipedia.org/wiki/2016_in_Bellator_MMA#Bellator_148': 3,
    'https://en.wikipedia.org/wiki/2016_in_Bellator_MMA#Bellator_149': 5,
    'https://en.wikipedia.org/wiki/2016_in_Bellator_MMA#Bellator_150': 7,
    'https://en.wikipedia.org/wiki/2016_in_Bellator_MMA#Bellator_151': 9,
    'https://en.wikipedia.org/wiki/2016_in_Bellator_MMA#Bellator_152': 11,
    'https://en.wikipedia.org/wiki/2016_in_Bellator_MMA#Bellator_153': 13,
    'https://en.wikipedia.org/wiki/2016_in_Bellator_MMA#Bellator_154': 15,
    'https://en.wikipedia.org/wiki/2016_in_Bellator_MMA#Bellator_155': 17,
    'https://en.wikipedia.org/wiki/2016_in_Bellator_MMA#Bellator_156': 19,
    'https://en.wikipedia.org/wiki/2016_in_Bellator_MMA#Bellator_157': 21,
    'https://en.wikipedia.org/wiki/2016_in_Bellator_MMA#Bellator_158': 23,
    'https://en.wikipedia.org/wiki/2016_in_Bellator_MMA#Bellator_159': 25,
    'https://en.wikipedia.org/wiki/2016_in_Bellator_MMA#Bellator_160': 27,
    'https://en.wikipedia.org/wiki/2016_in_Bellator_MMA#Bellator_161': 29,
    'https://en.wikipedia.org/wiki/2016_in_Bellator_MMA#Bellator_Kickboxing_3': 31,
    'https://en.wikipedia.org/wiki/2016_in_Bellator_MMA#Bellator_162': 33,
    'https://en.wikipedia.org/wiki/2016_in_Bellator_MMA#Bellator_163': 35,
    'https://en.wikipedia.org/wiki/2016_in_Bellator_MMA#Bellator_164': 37,
    'https://en.wikipedia.org/wiki/2016_in_Bellator_MMA#Bellator_165': 39,
    'https://en.wikipedia.org/wiki/2016_in_Bellator_MMA#Bellator_166': 41,
    'https://en.wikipedia.org/wiki/2016_in_Bellator_MMA#Bellator_167': 43,
    'https://en.wikipedia.org/wiki/2016_in_Bellator_MMA#Bellator_168': 45,
    'https://en.wikipedia.org/wiki/2016_in_Bellator_MMA#Bellator_169': 47,
    'https://en.wikipedia.org/wiki/2017_in_Bellator_MMA#Bellator_170': 3,
    'https://en.wikipedia.org/wiki/2017_in_Bellator_MMA#Bellator_171': 5,
    'https://en.wikipedia.org/wiki/2017_in_Bellator_MMA#Bellator_172': 7,
    'https://en.wikipedia.org/wiki/2017_in_Bellator_MMA#Bellator_173': 9,
    'https://en.wikipedia.org/wiki/2017_in_Bellator_MMA#Bellator_174': 11,
    'https://en.wikipedia.org/wiki/2017_in_Bellator_MMA#Bellator_175': 13,
    'https://en.wikipedia.org/wiki/2017_in_Bellator_MMA#Bellator_176': 15,
    'https://en.wikipedia.org/wiki/2017_in_Bellator_MMA#Bellator_177': 17,
    'https://en.wikipedia.org/wiki/2017_in_Bellator_MMA#Bellator_178': 19,
    'https://en.wikipedia.org/wiki/2017_in_Bellator_MMA#Bellator_179': 21,
    'https://en.wikipedia.org/wiki/2017_in_Bellator_MMA#Bellator_Monster_Energy_Fight_Series:_Charlotte': 23,
    'https://en.wikipedia.org/wiki/2017_in_Bellator_MMA#Bellator_NYC/Bellator_180': 25,
    'https://en.wikipedia.org/wiki/2017_in_Bellator_MMA#Bellator_181': 27,
    'https://en.wikipedia.org/wiki/2017_in_Bellator_MMA#Bellator_Monster_Energy_Fight_Series:_Bristol': 29,
    'https://en.wikipedia.org/wiki/2017_in_Bellator_MMA#Bellator_182': 31,
    'https://en.wikipedia.org/wiki/2017_in_Bellator_MMA#Bellator_183': 33,
    'https://en.wikipedia.org/wiki/2017_in_Bellator_MMA#Bellator_184': 35,
    'https://en.wikipedia.org/wiki/2017_in_Bellator_MMA#Bellator_Monster_Energy_Fight_Series:_Talladega': 37,
    'https://en.wikipedia.org/wiki/2017_in_Bellator_MMA#Bellator_185': 39,
    'https://en.wikipedia.org/wiki/2017_in_Bellator_MMA#Bellator_186': 41,
    'https://en.wikipedia.org/wiki/2017_in_Bellator_MMA#Bellator_187': 43,
    'https://en.wikipedia.org/wiki/2017_in_Bellator_MMA#Bellator_188': 45,
    'https://en.wikipedia.org/wiki/2017_in_Bellator_MMA#Bellator:_Monster_Energy_Fight_Series:_Homestead': 47,
    'https://en.wikipedia.org/wiki/2017_in_Bellator_MMA#Bellator_189': 49,
    'https://en.wikipedia.org/wiki/2017_in_Bellator_MMA#Bellator_190': 51,
    'https://en.wikipedia.org/wiki/2017_in_Bellator_MMA#Bellator_191': 53,
    'https://en.wikipedia.org/wiki/2018_in_Bellator_MMA#Bellator_192': 5,
    'https://en.wikipedia.org/wiki/2018_in_Bellator_MMA#Bellator_193': 7,
    'https://en.wikipedia.org/wiki/2018_in_Bellator_MMA#Bellator_194': 9,
    'https://en.wikipedia.org/wiki/2018_in_Bellator_MMA#Bellator_195': 11,
    'https://en.wikipedia.org/wiki/2018_in_Bellator_MMA#Bellator_Monster_Energy_Fight_Series:_Atlanta': 13,
    'https://en.wikipedia.org/wiki/2018_in_Bellator_MMA#Bellator_196': 15,
    'https://en.wikipedia.org/wiki/2018_in_Bellator_MMA#Bellator_197': 17,
    'https://en.wikipedia.org/wiki/2018_in_Bellator_MMA#Bellator_198': 19,
    'https://en.wikipedia.org/wiki/2018_in_Bellator_MMA#Bellator_199': 21,
    'https://en.wikipedia.org/wiki/2018_in_Bellator_MMA#Bellator_200': 23,
    'https://en.wikipedia.org/wiki/2018_in_Bellator_MMA#Bellator_201': 25,
    'https://en.wikipedia.org/wiki/2018_in_Bellator_MMA#Bellator_202': 27,
    'https://en.wikipedia.org/wiki/2018_in_Bellator_MMA#Bellator_203': 29,
    'https://en.wikipedia.org/wiki/2018_in_Bellator_MMA#Bellator_204': 31,
    'https://en.wikipedia.org/wiki/2018_in_Bellator_MMA#Bellator_205': 33,
    'https://en.wikipedia.org/wiki/2018_in_Bellator_MMA#Bellator_206': 35,
    'https://en.wikipedia.org/wiki/2018_in_Bellator_MMA#Bellator_207': 37,
    'https://en.wikipedia.org/wiki/2018_in_Bellator_MMA#Bellator_208': 39,
    'https://en.wikipedia.org/wiki/2018_in_Bellator_MMA#Bellator_209': 41,
    'https://en.wikipedia.org/wiki/2018_in_Bellator_MMA#Bellator_210': 43,
    'https://en.wikipedia.org/wiki/2018_in_Bellator_MMA#Bellator_211': 45,
    'https://en.wikipedia.org/wiki/2018_in_Bellator_MMA#Bellator_112': 47,
    'https://en.wikipedia.org/wiki/2018_in_Bellator_MMA#Bellator_213': 49,
    'https://en.wikipedia.org/wiki/2019_in_Bellator_MMA#Bellator_214': 5,
    'https://en.wikipedia.org/wiki/2019_in_Bellator_MMA#Bellator_Newcastle': 7,
    'https://en.wikipedia.org/wiki/2019_in_Bellator_MMA#Bellator_215': 9,
    'https://en.wikipedia.org/wiki/2019_in_Bellator_MMA#Bellator_216': 11,
    'https://en.wikipedia.org/wiki/2019_in_Bellator_MMA#Bellator_217': 13,
    'https://en.wikipedia.org/wiki/2019_in_Bellator_MMA#Bellator_218': 15,
    'https://en.wikipedia.org/wiki/2019_in_Bellator_MMA#Bellator_219': 17,
    'https://en.wikipedia.org/wiki/2019_in_Bellator_MMA#Bellator_220': 19,
    'https://en.wikipedia.org/wiki/2019_in_Bellator_MMA#Bellator_Birmingham': 21,
    'https://en.wikipedia.org/wiki/2019_in_Bellator_MMA#Bellator_221': 23,
    'https://en.wikipedia.org/wiki/2019_in_Bellator_MMA#Bellator_222': 25,
    'https://en.wikipedia.org/wiki/2019_in_Bellator_MMA#Bellator_223': 27,
    'https://en.wikipedia.org/wiki/2019_in_Bellator_MMA#Bellator_224': 29,
    'https://en.wikipedia.org/wiki/2019_in_Bellator_MMA#Bellator_225': 31,
    'https://en.wikipedia.org/wiki/2019_in_Bellator_MMA#Bellator_226': 33,
    'https://en.wikipedia.org/wiki/2019_in_Bellator_MMA#Bellator_Dublin/Bellator_227': 35,
    'https://en.wikipedia.org/wiki/2019_in_Bellator_MMA#Bellator_228': 37,
    'https://en.wikipedia.org/wiki/2019_in_Bellator_MMA#Bellator_229': 39,
    'https://en.wikipedia.org/wiki/2019_in_Bellator_MMA#Bellator_Milan/Bellator_230': 41,
    'https://en.wikipedia.org/wiki/2019_in_Bellator_MMA#Bellator_231': 43,
    'https://en.wikipedia.org/wiki/2019_in_Bellator_MMA#Bellator_132': 45,
    'https://en.wikipedia.org/wiki/2019_in_Bellator_MMA#Bellator_233': 47,
    'https://en.wikipedia.org/wiki/2019_in_Bellator_MMA#Bellator_234': 49,
    'https://en.wikipedia.org/wiki/2019_in_Bellator_MMA#Bellator_London_2': 51,
    'https://en.wikipedia.org/wiki/2019_in_Bellator_MMA#Bellator_235': 53,
    'https://en.wikipedia.org/wiki/2019_in_Bellator_MMA#Bellator_236': 55,
    'https://en.wikipedia.org/wiki/2019_in_Bellator_MMA#Bellator_237': 57,
    'https://en.wikipedia.org/wiki/2020_in_Bellator_MMA#Bellator_238': 4,
    'https://en.wikipedia.org/wiki/2020_in_Bellator_MMA#Bellator_239': 6,
    'https://en.wikipedia.org/wiki/2020_in_Bellator_MMA#Bellator_240': 8,
    'https://en.wikipedia.org/wiki/2020_in_Bellator_MMA#Bellator_241_(Cancelled)': 10,
    'https://en.wikipedia.org/wiki/2020_in_Bellator_MMA#Bellator_242_(Cancelled)': 12,
    'https://en.wikipedia.org/wiki/2020_in_Bellator_MMA#Bellator_London_3_(Cancelled)': 14,
    'https://en.wikipedia.org/wiki/2020_in_Bellator_MMA#Bellator_243_(Cancelled)': 16,
    'https://en.wikipedia.org/wiki/2020_in_Bellator_MMA#Bellator_244_(Cancelled)': 18,
    'https://en.wikipedia.org/wiki/2020_in_Bellator_MMA#Bellator_242': 20,
    'https://en.wikipedia.org/wiki/2020_in_Bellator_MMA#Bellator_243': 22,
    'https://en.wikipedia.org/wiki/2020_in_Bellator_MMA#Bellator_244': 24,
    'https://en.wikipedia.org/wiki/2020_in_Bellator_MMA#Bellator_245': 26,
    'https://en.wikipedia.org/wiki/2020_in_Bellator_MMA#Bellator_246': 28,
    'https://en.wikipedia.org/wiki/2020_in_Bellator_MMA#Bellator_Milan_2': 30,
    'https://en.wikipedia.org/wiki/2020_in_Bellator_MMA#Bellator_247': 32,
    'https://en.wikipedia.org/wiki/2020_in_Bellator_MMA#Bellator_Dublin_3_(Cancelled)': 34,
    'https://en.wikipedia.org/wiki/2020_in_Bellator_MMA#Bellator_Milan_3': 36,
    'https://en.wikipedia.org/wiki/2020_in_Bellator_MMA#Bellator_248': 38,
    'https://en.wikipedia.org/wiki/2020_in_Bellator_MMA#Bellator_249': 40,
    'https://en.wikipedia.org/wiki/2020_in_Bellator_MMA#Bellator_250': 42,
    'https://en.wikipedia.org/wiki/2020_in_Bellator_MMA#Bellator_251': 44,
    'https://en.wikipedia.org/wiki/2020_in_Bellator_MMA#Bellator_152': 46,
    'https://en.wikipedia.org/wiki/2020_in_Bellator_MMA#Bellator_253': 48,
    'https://en.wikipedia.org/wiki/2020_in_Bellator_MMA#Bellator_254': 50,
    }

    if event_main_event_url in event_to_table_mod:
        table_mod = event_to_table_mod[event_main_event_url]
    else:
        table_mod = 3
 
    fight_iterator = 1
    db = MySQLdb.connect(
    host=os.environ['MYSQL_HOST'],
    user=os.environ['MYSQL_ID'],
    passwd=os.environ['MYSQL_PASSWORD'],
    db="mark5463_ft_prod",
    charset="utf8")
    cur = db.cursor()
    for z in range(3, row_len):
        asccii_string3 = ''
        fgtr1_wbst = ''
        asccii_string4 = ''
        fgtr2_wbst = ''
        ascii_fight_weightclass = ''
        ascii_fight_method = ''
        ascii_fight_time = ''
        ascii_fight_round = ''
        
        fighter_one_array = None
        for xpath in ['//*[@id="mw-content-text"]/div[1]/table[%i]/tbody/tr[%i]/td[2]/a/text()',
                      '//*[@id="mw-content-text"]/div[1]/table[%i]/tbody/tr[%i]/td[2]/text()',
                      '//*[@id="mw-content-text"]/div[1]/table[%i]/body/tr[%i]/td[2]/text()',
                      '//*[@id="mw-content-text"]/div[1]/table[%i]/tr[%i]/td[2]/a/text()',
                      '//*[@id="mw-content-text"]/div[1]/table[%i]/tr[%i]/td[2]/text()']:
            fighter_one_array = tree.xpath(xpath % (table_mod, z))
            if fighter_one_array:
                # print(fighter_one_array)
                break;
                    

        if fighter_one_array:
            newstr3 = ''.join(fighter_one_array) 
            asccii_string3 = smart_str(newstr3)
            g_fighter_one.append(asccii_string3)
        else:
            g_fighter_one.append('')

        
        # Try and get the fighter one url
        fighter_one_url_array = None
        for xpath in ['//*[@id="mw-content-text"]/div[1]/table[%i]/tbody/tr[%i]/td[2]/a/@href',
                      '//*[@id="mw-content-text"]/div[1]/table[%i]/tr[%i]/td[2]/a/@href']:
            fighter_one_url_array = tree.xpath(xpath % (table_mod, z))
            if fighter_one_url_array:
                # print(fighter_one_url_array)
                break

        if fighter_one_url_array:
            fgtr1_wbst = 'https://en.wikipedia.org', ''.join(fighter_one_url_array)
            g_fighter_one_url.append(fgtr1_wbst)
        else:
            fgtr1_wbst = 'https://en.wikipedia.org', ''.join(fighter_one_url_array)
            g_fighter_one_url.append(fgtr1_wbst)
            
        fighter_two_array = None
        for xpath in ['//*[@id="mw-content-text"]/div[1]/table[%i]/tbody/tr[%i]/td[4]/a/text()',
                        '//*[@id="mw-content-text"]/div[1]/table[%i]/tbody/tr[%i]/td[4]/text()',
                        '//*[@id="mw-content-text"]/div[1]/table[%i]/body/tr[%i]/td[4]/text()',
                        '//*[@id="mw-content-text"]/div[1]/table[%i]/tr[%i]/td[4]/a/text()',
                        '//*[@id="mw-content-text"]/div[1]/table[%i]/tr[%i]/td[4]/text()']:
            fighter_two_array = tree.xpath(xpath % (table_mod, z))
            if fighter_two_array:
                # print(fighter_two_array)
                break

        if fighter_two_array:
            newstr4 = ''.join(fighter_two_array) 
            asccii_string4 = smart_str(newstr4)
            g_fighter_two.append(asccii_string4)
        else:
            g_fighter_two.append('')

        # Try and get the fighter two url
        fighter_two_url_array = None
        for xpath in ['//*[@id="mw-content-text"]/div[1]/table[%i]/tbody/tr[%i]/td[4]/a/@href',
                        '//*[@id="mw-content-text"]/div[1]/table[%i]/tr[%i]/td[4]/a/@href']:
            fighter_two_url_array = tree.xpath(xpath % (table_mod, z))
            if fighter_two_url_array:
                # print(fighter_two_url_array)
                break

        if fighter_two_url_array:
            fgtr2_wbst = 'https://en.wikipedia.org', ''.join(fighter_two_url_array)
            g_fighter_two_url.append(fgtr2_wbst)
        else:
            fgtr2_wbst = 'https://en.wikipedia.org', ''.join(fighter_two_url_array)
            g_fighter_two_url.append(fgtr2_wbst)
       
        fight_method_array = None
        for xpath in ['//*[@id="mw-content-text"]/div[1]/table[%i]/tbody/tr[%i]/td[5]/text()',
                        '//*[@id="mw-content-text"]/div[1]/table[%i]/body/tr[%i]/td[5]/text()',
                        '//*[@id="mw-content-text"]/div[1]/table[%i]/tr[%i]/td[5]/text()']:
            fight_method_array = tree.xpath(xpath % (table_mod, z))
            if fight_method_array:
                break

        if fight_method_array:
            new_fight_method_string = ''.join(fight_method_array)
            ascii_fight_method = smart_str(new_fight_method_string)
        else:
            new_fight_method_string = ''
            ascii_fight_method = smart_str(new_fight_method_string)
            
           
        fight_round_array = None
        for xpath in ['//*[@id="mw-content-text"]/div[1]/table[%i]/tbody/tr[%i]/td[6]/text()',
                        '//*[@id="mw-content-text"]/div[1]/table[%i]/body/tr[%i]/td[6]/text()',
                        '//*[@id="mw-content-text"]/div[1]/table[%i]/tr[%i]/td[6]/text()']:
            fight_round_array = tree.xpath(xpath % (table_mod, z))
            if fight_round_array:
                break

        if fight_round_array:
            new_fight_round_string = ''.join(fight_round_array)
            ascii_fight_round = smart_str(new_fight_round_string)
        else:
            new_fight_round_string = ''
            ascii_fight_round = smart_str(new_fight_round_string)
            
        fight_time_array = None
        for xpath in ['//*[@id="mw-content-text"]/div[1]/table[%i]/tbody/tr[%i]/td[7]/text()',
                        '//*[@id="mw-content-text"]/div[1]/table[%i]/body/tr[%i]/td[7]/text()',
                        '//*[@id="mw-content-text"]/div[1]/table[%i]/tr[%i]/td[7]/text()']:
            fight_time_array = tree.xpath(xpath % (table_mod, z))
            if fight_time_array:
                break

        if fight_time_array:
            new_fight_time_string = ''.join(fight_time_array)
            ascii_fight_time = smart_str(new_fight_time_string)
        else:
            new_fight_time_string = ''
            ascii_fight_time = smart_str(new_fight_time_string)
                

        #fight_notes_array = tree.xpath('//*[@id="mw-content-text"]/div[1]/table[%i]/tbody/tr[%i]/td[8]/text()' % ((table_mod, z)))
        #new_fight_notes_string = ''.join(fight_notes_array)
        #ascii_fight_notes = smart_str(new_fight_notes_string)
            
        fight_weightclass_array = None
        for xpath in ['//*[@id="mw-content-text"]/div[1]/table[%i]/tbody/tr[%i]/td[1]/text()',
                        '//*[@id="mw-content-text"]/div[1]/table[%i]/body/tr[%i]/td[1]/text()',
                        '//*[@id="mw-content-text"]/div[1]/table[%i]/tr[%i]/td[1]/text()']:
            fight_weightclass_array = tree.xpath(xpath % (table_mod, z))
            if fight_weightclass_array:
                break

        if fight_weightclass_array:
            new_fight_weightclass_string = ''.join(fight_weightclass_array)
            ascii_fight_weightclass = smart_str(new_fight_weightclass_string)
        else:
            new_fight_weightclass_string = ''
            ascii_fight_weightclass = smart_str(new_fight_weightclass_string)

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
        e_ep = ''.join(str(this_event_past)).strip()
        db_ep_int = int(e_ep)
        w_fight_id = str(e_wei) + "Fight" + str(fight_iterator)
        if e_f1 and e_f2 and ascii_fight_time and ascii_fight_round and ascii_fight_weightclass:
            # print('I am going to insert a query')
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
            db_utils.execute_on_postgres(query, values)
            # print(query, values)
            fight_iterator = fight_iterator + 1
        else:
            print("Not all required variables have a value. Skipping database insertion.")
            # print(e_name,e_f1,e_f2,e_fc_url)

cur.close()
db.close()
