def MY_CONTAINER
node {
    stage('Prepare node Build Environment') { // for display purposes
      // Get some code from a GitHub repository
      git 'https://github.com/futurepr0n/fightsToday.git'
      // Set up the Python Environment and dependencies  
      if (isUnix()) {
          sh 'pipenv --python 3.7 install -r requirements.txt --deploy --skip-lock'
          sh 'rm -rf index.php'
      } else {
          //put windows command here
      }        
      //##discordSend description: "Environment Prepared", footer: "futurepr0n", link: env.BUILD_URL, result: currentBuild.currentResult, image: "https://media0.giphy.com/media/XyaQAnihoZBU3GmFPl/giphy.gif", title: JOB_NAME, webhookURL: "https://discordapp.com/api/webhooks/725819926019047525/u2pGRTVXR9yCDzNnzhRgqlN4GiBgMmywTRUuyTagWQG9RmWAyDt6OSHYHWg7ObJlLVj9"
 //     discordSend description: "Environment Prepared\n" + "Duration: " + currentBuild.durationString , footer: "futurepr0n", link: env.BUILD_URL, result: currentBuild.currentResult, image: "https://media0.giphy.com/media/XyaQAnihoZBU3GmFPl/giphy.gif", title: JOB_NAME, webhookURL: "https://discordapp.com/api/webhooks/647580857242091570/tsfe5Y0YnzGqWKRrx0WiQOrpadM3OM-6pCEVIYC9DS2oNLTWtuNveJ9ZQP3agMjoEjIU"
   }
   
   stage('Startup MySQL Docker Container') { // prep the db
      // Set up the Python Environment and dependencies  
      if (isUnix()) {
         MY_CONTAINER = sh(script: 'docker run --name fightsTodayTestDB -p 3308:3306 --expose=3308 -e MYSQL_ROOT_PASSWORD="fttesting" -d mysql', returnStdout: true)
      }else{

      }
         //##discordSend description: "MySQL Container is now running..", footer: "futurepr0n", link: env.BUILD_URL, result: currentBuild.currentResult, image: "https://media0.giphy.com/media/XyaQAnihoZBU3GmFPl/giphy.gif", title: JOB_NAME, webhookURL: "https://discordapp.com/api/webhooks/725819926019047525/u2pGRTVXR9yCDzNnzhRgqlN4GiBgMmywTRUuyTagWQG9RmWAyDt6OSHYHWg7ObJlLVj9"       
   }
   stage('Prepare the fightsToday DB for loading') { // prep the db
      git 'https://github.com/futurepr0n/fightsToday.git'
      // Set up the Python Environment and dependencies  
      if (isUnix()) {
         sleep(35)
         retry(5){
            sh 'cat sql/fights_today_setup.sql | docker exec -i fightsTodayTestDB mysql --port=3308 -u root --password=fttesting'
         }
             
         }else{

      }
         //##discordSend description: "DB Staged and Prepared for Loading..", footer: "futurepr0n", link: env.BUILD_URL, result: currentBuild.currentResult, image: "https://media0.giphy.com/media/XyaQAnihoZBU3GmFPl/giphy.gif", title: JOB_NAME, webhookURL: "https://discordapp.com/api/webhooks/725819926019047525/u2pGRTVXR9yCDzNnzhRgqlN4GiBgMmywTRUuyTagWQG9RmWAyDt6OSHYHWg7ObJlLVj9"       
   }
   //stage('Sherdog Events Scrape') {
      // Run the build
   //      if (isUnix()) {
   //         sh 'pipenv run python python/sherdog-event-list-scraper.py'
   //      } else { //Run in windows
            //bat(/"python stuff here"/)
   //      }
   //      discordSend description: "Sherdog Events Scraped", footer: "futurepr0n", link: env.BUILD_URL, result: currentBuild.currentResult, image: "https://cdn1-www-forums.sherdog.com/data/avatars/l/569/569875.jpg?1580282612", title: JOB_NAME, webhookURL: "https://discordapp.com/api/webhooks/725819926019047525/u2pGRTVXR9yCDzNnzhRgqlN4GiBgMmywTRUuyTagWQG9RmWAyDt6OSHYHWg7ObJlLVj9"
   //      discordSend description: "Sherdog Events Scraped", footer: "futurepr0n", link: env.BUILD_URL, result: currentBuild.currentResult, image: "https://cdn1-www-forums.sherdog.com/data/avatars/l/569/569875.jpg?1580282612", title: JOB_NAME, webhookURL: "https://discordapp.com/api/webhooks/647580857242091570/tsfe5Y0YnzGqWKRrx0WiQOrpadM3OM-6pCEVIYC9DS2oNLTWtuNveJ9ZQP3agMjoEjIU"
   //}
   //stage('Sherdog Fight Cards Scrape') {
      // Run the build
   //      if (isUnix()) {
   //          sh 'pipenv run python python/sherdog-fight-card-scrape.py'
   //      } else { //Run in windows
            //bat(/"python stuff here"/)
   //      }
   //      discordSend description: "Sherdog Fight Cards Scraped", footer: "futurepr0n", link: env.BUILD_URL, result: currentBuild.currentResult, image: "https://cdn1-www-forums.sherdog.com/data/avatars/l/569/569875.jpg?1580282612", title: JOB_NAME, webhookURL: "https://discordapp.com/api/webhooks/725819926019047525/u2pGRTVXR9yCDzNnzhRgqlN4GiBgMmywTRUuyTagWQG9RmWAyDt6OSHYHWg7ObJlLVj9"
//         discordSend description: "Sherdog Fight Cards Scraped", footer: "futurepr0n", link: env.BUILD_URL, result: currentBuild.currentResult, image: "https://cdn1-www-forums.sherdog.com/data/avatars/l/569/569875.jpg?1580282612", title: JOB_NAME, webhookURL: "https://discordapp.com/api/webhooks/647580857242091570/tsfe5Y0YnzGqWKRrx0WiQOrpadM3OM-6pCEVIYC9DS2oNLTWtuNveJ9ZQP3agMjoEjIU"
   //}
   stage('Wikipedia Bellator Events Scrape') {
      steps {
         withCredentials([
               string(credentialsId: 'MYSQL_USER', variable: 'MYSQL_USER'),
               string(credentialsId: 'MYSQL_PASSWORD', variable: 'MYSQL_PASSWORD'),
               string(credentialsId: 'MYSQL_HOST', variable: 'MYSQL_HOST')
         ]) {
               script {
                  if (isUnix()) {
                     sh '''
                           export MYSQL_USER="${MYSQL_USER}"
                           export MYSQL_PASSWORD="${MYSQL_PASSWORD}"
                           export MYSQL_HOST="${MYSQL_HOST}"
                           pipenv run python python/wikipedia-bellator-event-scrape.py
                     '''
                  } else {
                     bat '''
                           set MYSQL_USER=%MYSQL_USER%
                           set MYSQL_PASSWORD=%MYSQL_PASSWORD%
                           set MYSQL_HOST=%MYSQL_HOST%
                           pipenv run python python/wikipedia-bellator-event-scrape.py
                     '''
                  }
               }
         }
      }
   }

   stage('Wikipedia UFC Events Scrape') {
      steps {
         withCredentials([
               string(credentialsId: 'MYSQL_USER', variable: 'MYSQL_USER'),
               string(credentialsId: 'MYSQL_PASSWORD', variable: 'MYSQL_PASSWORD'),
               string(credentialsId: 'MYSQL_HOST', variable: 'MYSQL_HOST')
         ]) {
               script {
                  if (isUnix()) {
                     sh '''
                           export MYSQL_USER="${MYSQL_USER}"
                           export MYSQL_PASSWORD="${MYSQL_PASSWORD}"
                           export MYSQL_HOST="${MYSQL_HOST}"
                           pipenv run python python/wikipedia-ufc-event-scrape.py
                     '''
                  } else {
                     bat '''
                           set MYSQL_USER=%MYSQL_USER%
                           set MYSQL_PASSWORD=%MYSQL_PASSWORD%
                           set MYSQL_HOST=%MYSQL_HOST%
                           pipenv run python python/wikipedia-ufc-event-scrape.py
                     '''
                  }
               }
         }
      }
   }
   stage('Wikipedia Bellator Posters Scrape') {
      steps {
         withCredentials([
               string(credentialsId: 'MYSQL_USER', variable: 'MYSQL_USER'),
               string(credentialsId: 'MYSQL_PASSWORD', variable: 'MYSQL_PASSWORD'),
               string(credentialsId: 'MYSQL_HOST', variable: 'MYSQL_HOST')
         ]) {
               script {
                  if (isUnix()) {
                     sh '''
                           export MYSQL_USER="${MYSQL_USER}"
                           export MYSQL_PASSWORD="${MYSQL_PASSWORD}"
                           export MYSQL_HOST="${MYSQL_HOST}"
                           pipenv run python python/wikipedia-bellator-poster-scrape.py
                     '''
                  } else {
                     bat '''
                           set MYSQL_USER=%MYSQL_USER%
                           set MYSQL_PASSWORD=%MYSQL_PASSWORD%
                           set MYSQL_HOST=%MYSQL_HOST%
                           pipenv run python python/wikipedia-bellator-poster-scrape.py
                     '''
                  }
               }
         }
      }
   }
   stage('Wikipedia UFC Posters Scrape') {
      steps {
         withCredentials([
               string(credentialsId: 'MYSQL_USER', variable: 'MYSQL_USER'),
               string(credentialsId: 'MYSQL_PASSWORD', variable: 'MYSQL_PASSWORD'),
               string(credentialsId: 'MYSQL_HOST', variable: 'MYSQL_HOST')
         ]) {
               script {
                  if (isUnix()) {
                     sh '''
                           export MYSQL_USER="${MYSQL_USER}"
                           export MYSQL_PASSWORD="${MYSQL_PASSWORD}"
                           export MYSQL_HOST="${MYSQL_HOST}"
                           pipenv run python python/wikipedia-ufc-poster-scrape.py
                     '''
                  } else {
                     bat '''
                           set MYSQL_USER=%MYSQL_USER%
                           set MYSQL_PASSWORD=%MYSQL_PASSWORD%
                           set MYSQL_HOST=%MYSQL_HOST%
                           pipenv run python python/wikipedia-ufc-poster-scrape.py
                     '''
                  }
               }
         }
      }
   }
   stage('Wikipedia Fight Cards Scrape') {
      steps {
         withCredentials([
               string(credentialsId: 'MYSQL_USER', variable: 'MYSQL_USER'),
               string(credentialsId: 'MYSQL_PASSWORD', variable: 'MYSQL_PASSWORD'),
               string(credentialsId: 'MYSQL_HOST', variable: 'MYSQL_HOST')
         ]) {
               script {
                  if (isUnix()) {
                     sh '''
                           export MYSQL_USER="${MYSQL_USER}"
                           export MYSQL_PASSWORD="${MYSQL_PASSWORD}"
                           export MYSQL_HOST="${MYSQL_HOST}"
                           pipenv run python python/wikipedia-fight-card-scrape.py
                     '''
                  } else {
                     bat '''
                           set MYSQL_USER=%MYSQL_USER%
                           set MYSQL_PASSWORD=%MYSQL_PASSWORD%
                           set MYSQL_HOST=%MYSQL_HOST%
                           pipenv run python python/wikipedia-fight-card-scrape.py
                     '''
                  }
               }
         }
      }
   }
   stage('Wikipedia Ultimate Fighter Fight Cards Scrape') {
      steps {
         withCredentials([
               string(credentialsId: 'MYSQL_USER', variable: 'MYSQL_USER'),
               string(credentialsId: 'MYSQL_PASSWORD', variable: 'MYSQL_PASSWORD'),
               string(credentialsId: 'MYSQL_HOST', variable: 'MYSQL_HOST')
         ]) {
               script {
                  if (isUnix()) {
                     sh '''
                           export MYSQL_USER="${MYSQL_USER}"
                           export MYSQL_PASSWORD="${MYSQL_PASSWORD}"
                           export MYSQL_HOST="${MYSQL_HOST}"
                           pipenv run python python/wiki_fight_card_scrape_ultimate_fighter.py
                     '''
                  } else {
                     bat '''
                           set MYSQL_USER=%MYSQL_USER%
                           set MYSQL_PASSWORD=%MYSQL_PASSWORD%
                           set MYSQL_HOST=%MYSQL_HOST%
                           pipenv run python python/wiki_fight_card_scrape_ultimate_fighter.py
                     '''
                  }
               }
         }
      }
   }
   stage('Wikipedia Ultimate Fighter Fight Cards Scrape Part 2') {
      steps {
         withCredentials([
               string(credentialsId: 'MYSQL_USER', variable: 'MYSQL_USER'),
               string(credentialsId: 'MYSQL_PASSWORD', variable: 'MYSQL_PASSWORD'),
               string(credentialsId: 'MYSQL_HOST', variable: 'MYSQL_HOST')
         ]) {
               script {
                  if (isUnix()) {
                     sh '''
                           export MYSQL_USER="${MYSQL_USER}"
                           export MYSQL_PASSWORD="${MYSQL_PASSWORD}"
                           export MYSQL_HOST="${MYSQL_HOST}"
                           pipenv run python python/wiki_fight_card_scrape_ultimate_fighter_2.py
                     '''
                  } else {
                     bat '''
                           set MYSQL_USER=%MYSQL_USER%
                           set MYSQL_PASSWORD=%MYSQL_PASSWORD%
                           set MYSQL_HOST=%MYSQL_HOST%
                           pipenv run python python/wiki_fight_card_scrape_ultimate_fighter_2.py
                     '''
                  }
               }
         }
      }
      //         discordSend description: "Wikipedia Fight Cards Scraped", footer: "futurepr0n", link: env.BUILD_URL, result: currentBuild.currentResult, image: "https://upload.wikimedia.org/wikipedia/commons/7/7a/Nohat-wiki-logo.png", title: JOB_NAME, webhookURL: "https://discordapp.com/api/webhooks/647580857242091570/tsfe5Y0YnzGqWKRrx0WiQOrpadM3OM-6pCEVIYC9DS2oNLTWtuNveJ9ZQP3agMjoEjIU"
   }
   stage('Wikipedia Ultimate Fighter Fight Cards Scrape Part 3') {
      steps {
         withCredentials([
               string(credentialsId: 'MYSQL_USER', variable: 'MYSQL_USER'),
               string(credentialsId: 'MYSQL_PASSWORD', variable: 'MYSQL_PASSWORD'),
               string(credentialsId: 'MYSQL_HOST', variable: 'MYSQL_HOST')
         ]) {
               script {
                  if (isUnix()) {
                     sh '''
                           export MYSQL_USER="${MYSQL_USER}"
                           export MYSQL_PASSWORD="${MYSQL_PASSWORD}"
                           export MYSQL_HOST="${MYSQL_HOST}"
                           pipenv run python python/wiki_fight_card_scrape_ultimate_fighter_3.py
                     '''
                  } else {
                     bat '''
                           set MYSQL_USER=%MYSQL_USER%
                           set MYSQL_PASSWORD=%MYSQL_PASSWORD%
                           set MYSQL_HOST=%MYSQL_HOST%
                           pipenv run python python/wiki_fight_card_scrape_ultimate_fighter_3.py
                     '''
                  }
               }
         }
      }
      //         discordSend description: "Wikipedia Fight Cards Scraped", footer: "futurepr0n", link: env.BUILD_URL, result: currentBuild.currentResult, image: "https://upload.wikimedia.org/wikipedia/commons/7/7a/Nohat-wiki-logo.png", title: JOB_NAME, webhookURL: "https://discordapp.com/api/webhooks/647580857242091570/tsfe5Y0YnzGqWKRrx0WiQOrpadM3OM-6pCEVIYC9DS2oNLTWtuNveJ9ZQP3agMjoEjIU"
   }
   stage('Wikipedia Bellator Fight Cards Scrape part 1') {
      steps {
         withCredentials([
               string(credentialsId: 'MYSQL_USER', variable: 'MYSQL_USER'),
               string(credentialsId: 'MYSQL_PASSWORD', variable: 'MYSQL_PASSWORD'),
               string(credentialsId: 'MYSQL_HOST', variable: 'MYSQL_HOST')
         ]) {
               script {
                  if (isUnix()) {
                     sh '''
                           export MYSQL_USER="${MYSQL_USER}"
                           export MYSQL_PASSWORD="${MYSQL_PASSWORD}"
                           export MYSQL_HOST="${MYSQL_HOST}"
                           pipenv run python python/wikipedia_bellator_fight_card_scrape.py
                     '''
                  } else {
                     bat '''
                           set MYSQL_USER=%MYSQL_USER%
                           set MYSQL_PASSWORD=%MYSQL_PASSWORD%
                           set MYSQL_HOST=%MYSQL_HOST%
                           pipenv run python python/wikipedia_bellator_fight_card_scrape.py
                     '''
                  }
               }
         }
      }
      //         discordSend description: "Wikipedia Fight Cards Scraped", footer: "futurepr0n", link: env.BUILD_URL, result: currentBuild.currentResult, image: "https://upload.wikimedia.org/wikipedia/commons/7/7a/Nohat-wiki-logo.png", title: JOB_NAME, webhookURL: "https://discordapp.com/api/webhooks/647580857242091570/tsfe5Y0YnzGqWKRrx0WiQOrpadM3OM-6pCEVIYC9DS2oNLTWtuNveJ9ZQP3agMjoEjIU"
   }
   stage('Wikipedia Bellator Fight Cards Scrape part 2') {
      steps {
         withCredentials([
               string(credentialsId: 'MYSQL_USER', variable: 'MYSQL_USER'),
               string(credentialsId: 'MYSQL_PASSWORD', variable: 'MYSQL_PASSWORD'),
               string(credentialsId: 'MYSQL_HOST', variable: 'MYSQL_HOST')
         ]) {
               script {
                  if (isUnix()) {
                     sh '''
                           export MYSQL_USER="${MYSQL_USER}"
                           export MYSQL_PASSWORD="${MYSQL_PASSWORD}"
                           export MYSQL_HOST="${MYSQL_HOST}"
                           pipenv run python python/wikipedia_bellator_fight_card_scrape2.py
                     '''
                  } else {
                     bat '''
                           set MYSQL_USER=%MYSQL_USER%
                           set MYSQL_PASSWORD=%MYSQL_PASSWORD%
                           set MYSQL_HOST=%MYSQL_HOST%
                           pipenv run python python/wikipedia_bellator_fight_card_scrape2.py
                     '''
                  }
               }
         }
      }
      //         discordSend description: "Wikipedia Fight Cards Scraped", footer: "futurepr0n", link: env.BUILD_URL, result: currentBuild.currentResult, image: "https://upload.wikimedia.org/wikipedia/commons/7/7a/Nohat-wiki-logo.png", title: JOB_NAME, webhookURL: "https://discordapp.com/api/webhooks/647580857242091570/tsfe5Y0YnzGqWKRrx0WiQOrpadM3OM-6pCEVIYC9DS2oNLTWtuNveJ9ZQP3agMjoEjIU"
   }
   stage('Build HTML Page') {
      steps {
         withCredentials([
               string(credentialsId: 'MYSQL_USER', variable: 'MYSQL_USER'),
               string(credentialsId: 'MYSQL_PASSWORD', variable: 'MYSQL_PASSWORD'),
               string(credentialsId: 'MYSQL_HOST', variable: 'MYSQL_HOST')
         ]) {
               script {
                  if (isUnix()) {
                     sh '''
                           export MYSQL_USER="${MYSQL_USER}"
                           export MYSQL_PASSWORD="${MYSQL_PASSWORD}"
                           export MYSQL_HOST="${MYSQL_HOST}"
                           pipenv run python python/generate-html.py
                     '''
                  } else {
                     bat '''
                           set MYSQL_USER=%MYSQL_USER%
                           set MYSQL_PASSWORD=%MYSQL_PASSWORD%
                           set MYSQL_HOST=%MYSQL_HOST%
                           pipenv run python python/generate-html.py
                     '''
                  }
               }
         }
      }
      //         discordSend description: "Wikipedia Fight Cards Scraped", footer: "futurepr0n", link: env.BUILD_URL, result: currentBuild.currentResult, image: "https://upload.wikimedia.org/wikipedia/commons/7/7a/Nohat-wiki-logo.png", title: JOB_NAME, webhookURL: "https://discordapp.com/api/webhooks/647580857242091570/tsfe5Y0YnzGqWKRrx0WiQOrpadM3OM-6pCEVIYC9DS2oNLTWtuNveJ9ZQP3agMjoEjIU"
   }
   stage('Build ICS File') {
      steps {
         withCredentials([
               string(credentialsId: 'MYSQL_USER', variable: 'MYSQL_USER'),
               string(credentialsId: 'MYSQL_PASSWORD', variable: 'MYSQL_PASSWORD'),
               string(credentialsId: 'MYSQL_HOST', variable: 'MYSQL_HOST')
         ]) {
               script {
                  if (isUnix()) {
                     sh '''
                           export MYSQL_USER="${MYSQL_USER}"
                           export MYSQL_PASSWORD="${MYSQL_PASSWORD}"
                           export MYSQL_HOST="${MYSQL_HOST}"
                           pipenv run python python/generate-ics.py
                     '''
                  } else {
                     bat '''
                           set MYSQL_USER=%MYSQL_USER%
                           set MYSQL_PASSWORD=%MYSQL_PASSWORD%
                           set MYSQL_HOST=%MYSQL_HOST%
                           pipenv run python python/generate-ics.py
                     '''
                  }
               }
         }
      }
      //         discordSend description: "Wikipedia Fight Cards Scraped", footer: "futurepr0n", link: env.BUILD_URL, result: currentBuild.currentResult, image: "https://upload.wikimedia.org/wikipedia/commons/7/7a/Nohat-wiki-logo.png", title: JOB_NAME, webhookURL: "https://discordapp.com/api/webhooks/647580857242091570/tsfe5Y0YnzGqWKRrx0WiQOrpadM3OM-6pCEVIYC9DS2oNLTWtuNveJ9ZQP3agMjoEjIU"
   }
   stage('Upload To Server') {
      steps {
         withCredentials([
               string(credentialsId: 'MYSQL_USER', variable: 'MYSQL_USER'),
               string(credentialsId: 'MYSQL_PASSWORD', variable: 'MYSQL_PASSWORD'),
               string(credentialsId: 'MYSQL_HOST', variable: 'MYSQL_HOST')
         ]) {
               script {
                  if (isUnix()) {
                     sh '''
                           export FightsTodayFTPID="${FightsTodayFTPID}"
                           export FightsTodayFTPPass="${FightsTodayFTPPass}"
                           pipenv run python python/generate-ics.py
                     '''
                  } else {
                     bat '''
                           set FightsTodayFTPID=%FightsTodayFTPID%
                           set FightsTodayFTPPass=%FightsTodayFTPPass%
                           pipenv run python python/upload-files.py
                     '''
                  }
               }
         }
      }
      //         discordSend description: "Wikipedia Fight Cards Scraped", footer: "futurepr0n", link: env.BUILD_URL, result: currentBuild.currentResult, image: "https://upload.wikimedia.org/wikipedia/commons/7/7a/Nohat-wiki-logo.png", title: JOB_NAME, webhookURL: "https://discordapp.com/api/webhooks/647580857242091570/tsfe5Y0YnzGqWKRrx0WiQOrpadM3OM-6pCEVIYC9DS2oNLTWtuNveJ9ZQP3agMjoEjIU"
   } 
   stage('Delete and Remove the MySQL Container') { // prep the db
      // Set up the Python Environment and dependencies  
      println(MY_CONTAINER)
      echo MY_CONTAINER
      if (isUnix()) {
            sh 'docker kill ' + MY_CONTAINER 
            sh 'docker rm ' + MY_CONTAINER
         }else{
         
      }
         //#discordSend description: "Docker Container has been Killed & Removed..", footer: "futurepr0n", link: env.BUILD_URL, result: currentBuild.currentResult, image: "https://media0.giphy.com/media/XyaQAnihoZBU3GmFPl/giphy.gif", title: JOB_NAME, webhookURL: "https://discordapp.com/api/webhooks/725819926019047525/u2pGRTVXR9yCDzNnzhRgqlN4GiBgMmywTRUuyTagWQG9RmWAyDt6OSHYHWg7ObJlLVj9"       
   } 
}
