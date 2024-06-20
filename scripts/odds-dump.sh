#!/bin/bash

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
done

# Execute the insert statements using MySQL
#mysql -h $SERVERNAME -u $USERNAME -p$PASSWORD $DBNAME < insert_statements.sql
# Run MySQL commands using Docker
docker run --rm -i --network=host \
  -e MYSQL_PWD=$PASSWORD \
  mysql:latest \
  mysql -h $SERVERNAME -u $USERNAME $DBNAME < insert_statements.sql
