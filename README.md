# README #



### This repository has the first draft - python specific code that will later be translated into something else - to scrape various sources and populate databases. Also it can generate some html ###

* Quick summary
* Version 0.1.0
* [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)

## How do I get set up? ##

* Clone the Repository.

* Configuration

    * For OS X Clients, have brew install mysql
    * For Unix apt install python-mysqldb
	* Have Python3 Installed 
	    sudo apt-get install python3 python3-pip
	    pip install pipenv
	* Use $ pipenv install -r requirements.txt 

* Database Configuration

	* If you would like to use a local database or your own - replace the information in each of the python files, otherwise these scripts are set up to run against the fightsToday test database. Prior to executing the inserts, I have set up a quick truncate of the tables, to empty them ahead of the run. You can comment this out or comment any line with cur.execute().  

	* Database Connection is the same in every file. you are free to use mine, with the details below - or change them to your own local or remote db.
	    * db = MySQLdb.connect(host="markpereira.com", # your host, usually localhost
	    * user="mark5463_ft_test", # your username
	    * passwd="fttesting", # your password
	    * db="mark5463_ft_testdb") # name of the data base

## Load the Data ##

* From inside python/ run the scripts in this order:
 
 Sherdog Scrapes 
 1. $ pipenv run python sherdog-event-list-scraper.py
    * This will load the database with Event Data from Sherdog.

 2. $ pipenv run python sherdog-fight-card-scrape.py
    * This will load the database with Fight Card Data from Sherdog.
    
 
 Wikipedia Scrapes 
    
 3. $ pipenv run python wikipedia-bellator-event-scrape.py
    * This will load the database with UFC Event Data from Wikipedia.
    
 3. $ pipenv run python wikipedia-ufc-event-scrape.py
    * This will load the database with UFC Event Data from Wikipedia.

 4. $ pipenv run python wikipedia-ufc-poster-scrape.py
    * This will load the database with UFC Event Poster Data from Wikipedia.
    
 5. $ pipenv run python wikipedia-fight-card-scrape.py
    * This should load the database for wikipedia fight card info
    

## Generate the HTML Page ##		
 
 6. $ pipenv run python generate-html.py > ../index.html
    This will create a file "index.html" and put it in the correct directory for it to be opened locally in Google Chrome. Unfortunately, this file needs to be encoded in utf-8. At the moment, I am doing this manually by opening the file in Sublime Text and choosing Save with Encoding UTF-8. After this has been encoded properly, index.html will render properly in Chrome, Firefox, etc.

 7. $ pipenv run python generate-ics.py 
    This creates the ICS file

### Extra Stuff thats being worked on ###		

* rss-scraper.py
	This file is getting started with putting together rss feed info. 


* Dependencies

* How to run tests
* Deployment instructions

### Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines

### Who do I talk to? ###

* realmarkp@gmail.com
* New developers welcome

### This Repository Contains: ###

* Python code written by the authors
* [AppStation Bootstrap Theme from BootstrapZero](http://www.bootstrapzero.com/bootstrap-template/appstation-app-landing-page-template)