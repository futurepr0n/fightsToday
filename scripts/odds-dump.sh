#!/bin/bash


wget --no-check-certificate -O ufc-response.json "https://sportsbook-nash.draftkings.com/api/sportscontent/dkcaon/v1/leagues/9034?format=json"
wget --no-check-certificate -O pfl-response.json "https://sportsbook.draftkings.com/sites/US-SB/api/v5/eventgroups/142268?format=json"
wget --no-check-certificate -O bellator-response.json "https://sportsbook.draftkings.com/sites/US-SB/api/v5/eventgroups/33112?format=json"

# File paths (add paths to your JSON files here)
FILES=("ufc-response.json" "pfl-response.json" "bellator-response.json")

# MySQL connection details from environment variables
SERVERNAME=${MYSQL_HOST}
USERNAME=${MYSQL_ID}
PASSWORD=${MYSQL_PASSWORD}
DBNAME="mark5463_ft_prod"
TABLENAME="odds"

# Loop through each file
for FILE_PATH in "${FILES[@]}"
do
  # Get the current timestamp
  TIMESTAMP=$(date +%Y-%m-%dT%H:%M:%S)

  # Extract data using jq and format as SQL insert statements
  # For UFC, use the new API format. For PFL and Bellator, use old format for now
  if [ "$FILE_PATH" = "ufc-response.json" ]; then
    # New API format for UFC
    jq -r --arg timestamp "$TIMESTAMP" '
      # Create event name lookup
      (.events | map({(.id): .name}) | add) as $event_names |
      
      # Create selections lookup by marketId  
      (.selections | group_by(.marketId) | map({(.[0].marketId): .}) | add) as $selections_by_market |
      
      # Process each moneyline market
      .markets[] | 
      select(.name == "Moneyline") |
      . as $market |
      
      # Get selections for this market
      ($selections_by_market[$market.id] // []) as $market_selections |
      
      # Only process if we have exactly 2 fighters
      if ($market_selections | length == 2) then
        ($market_selections[0] | {name: .label, odds: .displayOdds.american}) as $fighter1 |
        ($market_selections[1] | {name: .label, odds: .displayOdds.american}) as $fighter2 |
        
        # Get event name from event ID
        $event_names[$market.eventId] as $event_name |
        
        # Format as CSV and create INSERT statement
        [$event_name, $fighter1.name, $fighter1.odds, $fighter2.name, $fighter2.odds, $timestamp] |
        @csv |
        "INSERT INTO odds (event_name, fighter_one, fighter_one_odds, fighter_two, fighter_two_odds, timestamp) VALUES (" + . + ");"
      else
        empty
      end
    ' $FILE_PATH >> insert_statements.sql
  else
    # Old API format for PFL and Bellator
    jq -r --arg timestamp "$TIMESTAMP" '
      .eventGroup.offerCategories[]
      | select(.name == "Fight Lines")
      | .offerSubcategoryDescriptors[].offerSubcategory.offers[]
      | .[]
      | select(.label == "Moneyline")
      | . as $offer
      | $offer.outcomes as $outcomes
      | ($outcomes[0] | {participant_one: .participant, odds_one: .oddsAmerican}) as $first
      | ($outcomes[1] | {participant_two: .participant, odds_two: .oddsAmerican}) as $second
      | [$offer.eventId, $first.participant_one, $first.odds_one, $second.participant_two, $second.odds_two, $timestamp]
      | @csv
      | "INSERT INTO odds (event_name, fighter_one, fighter_one_odds, fighter_two, fighter_two_odds, timestamp) VALUES (" + . + ");"
    ' $FILE_PATH >> insert_statements.sql
  fi
done

# Execute the insert statements using MySQL
# mysql -h $SERVERNAME -u $USERNAME -p$PASSWORD $DBNAME < insert_statements.sql
# Run MySQL commands using Docker
docker run --rm -i --network=host \
  -e MYSQL_PWD=$PASSWORD \
  mysql:latest \
  mysql -h $SERVERNAME -u $USERNAME $DBNAME < insert_statements.sql
