node {
   stage('Prepare node Build Environment') { // for display purposes
      // Get some code from a GitHub repository
      git 'https://github.com/futurepr0n/fightsToday.git'
      // Set up the Python Environment and dependencies  
      if (isUnix()) {
          sh 'pipenv --python 3.7 install -r requirements.txt --deploy --skip-lock'
          sh 'rm -rf index.html'
      } else {
          //put windows command here
      }        
      discordSend description: "Environment Prepared", footer: "futurepr0n", link: env.BUILD_URL, result: currentBuild.currentResult, image: "https://media0.giphy.com/media/XyaQAnihoZBU3GmFPl/giphy.gif", title: JOB_NAME, webhookURL: "https://discordapp.com/api/webhooks/725819926019047525/u2pGRTVXR9yCDzNnzhRgqlN4GiBgMmywTRUuyTagWQG9RmWAyDt6OSHYHWg7ObJlLVj9"
 //     discordSend description: "Environment Prepared\n" + "Duration: " + currentBuild.durationString , footer: "futurepr0n", link: env.BUILD_URL, result: currentBuild.currentResult, image: "https://media0.giphy.com/media/XyaQAnihoZBU3GmFPl/giphy.gif", title: JOB_NAME, webhookURL: "https://discordapp.com/api/webhooks/647580857242091570/tsfe5Y0YnzGqWKRrx0WiQOrpadM3OM-6pCEVIYC9DS2oNLTWtuNveJ9ZQP3agMjoEjIU"
   }
   stage('startup mysql docker container') { // prep the db
      step{
      // Set up the Python Environment and dependencies  
      if (isUnix()) {
         sh 'docker run --name fightsTodayTestDB -p 3308:3306 --expose=3308 -e MYSQL_ROOT_PASSWORD="fttesting" -d mysql'
      }else{

      }
        // docker.image('mysql').withRun('-v `$PWD`:`$PWD` --name fightsTodayTestDB -p 3308:3306 --expose=3308 -e MYSQL_ROOT_PASSWORD="fttesting" -d') {c -> 
        //    sh 'docker exec -i fightsTodayTestDB service mysql start'
        //    sh 'cat sql/fights_today_setup.sql | docker exec -i fightsTodayTestDB mysql -u root --password=fttesting'
        // }
      
         discordSend description: "mysql Container Started", footer: "futurepr0n", link: env.BUILD_URL, result: currentBuild.currentResult, image: "https://media0.giphy.com/media/XyaQAnihoZBU3GmFPl/giphy.gif", title: JOB_NAME, webhookURL: "https://discordapp.com/api/webhooks/725819926019047525/u2pGRTVXR9yCDzNnzhRgqlN4GiBgMmywTRUuyTagWQG9RmWAyDt6OSHYHWg7ObJlLVj9"       
      }
   
      step { // prep the db
      // Set up the Python Environment and dependencies  
      if (isUnix()) {
         sh 'cat sql/fights_today_setup.sql | docker exec -i fightsTodayTestDB mysql -u root --password=fttesting mark5436_ft_prod'
      }else{

      }
        // docker.image('mysql').withRun('-v `$PWD`:`$PWD` --name fightsTodayTestDB -p 3308:3306 --expose=3308 -e MYSQL_ROOT_PASSWORD="fttesting" -d') {c -> 
        //    sh 'docker exec -i fightsTodayTestDB service mysql start'
        //    sh 'cat sql/fights_today_setup.sql | docker exec -i fightsTodayTestDB mysql -u root --password=fttesting'
        // }
      
      discordSend description: "mysql db prepared", footer: "futurepr0n", link: env.BUILD_URL, result: currentBuild.currentResult, image: "https://media0.giphy.com/media/XyaQAnihoZBU3GmFPl/giphy.gif", title: JOB_NAME, webhookURL: "https://discordapp.com/api/webhooks/725819926019047525/u2pGRTVXR9yCDzNnzhRgqlN4GiBgMmywTRUuyTagWQG9RmWAyDt6OSHYHWg7ObJlLVj9"       
   }
   stage('Sherdog Events Scrape') {
      // Run the build
         if (isUnix()) {
            sh 'pipenv run python python/sherdog-event-list-scraper.py'
         } else { //Run in windows
            //bat(/"python stuff here"/)
         }
         discordSend description: "Sherdog Events Scraped", footer: "futurepr0n", link: env.BUILD_URL, result: currentBuild.currentResult, image: "https://cdn1-www-forums.sherdog.com/data/avatars/l/569/569875.jpg?1580282612", title: JOB_NAME, webhookURL: "https://discordapp.com/api/webhooks/725819926019047525/u2pGRTVXR9yCDzNnzhRgqlN4GiBgMmywTRUuyTagWQG9RmWAyDt6OSHYHWg7ObJlLVj9"
   //      discordSend description: "Sherdog Events Scraped", footer: "futurepr0n", link: env.BUILD_URL, result: currentBuild.currentResult, image: "https://cdn1-www-forums.sherdog.com/data/avatars/l/569/569875.jpg?1580282612", title: JOB_NAME, webhookURL: "https://discordapp.com/api/webhooks/647580857242091570/tsfe5Y0YnzGqWKRrx0WiQOrpadM3OM-6pCEVIYC9DS2oNLTWtuNveJ9ZQP3agMjoEjIU"
      }
   stage('Sherdog Fight Cards Scrape') {
      // Run the build
         if (isUnix()) {
             sh 'pipenv run python python/sherdog-fight-card-scrape.py'
         } else { //Run in windows
            //bat(/"python stuff here"/)
         }
         discordSend description: "Sherdog Fight Cards Scraped", footer: "futurepr0n", link: env.BUILD_URL, result: currentBuild.currentResult, image: "https://cdn1-www-forums.sherdog.com/data/avatars/l/569/569875.jpg?1580282612", title: JOB_NAME, webhookURL: "https://discordapp.com/api/webhooks/725819926019047525/u2pGRTVXR9yCDzNnzhRgqlN4GiBgMmywTRUuyTagWQG9RmWAyDt6OSHYHWg7ObJlLVj9"
//         discordSend description: "Sherdog Fight Cards Scraped", footer: "futurepr0n", link: env.BUILD_URL, result: currentBuild.currentResult, image: "https://cdn1-www-forums.sherdog.com/data/avatars/l/569/569875.jpg?1580282612", title: JOB_NAME, webhookURL: "https://discordapp.com/api/webhooks/647580857242091570/tsfe5Y0YnzGqWKRrx0WiQOrpadM3OM-6pCEVIYC9DS2oNLTWtuNveJ9ZQP3agMjoEjIU"
      }
   stage('Wikipedia Bellator Events Scrape') {
      // Run the build
         if (isUnix()) {
            sh 'pipenv run python python/wikipedia-bellator-event-scrape.py'
         } else { //Run in windows
            //bat(/"python stuff here"/)
         }
         discordSend description: "Wikipedia Bellator Events Scraped", footer: "futurepr0n", link: env.BUILD_URL, result: currentBuild.currentResult, image: "https://upload.wikimedia.org/wikipedia/commons/7/7a/Nohat-wiki-logo.png", title: JOB_NAME, webhookURL: "https://discordapp.com/api/webhooks/725819926019047525/u2pGRTVXR9yCDzNnzhRgqlN4GiBgMmywTRUuyTagWQG9RmWAyDt6OSHYHWg7ObJlLVj9"
//         discordSend description: "Wikipedia Bellator Events Scraped", footer: "futurepr0n", link: env.BUILD_URL, result: currentBuild.currentResult, image: "https://upload.wikimedia.org/wikipedia/commons/7/7a/Nohat-wiki-logo.png", title: JOB_NAME, webhookURL: "https://discordapp.com/api/webhooks/647580857242091570/tsfe5Y0YnzGqWKRrx0WiQOrpadM3OM-6pCEVIYC9DS2oNLTWtuNveJ9ZQP3agMjoEjIU"
      }
   stage('Wikipedia UFC Events Scrape') {
      // Run the build
         if (isUnix()) {
            sh 'pipenv run python python/wikipedia-ufc-event-scrape.py'
         } else { //Run in windows
            //bat(/"python stuff here"/)
         }
         discordSend description: "Wikipedia UFC Events Scraped", footer: "futurepr0n", link: env.BUILD_URL, result: currentBuild.currentResult, image: "https://upload.wikimedia.org/wikipedia/commons/7/7a/Nohat-wiki-logo.png", title: JOB_NAME, webhookURL: "https://discordapp.com/api/webhooks/725819926019047525/u2pGRTVXR9yCDzNnzhRgqlN4GiBgMmywTRUuyTagWQG9RmWAyDt6OSHYHWg7ObJlLVj9"
//         discordSend description: "Wikipedia UFC Events Scraped", footer: "futurepr0n", link: env.BUILD_URL, result: currentBuild.currentResult, image: "https://upload.wikimedia.org/wikipedia/commons/7/7a/Nohat-wiki-logo.png", title: JOB_NAME, webhookURL: "https://discordapp.com/api/webhooks/647580857242091570/tsfe5Y0YnzGqWKRrx0WiQOrpadM3OM-6pCEVIYC9DS2oNLTWtuNveJ9ZQP3agMjoEjIU"
      }
   stage('Wikipedia UFC Posters Scrape') {
      // Run the build
         if (isUnix()) {
            sh 'pipenv run python python/wikipedia-ufc-poster-scrape.py'
         } else { //Run in windows
            //bat(/"python stuff here"/)
         }
         discordSend description: "Wikipedia UFC Posters Scraped", footer: "futurepr0n", link: env.BUILD_URL, result: currentBuild.currentResult, image: "https://upload.wikimedia.org/wikipedia/commons/7/7a/Nohat-wiki-logo.png", title: JOB_NAME, webhookURL: "https://discordapp.com/api/webhooks/725819926019047525/u2pGRTVXR9yCDzNnzhRgqlN4GiBgMmywTRUuyTagWQG9RmWAyDt6OSHYHWg7ObJlLVj9"
//         discordSend description: "Wikipedia UFC Posters Scraped", footer: "futurepr0n", link: env.BUILD_URL, result: currentBuild.currentResult, image: "https://upload.wikimedia.org/wikipedia/commons/7/7a/Nohat-wiki-logo.png", title: JOB_NAME, webhookURL: "https://discordapp.com/api/webhooks/647580857242091570/tsfe5Y0YnzGqWKRrx0WiQOrpadM3OM-6pCEVIYC9DS2oNLTWtuNveJ9ZQP3agMjoEjIU"
      }
   stage('Wikipedia Fight Cards Scrape') {
      // Run the build
         if (isUnix()) {
            sh 'pipenv run python python/wikipedia-fight-card-scrape.py'
         } else { //Run in windows
            //bat(/"python stuff here"/)
         }
         discordSend description: "Wikipedia Fight Cards Scraped", footer: "futurepr0n", link: env.BUILD_URL, result: currentBuild.currentResult, image: "https://upload.wikimedia.org/wikipedia/commons/7/7a/Nohat-wiki-logo.png", title: JOB_NAME, webhookURL: "https://discordapp.com/api/webhooks/725819926019047525/u2pGRTVXR9yCDzNnzhRgqlN4GiBgMmywTRUuyTagWQG9RmWAyDt6OSHYHWg7ObJlLVj9"
//         discordSend description: "Wikipedia Fight Cards Scraped", footer: "futurepr0n", link: env.BUILD_URL, result: currentBuild.currentResult, image: "https://upload.wikimedia.org/wikipedia/commons/7/7a/Nohat-wiki-logo.png", title: JOB_NAME, webhookURL: "https://discordapp.com/api/webhooks/647580857242091570/tsfe5Y0YnzGqWKRrx0WiQOrpadM3OM-6pCEVIYC9DS2oNLTWtuNveJ9ZQP3agMjoEjIU"
      }
   stage('Build HTML Page') {
      // Run the build
         if (isUnix()) {
            sh 'pipenv run python python/generate-html.py'
         } else { //Run in windows
            //bat(/"python stuff here"/)
         }
         discordSend description: "WebPage Built", footer: "futurepr0n", link: env.BUILD_URL, result: currentBuild.currentResult, image: "https://media3.giphy.com/media/l3vRfNA1p0rvhMSvS/200.gif", title: JOB_NAME, webhookURL: "https://discordapp.com/api/webhooks/725819926019047525/u2pGRTVXR9yCDzNnzhRgqlN4GiBgMmywTRUuyTagWQG9RmWAyDt6OSHYHWg7ObJlLVj9"
//        discordSend description: "WebPage Built", footer: "futurepr0n", link: env.BUILD_URL, result: currentBuild.currentResult, image: "https://media3.giphy.com/media/l3vRfNA1p0rvhMSvS/200.gif", title: JOB_NAME, webhookURL: "https://discordapp.com/api/webhooks/647580857242091570/tsfe5Y0YnzGqWKRrx0WiQOrpadM3OM-6pCEVIYC9DS2oNLTWtuNveJ9ZQP3agMjoEjIU"
      }
   stage('Build ICS File') {
      // Run the build
         if (isUnix()) {
            sh 'pipenv run python python/generate-ics.py'
         } else { //Run in windows
            //bat(/"python stuff here"/)
         }
         discordSend description: "iCal Built", footer: "futurepr0n", link: env.BUILD_URL, result: currentBuild.currentResult, image: "https://www.assetworks.com/wp-content/uploads/2018/11/Calendar-GIF-240p-8d6f3eae-a7fa-4497-bbad-28b1e76d64d0.gif", title: JOB_NAME, webhookURL: "https://discordapp.com/api/webhooks/725819926019047525/u2pGRTVXR9yCDzNnzhRgqlN4GiBgMmywTRUuyTagWQG9RmWAyDt6OSHYHWg7ObJlLVj9"
//         discordSend description: "iCal Built", footer: "futurepr0n", link: env.BUILD_URL, result: currentBuild.currentResult, image: "https://www.assetworks.com/wp-content/uploads/2018/11/Calendar-GIF-240p-8d6f3eae-a7fa-4497-bbad-28b1e76d64d0.gif", title: JOB_NAME, webhookURL: "https://discordapp.com/api/webhooks/647580857242091570/tsfe5Y0YnzGqWKRrx0WiQOrpadM3OM-6pCEVIYC9DS2oNLTWtuNveJ9ZQP3agMjoEjIU"
      }
   stage('Upload To Server') {
      sh 'pipenv run python python/upload-files.py'
      //discordSend description: 'Everything looks great!', footer: '', image: 'https://media1.tenor.com/images/32457dbd5788a0b907d356ce16cbaba5/tenor.gif?itemid=4950041', link: 'env.BUILD_URL', result: 'SUCCESS', thumbnail: '', title: 'env.JOB_NAME', webhookURL: 'https://discordapp.com/api/webhooks/725819926019047525/u2pGRTVXR9yCDzNnzhRgqlN4GiBgMmywTRUuyTagWQG9RmWAyDt6OSHYHWg7ObJlLVj9'
      discordSend description: "Jenkins Build", footer: "futurepr0n", link: env.BUILD_URL, result: currentBuild.currentResult,image: "https://media1.tenor.com/images/32457dbd5788a0b907d356ce16cbaba5/tenor.gif?itemid=4950041", title: JOB_NAME, webhookURL: "https://discordapp.com/api/webhooks/725819926019047525/u2pGRTVXR9yCDzNnzhRgqlN4GiBgMmywTRUuyTagWQG9RmWAyDt6OSHYHWg7ObJlLVj9"
//      discordSend description: "Jenkins Build", footer: "futurepr0n", link: env.BUILD_URL, result: currentBuild.currentResult,image: "https://media1.tenor.com/images/32457dbd5788a0b907d356ce16cbaba5/tenor.gif?itemid=4950041", title: JOB_NAME, webhookURL: "https://discordapp.com/api/webhooks/647580857242091570/tsfe5Y0YnzGqWKRrx0WiQOrpadM3OM-6pCEVIYC9DS2oNLTWtuNveJ9ZQP3agMjoEjIU"

   }
}
