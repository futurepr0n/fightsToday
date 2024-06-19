#!/bin/bash

# Database connection details
DB_HOST="markpereira.com"
DB_USER="mark5463_ft_test"
DB_PASS="fttesting66"
DB_NAME="mark5463_ft_prod"

# Function to compare fighter names
compare_fighter_names() {
  local name1="$1"
  local name2="$2"
  local name1_lower
  local name2_lower
  local name1_parts
  local name2_parts

  name1_lower=$(echo "$name1" | tr '[:upper:]' '[:lower:]')
  name2_lower=$(echo "$name2" | tr '[:upper:]' '[:lower:]')
  IFS=' ' read -r -a name1_parts <<< "$name1_lower"
  IFS=' ' read -r -a name2_parts <<< "$name2_lower"

  for part1 in "${name1_parts[@]}"; do
    for part2 in "${name2_parts[@]}"; do
      if [ "$part1" == "$part2" ]; then
        return 0
      fi
    done
  done
  return 1
}

# Download JSON files
#wget --no-check-certificate -O ufc-response.json "https://sportsbook.draftkings.com/sites/US-SB/api/v5/eventgroups/9034/categories/491?format=json"
#wget --no-check-certificate -O pfl-response.json "https://sportsbook.draftkings.com/sites/US-SB/api/v5/eventgroups/142268?format=json"
#wget --no-check-certificate -O bellator-response.json "https://sportsbook.draftkings.com/sites/US-SB/api/v5/eventgroups/33112?format=json"

# Files to process
FILES=("pfl-response.json" "ufc-response.json" "bellator-response.json")

# Process each JSON file
for FILE in "${FILES[@]}"; do
  echo "Processing file: $FILE"
  EVENT_GROUP_NAME=$(jq -r '.eventGroup.name' "$FILE")

  OFFER_CATEGORIES=$(jq -c '.eventGroup.offerCategories[]' "$FILE")

  # Iterate over each category
  echo "$OFFER_CATEGORIES" | while IFS= read -r CATEGORY; do
    OFFER_SUBCATEGORY_DESCRIPTORS=$(echo "$CATEGORY" | jq -c '.offerSubcategoryDescriptors[]')

    # Iterate over each subcategory descriptor
    echo "$OFFER_SUBCATEGORY_DESCRIPTORS" | while IFS= read -r DESCRIPTOR; do
      OFFERS=$(echo "$DESCRIPTOR" | jq -c '.offerSubcategory.offers[]')

      # Iterate over each offer group
      echo "$OFFERS" | while IFS= read -r OFFER_GROUP; do
        echo "$OFFER_GROUP" | jq -c '.[]' | while IFS= read -r OFFER; do
          OUTCOMES=$(echo "$OFFER" | jq -c '.outcomes[]')

          # Variables to store fighter names and odds
          FIGHTER_ONE=""
          FIGHTER_TWO=""
          ODDS_ONE=""
          ODDS_TWO=""

          # Iterate over each outcome
          echo "$OUTCOMES" | while IFS= read -r OUTCOME; do
            LABEL=$(echo "$OUTCOME" | jq -r '.label')
            ODDS_AMERICAN=$(echo "$OUTCOME" | jq -r '.oddsAmerican')

            if [ -z "$FIGHTER_ONE" ]; then
              FIGHTER_ONE="$LABEL"
              ODDS_ONE="$ODDS_AMERICAN"
            elif [ -z "$FIGHTER_TWO" ]; then
              FIGHTER_TWO="$LABEL"
              ODDS_TWO="$ODDS_AMERICAN"
            fi
          done

          # Insert data if both fighters and odds are available
          if [ -n "$FIGHTER_ONE" ] && [ -n "$FIGHTER_TWO" ] && [ -n "$ODDS_ONE" ] && [ -n "$ODDS_TWO" ]; then
            TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
            QUERY="INSERT INTO odds (event_name, fighter_one, fighter_one_odds, fighter_two, fighter_two_odds, timestamp) VALUES ('$EVENT_GROUP_NAME', '$FIGHTER_ONE', $ODDS_ONE, '$FIGHTER_TWO', $ODDS_TWO, '$TIMESTAMP');"
            mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASS" "$DB_NAME" -e "$QUERY" || echo "Failed to execute query: $QUERY"
          fi
        done
      done
    done
  done
done

# Upload JSON files via FTP
#lftp -u "mp3loader@markpereira.com,korn66!" -e "set ssl:verify-certificate no; put pfl-response.json; exit" ftp.markpereira.com
#lftp -u "mp3loader@markpereira.com,korn66!" -e "set ssl:verify-certificate no; put ufc-response.json; exit" ftp.markpereira.com
#lftp -u "mp3loader@markpereira.com,korn66!" -e "set ssl:verify-certificate no; put bellator-response.json; exit" ftp.markpereira.com
