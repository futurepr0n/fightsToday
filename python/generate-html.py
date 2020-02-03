##################
# FILE HAS BEEN TESTED Not SUCCESSFULLY
#

from lxml import html, etree
import io
from django.utils.encoding import smart_str, smart_text
from pyquery import PyQuery as pq
from datetime import datetime
import re
import calendar
import time
import sys
import requests
import MySQLdb


def urlify(s):
    # Remove all non-word characters (everything except numbers and letters)
    s = re.sub(r"[^\w\s]", '', s)

    # Replace all runs of whitespace with a plus
    s = re.sub(r"\s+", '+', s)

    return s


def dateify(s):
    # Remove all non-word characters (everything except numbers and letters)
    s = re.sub(r"[^\w\s]", '', s)

    # Remove the year
    # s = re.sub(r"2016", '', s)
    s = re.sub(r"2016", '', s)
    s = re.sub(r"2017", '', s)
    s = re.sub(r"2018", '', s)
    s = re.sub(r"2019", '', s)
    s = re.sub(r"2020", '', s)

    s = re.sub(r"Jan", '01', s)
    s = re.sub(r"Feb", '02', s)
    s = re.sub(r"Mar", '03', s)
    s = re.sub(r"Apr", '04', s)
    s = re.sub(r"May", '05', s)
    s = re.sub(r"Jun", '06', s)
    s = re.sub(r"Jul", '07', s)
    s = re.sub(r"Aug", '08', s)
    s = re.sub(r"Sep", '09', s)
    s = re.sub(r"Oct", '10', s)
    s = re.sub(r"Nov", '11', s)
    s = re.sub(r"Dec", '12', s)

    # Replace all runs of whitespace with a plus
    s = re.sub(r"\s+", '', s)

    y = '2016' + s

    return y


# setting first day of the week to Sunday
# calendar.setfirstweekday(6)

# year = ['January',  'February',  'March',  'April',  'May',  'June',  'July',  'August',  'September',  'October',  'November',  'December']

def main(poster_url, poster_id, fight_card_url, event_date, event_name, bellator_event_fight_poster_url, bellator_event_id, bellator_event_fight_card_url, bellator_event_date, bellator_event_name):


    print('''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>fights.Today</title>

    <!-- Bootstrap -->
    <link href="css/bootstrap.min.css" rel="stylesheet">
    <!-- Slick slider css -->
    <link href="css/skdslider.css" rel="stylesheet">
    <!-- Font awesome css -->
    <link rel="stylesheet" href="css/font-awesome.min.css">
    <!-- smooth animate css file -->
    <link rel="stylesheet" href="css/animate.css">
    <!-- Main style css -->
    <link rel="stylesheet" href="style.css">
    <!-- Favicon -->
    <link rel="shortcut icon" type="image/png" href="img/favicon.png"/>
    <!-- Google Fonts -->
    <link href='http://fonts.googleapis.com/css?family=Roboto:400,300,100' rel='stylesheet' type='text/css'>



    <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
      <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>

  <body>
  <!-- BEGAIN PRELOADER -->
  <div id="preloader">
    <div id="status">&nbsp;</div>
  </div>
  <!-- END PRELOADER -->

  <!-- START HEADER SECTION -->
  <header id="headerArea">
    <a href="#" class="scrollToTop"><i class="fa fa-angle-up"></i></a>
    <div class="row">
      <div class="col-lg-12 col-md-12 col-sm-12">
        <div class="slider_area">
          <div class="menuarea">
            <div class="navbar navbar-default navbar-fixed-top" role="navigation">
              <div class="container">
                <div class="navbar-header">
                  <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
                    <span class="sr-only">Toggle navigation</span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                  </button>
                  <!-- For Text Logo -->
                 <a class="navbar-brand logo" href="#"><span>fights</span>Today</a>
                 <!-- For Img Logo -->
                  <!--  <a class="navbar-brand logo" href="#"><img src="img/logo.png" alt="logo"></a> -->
                </div>
                <div id="navbar" class="navbar-collapse collapse">
                  <ul class="nav navbar-nav navbar-right custom_nav mobnav" id="top-menu">
                    <li class="active"><a href="#headerArea">HOME</a></li>
                    <li><a href="#featuresSection">UPCOMING EVENTS </a></li>
                    <li><a href="#priceList">PAST EVENTS</a></li>
                    <li><a href="#bellatorEvents">BELLATOR EVENTS</a></li>
                  </ul>
                </div><!--/.nav-collapse -->
              </div>
            </div>
          </div>
          <ul id="demo1" class="slides">
            <li>
              <img src="img/slider/asfalt.png" />
              <!--Slider Description example-->
              <div class="slide-desc">
                <div class="slide_descleft">
                  <!-- img src="img/mobileapp_img.png" alt="img" -->
                </div>
                <div class="slide_descright">
                  <h1>Upcoming Events</h1>
                  <p>See upcoming UFC Events, Fight Cards and related Wikipedia, Social Media, Blog information</p>
                  <div class="header_btnarea">
                    <!--
                    <a href="#featuresSection" class="learnmore_btn">Learn More</a>
                    <a href="#" class="download_btn">Download</a>
                    -->
                  </div>
                </div>
              </div>
            </li>
            <li>
              <img src="img/slider/dark_wall.png" />
              <div class="slide-desc">
                <div class="slide_descleft">
                 <!-- img src="img/mobileapp_img.png" alt="img" -->
                </div>
                <div class="slide_descright">
                 <h1>Past Events</h1>
                  <p>See upcoming UFC Events, Fight Cards and related Wikipedia, Social Media, Blog information</p>
                  <div class="header_btnarea">
                    <!--
                    <a href="#featuresSection" class="learnmore_btn">Learn More</a>
                    <a href="#" class="download_btn">Download</a>
                    -->
                  </div>
                </div>
              </div>
            </li>
            <li>
              <img src="img/slider/dark_wall.png" />
              <div class="slide-desc">
                <div class="slide_descleft">
                 <!-- img src="img/mobileapp_img.png" alt="img" -->
                </div>
                <div class="slide_descright">
                 <h1>Bellator Events</h1>
                  <p>See upcoming and past Bellator Events, Fight Cards and related Wikipedia, Social Media, Blog information</p>
                  <div class="header_btnarea">
                    <!--
                    <a href="#featuresSection" class="learnmore_btn">Learn More</a>
                    <a href="#" class="download_btn">Download</a>
                    -->
                  </div>
                </div>
              </div>
            </li>
            <li>
              <img src="img/slider/stardust.png" />
              <div class="slide-desc">
               <div class="slide_descleft">
                 <!-- img src="img/mobileapp_img.png" alt="img" -->
               </div>
               <div class="slide_descright">
                  <h1>feature Yet to Come </h1>
                  <p>Lorem Ipsum Lorem Ipsum things will be added, as I add them</p>
                <div class="header_btnarea">
                  <!--
                  <a href="#" class="learnmore_btn">Learn More</a>
                  <a href="#" class="download_btn">Download</a>
                  -->
                </div>
               </div>
              </div>
            </li>
            <li>
              <img src="img/slider/dark_wood.png" />
              <div class="slide-desc">
                <div class="slide_descleft">
                   <!-- img src="img/mobileapp_img.png" alt="img" -->
                </div>
                <div class="slide_descright">
                  <h1>another feature Yet to Come</h1>
                   <p>promise things will be here sometime.</p>
                  <div class="header_btnarea">
                    <!--
                    <a href="#" class="learnmore_btn">Learn More</a>
                    <a href="#" class="download_btn">Download</a>
                    -->
                  </div>
                </div>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </header>
  <!-- END HEADER SECTION -->

  <!-- START FEATURES SECTION -->
  <section id="featuresSection">
    <div class="container">
      <div class="row">
        <div class="col-lg-12 col-md-12">
          <div class="features_ara">
            <h1>Upcoming UFC Events</h1>
            <p>
''')

    ##This section needs to produce the Upcoming Events
    #############################################################
    # nrows = len(poster_url)

    for x in range(511, 523):
        print('<tr><th >%s</th></tr><br>' % (event_name[x]))
        print('<tr><td><a href="%s">' % (fight_card_url[x]))
        print('<img src="%s"><br>' % (poster_url[x]))
        str1 = urlify(event_name[x])
        str2 = dateify(event_date[x])
        # print '<a href="https://www.google.com/calendar/render?action=TEMPLATE&text=%s&dates=%s/%s&details=&location=&sf=true&output=xml">Add to Google Calendar</a>'%(str1, str2, str2)
        print('<p>%s %s %s ' % (str1, str2, str2))
        # http://www.google.com/calendar/event?action=TEMPLATE&text=Event1&dates=20140905/20140905&details=&location=&trp=false&sprop=&sprop=name:
        # print '<img src="images/Small_Wikipedia_logo.png">'
        print('</a></td></tr><br>')

    print('''
            </p>
            </div>
        </div>
      </div>
    </div>
  </section>

  <!-- START PRICE LIST SECTION -->
  <section id="priceList">
   <div class="container">
      <div class="row">
        <div class="col-lg-12 col-md-12">
          <div class="features_ara">
          <h1>Past UFC Events</h1>
          <p>''')

    ##This section needs to produce the Past UFC Events
    #############################################################
    # nrows = len(poster_url)

    i = 510
    while i >= 0:
        print('<tr><th >%s</th></tr><br>' % (event_name[i]))
        print('<tr><td><a href="%s">' % (fight_card_url[i]))
        print('<img src="%s"><br>' % (poster_url[i]))
        print('</a></td></tr><br>')
        i -= 1
        # print '<img src="images/Small_Wikipedia_logo.png">'

    print('''
            </p>
        </div>
      </div>
    </div>
   </div>
  </section>
  <!-- END PRICE LIST SECTION -->

<!-- START BELLATOR EVENTS SECTION -->
<section id="bellatorEvents">
 <div class="container">
    <div class="row">
      <div class="col-lg-12 col-md-12">
        <div class="features_ara">
        <h1>Bellator Events</h1>
        <p>''')

    # This section needs to produce the Past UFC Events
    #############################################################
    # nrows = len(poster_url)

    for z in range(0, 250):
        print('<tr><th >%s</th></tr><br>' % (bellator_event_name[z]))
        print('<tr><td><a href="%s">' % (bellator_event_fight_card_url[z]))
        print('<img src="https://cdn.mmaweekly.com/wp-content/uploads/2017/01/Bellator-173-and-BAMMA-28-Fight-Poster.jpg"><br>')
        # print '<img src="images/Small_Wikipedia_logo.png">'
        print('</a></td></tr><br>')

    print('''
          </p>
      </div>
    </div>
  </div>
 </div>
</section>
<!-- END Bellator Events SECTION -->
  <!-- START FOOTER SECTION -->
  <footer id="footer">
    <div class="container">
      <div class="row">
        <div class="col-lg-12 col-md-12">
          <div class="footer_area">
            <p>Designed By <a href="http://markpereira.com" rel="nofollow">Mark Pereira</a></p>
          </div>
        </div>
      </div>
    </div>
  </footer>
  <!-- END FOOTER SECTION -->

  <!-- JQuery Files -->

  <!-- Initialize jQuery Library -->
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script>
  <!-- Google map -->

  <script src="https://maps.googleapis.com/maps/api/js"></script>
  <script src="js/jquery.ui.map.js"></script>

  <!-- Skds slider -->
  <script src="js/skdslider.min.js"></script>
  <!-- Bootstrap js  -->
  <script src="js/bootstrap.min.js"></script>
  <!-- For smooth animatin  -->
  <script src="js/wow.min.js"></script>

  <!-- Custom js -->
  <script type="text/javascript" src="js/custom.js"></script>

  </body>
</html>
''')


# Database Connection
db = MySQLdb.connect(host="markpereira.com", user="mark5463_ft_test", passwd="fttesting", db="mark5463_ft_prod")

# Cursor object. It will let you execute the queries
cur = db.cursor()

# This section will delete the information on the table, for a clean run.
# cur.execute("TRUNCATE mma_events_wiki_poster ")


# This section will query the database and return all data in the table
cur.execute("SELECT event_fight_poster_url, event_id, event_fight_card_url, event_date, event_name from wiki_mma_events_poster ")

# initialize the arrays
event_fight_poster_url = []
event_id = []
event_fight_card_url = []
event_date = []
event_name = []

# load our arrays with all of our event data.
for row in cur.fetchall():
    event_fight_poster_url.append(row[0])
    event_id.append(row[1])
    event_fight_card_url.append(row[2])
    event_date.append(row[3])
    event_name.append(row[4])

format_org = "Bellator"
# Bellator query
cur.execute("SELECT event_id, event_fight_card_url, event_date, event_name from wiki_mma_events where event_org = '%s'" % format_org)

bellator_event_id = []
bellator_event_fight_card_url = []
bellator_event_date = []
bellator_event_name = []
bellator_event_fight_poster_url = 'https://cdn.mmaweekly.com/wp-content/uploads/2017/01/Bellator-173-and-BAMMA-28-Fight-Poster.jpg'

for row2 in cur.fetchall():
    # bellator_event_fight_poster_url.append(row[0])
    bellator_event_id.append(row2[0])
    bellator_event_fight_card_url.append(row2[1])
    bellator_event_date.append(row2[2])
    bellator_event_name.append(row2[3])

if __name__ == "__main__":
    main( event_fight_poster_url, event_id, event_fight_card_url, event_date, event_name, bellator_event_fight_poster_url, bellator_event_id, bellator_event_fight_card_url, bellator_event_date, bellator_event_name )
