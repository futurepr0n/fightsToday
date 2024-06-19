import MySQLdb
import json
from pyquery import PyQuery as pq
from datetime import datetime

# Database connection details
servername = "markpereira.com";
username = "mark5463_ft_test";
password = "fttesting66";
dbname = "mark5463_ft_prod";

# Connect to MySQL database
conn = MySQLdb.connect(host=servername, user=username, passwd=password, db=dbname)
cursor = conn.cursor()

# Load JSON data from file
with open('pfl-response.json', 'r') as file:
    data = json.load(file)

# Extract relevant information
events = data['eventGroup']['events']

# Function to insert data into the database
def insert_odds(event_name, fighter_one, fighter_one_odds, fighter_two, fighter_two_odds, timestamp):
    query = '''
    INSERT INTO odds_history (event_name, fighter_one, fighter_one_odds, fighter_two, fighter_two_odds, timestamp)
    VALUES (%s, %s, %s, %s, %s, %s)
    '''
    cursor.execute(query, (event_name, fighter_one, fighter_one_odds, fighter_two, fighter_two_odds, timestamp))
    conn.commit()

# Iterate through events and insert data
for event in events:
    event_name = event['name']
    for offer in event['offers']:
        if offer['label'] == 'Moneyline':
            outcomes = offer['outcomes']
            if len(outcomes) == 2:
                fighter_one = outcomes[0]['participant']
                fighter_one_odds = outcomes[0]['oddsDecimal']
                fighter_two = outcomes[1]['participant']
                fighter_two_odds = outcomes[1]['oddsDecimal']
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                insert_odds(event_name, fighter_one, fighter_one_odds, fighter_two, fighter_two_odds, timestamp)

# Close the connection
conn.close()
