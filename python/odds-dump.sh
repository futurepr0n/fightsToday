#!/bin/bash

# Database connection details
DB_HOST="markpereira.com"
DB_USER="mark5463_ft_test"
DB_PASS="fttesting66"
DB_NAME="mark5463_ft_prod"

# Download JSON files
wget --no-check-certificate -O ufc-response.json "https://sportsbook.draftkings.com/sites/US-SB/api/v5/eventgroups/9034/categories/491?format=json"
wget --no-check-certificate -O pfl-response.json "https://sportsbook.draftkings.com/sites/US-SB/api/v5/eventgroups/142268?format=json"
wget --no-check-certificate -O bellator-response.json "https://sportsbook.draftkings.com/sites/US-SB/api/v5/eventgroups/33112?format=json"

# Files to process
FILES=("pfl-response.json" "ufc-response.json" "bellator-response.json")
# Function to log and handle errors
log_and_exit() {
  echo "$1"
  exit 1
}

# Process each JSON file
for FILE in "${FILES[@]}"; do
  echo "Processing file: $FILE"
  EVENTS=$(jq -c '.eventGroup.events[]' "$FILE" 2>/dev/null) || log_and_exit "Failed to parse events in $FILE"

  # Check if EVENTS is not null
  if [ -z "$EVENTS" ]; then
    log_and_exit "No events found in $FILE"
  fi

  # Iterate over each event
  echo "$EVENTS" | while IFS= read -r EVENT; do
    EVENT_NAME=$(echo "$EVENT" | jq -r '.name')
    OFFERS=$(echo "$EVENT" | jq -c '.offers[]' 2>/dev/null)

    # Check if OFFERS is not null
    if [ -z "$OFFERS" ]; then
      log_and_exit "No offers found for event: $EVENT_NAME in $FILE"
    fi

    # Iterate over each offer
    echo "$OFFERS" | while IFS= read -r OFFER; do
      LABEL=$(echo "$OFFER" | jq -r '.label')
      if [ "$LABEL" == "Moneyline" ]; then
        OUTCOMES=$(echo "$OFFER" | jq -c '.outcomes[]' 2>/dev/null)

        # Check if OUTCOMES is not null
        if [ -z "$OUTCOMES" ]; then
          log_and_exit "No outcomes found for offer: $LABEL in event: $EVENT_NAME in $FILE"
        fi

        FIGHTER_ONE=$(echo "$OUTCOMES" | jq -r '.[0].participant')
        FIGHTER_ONE_ODDS=$(echo "$OUTCOMES" | jq -r '.[0].oddsDecimal')
        FIGHTER_TWO=$(echo "$OUTCOMES" | jq -r '.[1].participant')
        FIGHTER_TWO_ODDS=$(echo "$OUTCOMES" | jq -r '.[1].oddsDecimal')

        TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

        # Insert into database
        QUERY="INSERT INTO odds (event_name, fighter_one, fighter_one_odds, fighter_two, fighter_two_odds, timestamp) VALUES ('$EVENT_NAME', '$FIGHTER_ONE', $FIGHTER_ONE_ODDS, '$FIGHTER_TWO', $FIGHTER_TWO_ODDS, '$TIMESTAMP');"
        mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASS" "$DB_NAME" -e "$QUERY" || log_and_exit "Failed to execute query: $QUERY"
      fi
    done
  done
done


# Upload JSON files via FTP
lftp -u "mp3loader@markpereira.com,korn66!" -e "set ssl:verify-certificate no; put pfl-response.json; exit" ftp.markpereira.com
lftp -u "mp3loader@markpereira.com,korn66!" -e "set ssl:verify-certificate no; put ufc-response.json; exit" ftp.markpereira.com
lftp -u "mp3loader@markpereira.com,korn66!" -e "set ssl:verify-certificate no; put bellator-response.json; exit" ftp.markpereira.com
