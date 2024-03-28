##################
# FILE HAS BEEN TESTED SUCCESSFULLY
#

from lxml import html, etree
import io
#from django.utils.encoding import smart_str, smart_text
import django
from django.utils.encoding import smart_str
django.utils.encoding.smart_text = smart_str
from pyquery import PyQuery as pq
from datetime import datetime
import re
import calendar
import time
import sys
import requests
import MySQLdb
from pastevents import *
from schedevents import * 
from totalevents import *
from bellator_pastevents import *
from bellator_schedevents import * 
from bellator_totalevents import *
import os


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
    s = re.sub(r"2021", '', s)
    s = re.sub(r"2022", '', s)
    s = re.sub(r"2023", '', s)
    s = re.sub(r"2024", '', s)

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

    print('''<?php
session_start();
?>
<!DOCTYPE html>
<html lang="en" class="no-js">
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
        <meta name="description" content="Fights Today upcoming & past events. Bellator & UFC Event previews. Stats, Rankings, MMA Trivia, iCal subscription. Track your stats & compete."/>
        <meta name="author" content="" />
        <title>Welcome to fights.Today - Your source for Upcoming UFC Bellator MMA Events</title>
        <link rel="icon" type="image/x-icon" href="assets/img/favicon.ico" />
        <!-- Font Awesome icons (free version)-->
        <script src="https://use.fontawesome.com/releases/v5.13.0/js/all.js" crossorigin="anonymous"></script>
        <!-- Google fonts-->
        <link href="https://fonts.googleapis.com/css?family=Montserrat:400,700" rel="stylesheet" type="text/css" />
        <link href="https://fonts.googleapis.com/css?family=Droid+Serif:400,700,400italic,700italic" rel="stylesheet" type="text/css" />
        <link href="https://fonts.googleapis.com/css?family=Roboto+Slab:400,100,300,700" rel="stylesheet" type="text/css" />
        <!-- Core theme CSS (includes Bootstrap)-->
        <link href="css/styles.css" rel="stylesheet" />
        <style>
            
             /* Modal styles */
             .modal {
    display: none;
    position: fixed;
    z-index: 1;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    overflow: auto;
    background-color: rgba(0, 0, 0, 0.4);
  }

  .modal-content {
    background-color: #fefefe;
    margin: auto;
    padding: 1px;
    border: 1px solid #888;
    max-width: 800px;
    max-height: 800px;
    overflow: auto;
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }

.close-modal {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 20px;
  font-weight: bold;
  cursor: pointer;
}

.close-modal:hover {
  color: red;
}


#modalContent table {
        border-collapse: separate;
        border-spacing: 0;
        width: 100%;
        margin-top: 20px;
    }

    #modalContent th,
    #modalContent td {
        padding: 10px;
        text-align: left;
        font-weight: bold;
        border-bottom: 1px solid #ddd;
    }

    #modalContent tr:not(:first-child) {
        border-top: 2px solid #ddd;
    }

    #modalContent tr:nth-child(even) {
        background-color: #f2f2f2;
    }

    #modalContent tr:hover {
        background-color: #e9e9e9;
    }

    #modalContent th {
        background-color: #333;
        color: white;
    }

    .table-format {
  width: 100%;
  border-collapse: collapse;
}

.table-format th,
.table-format td {
  /*border: 1px solid black;*/
  padding: 0px;
}

.table-format th {
  background-color: #f2f2f2;
}


.small-text {
  font-size: 8px;
}
.table-format td:not(:nth-child(2)):not(:nth-child(3)) {
  border-right: none;
}

/* Custom colors */
.table-format th {
  background-color: #fed136;
  color: #212529;
}

.small-text {
  color: #6c757d;
}

.table-format tr:nth-child(even) {
  background-color: #f2f2f2;
}

.table-format tr:hover {
  background-color: #e9e9e9;
}

.table-format tr:nth-child(odd) {
  background-color: #ffe68f;
}

        </style>
        <link rel="stylesheet" href="css/demo.css"/>
        <link rel="stylesheet" href="css/jquery.flipster.min.css"/>
        <!-- Yandex.Metrika counter -->
        <script type="text/javascript" >
            (function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};
                 m[i].l=1*new Date();
                for (var j = 0; j < document.scripts.length; j++) {if (document.scripts[j].src === r) { return; }}
                    k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})
                    (window, document, "script", "https://mc.yandex.ru/metrika/tag.js", "ym");

                    ym(93643512, "init", {
                            clickmap:true,
                            trackLinks:true,
                            accurateTrackBounce:true
                    });
        </script>
        <noscript><div><img src="https://mc.yandex.ru/watch/93643512" style="position:absolute; left:-9999px;" alt="" /></div></noscript>
        <!-- /Yandex.Metrika counter -->
        <script src="js/jquery.min.js"></script>
        <script src="js/jquery.flipster.min.js"></script>

    </head>
    <body id="page-top">
        <!-- Navigation-->
        <nav class="navbar navbar-expand-lg navbar-dark fixed-top" id="mainNav">
            <div class="container">
                <a class="navbar-brand js-scroll-trigger" href="#page-top"><!--<img src="assets/img/navbar-logo.svg" alt="" / ---></a>
                <button class="navbar-toggler navbar-toggler-right" type="button" data-toggle="collapse" data-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
                    Menu
                    <i class="fas fa-bars ml-1"></i>
                </button>
                <div class="collapse navbar-collapse" id="navbarResponsive">
                    <ul class="navbar-nav text-uppercase ml-auto">
                        <li class="nav-item"><a class="nav-link js-scroll-trigger" href="#services">Upcoming UFC Events</a></li>
                        <li class="nav-item"><a class="nav-link js-scroll-trigger" href="#portfolio">Past UFC Events</a></li>
                        <li class="nav-item"><a class="nav-link js-scroll-trigger" href="#bellatorup">Upcoming Bellator Events</a></li>
                        <li class="nav-item"><a class="nav-link js-scroll-trigger" href="#bellatorpast">Past Bellator Events</a></li>
                        <li class="nav-item"><a class="nav-link js-scroll-trigger" href="https://fights.today/picks/">My Picks</a></li>
                        <li class="nav-item"><a class="nav-link js-scroll-trigger" href="https://fights.today/trivia/">Trivia</a></li>
                        <li class="nav-item"><a class="nav-link js-scroll-trigger" href="https://fights.today/ical/">iCal</a></li>
                        <li class="nav-item"><a class="nav-link js-scroll-trigger" href="https://fights.today/socials/">Socials</a></li>
                        <li class="nav-item"><a class="nav-link js-scroll-trigger" href="#more">More</a></li>
                        <?php
                            if (isset($_SESSION['username'])) {
                                // User is logged in
                                $username = $_SESSION['username'];
                                echo '<li class="nav-item">' . $username . ' Logged in, <a class="nav-link js-scroll-trigger" href="https://fights.today/auth/logout.php">logout</a></li>';
                            } else {
                            // User is not logged in
                            echo '<li class="nav-item"><a class="nav-link js-scroll-trigger" href="https://fights.today/auth/">Login</a></li>';
                            }
                        ?>
                    </ul>
                </div>
            </div>
        </nav>
        <!-- Masthead-->
        <header class="masthead">
            <div class="container">
                <h1 class="masthead-subheading"> Welcome to fights.Today!</h1>
                <div class="masthead-heading text-uppercase">A way to see what fights are happening today.</div>
                <a class="btn btn-primary btn-xl text-uppercase js-scroll-trigger" href="#services">Tell Me More</a>
            </div>
        </header>
        <!-- Services-->
        <section class="page-section" id="services">
            <div class="container">
                <div class="text-center">
                    <h2 class="section-heading text-uppercase">Upcoming UFC Events</h2>
                    <h3 class="section-subheading text-muted">Check out these featured upcoming events. Click or tap the poster to view the Fight Card</h3>
                </div>
                <div class="row text-center">
                    <div class="col-lg-12 col-md-12">
                        <div class="features_ara">
                        <p>
<!-- Modal HTML -->
<div id="eventModal" class="modal">
    <div class="modal-content">
        <span class="close-modal">&times;</span>
        <div id="modalContent"></div>
    </div>
</div>
''', file=f)

    ##This section needs to produce the Upcoming Events
    #############################################################
    # nrows = len(poster_url)

    for x in range(PAST_EVENTS, TOTAL_EVENTS):
        event_container_string = event_name[x]
        modified_string = event_container_string.replace(" ", "_")
        print('<div class="event-container" id="%s">' % (modified_string), file=f)
        print('<tr><th><h2>%s</h2></th></tr><br>' % (event_name[x]), file=f)
        print('<tr><th><h6>%s</h6></th></tr><br>' % (event_date[x]), file=f)
        
        if(poster_url[x]=="https:"):
            print('<img src="https://fights.today/images/ufc_placeholder.png" alt="UFC event poster for %s"><br>' % (event_name[x]), file=f)
        else:
            print('<img src="%s" alt="UFC event poster for %s"><br>' % (poster_url[x], event_name[x]), file=f)
        print('<div class="event-section">', file=f)
        # str1 = urlify(event_name[x])
        # str2 = dateify(event_date[x])
        ## print '<a href="https://www.google.com/calendar/render?action=TEMPLATE&text=%s&dates=%s/%s&details=&location=&sf=true&output=xml">Add to Google Calendar</a>'%(str1, str2, str2)
        # print('<p>%s %s %s ' % (str1, str2, str2), file=f)
        ## http://www.google.com/calendar/event?action=TEMPLATE&text=Event1&dates=20140905/20140905&details=&location=&trp=false&sprop=&sprop=name:
        ## print '<img src="images/Small_Wikipedia_logo.png">'
        print('</td></tr><br>', file=f)
        print('</div>', file=f)
        print('</div>', file=f)
        print('<p>', file=f)



    print('''
                  </p>
                </div>
            </div>
        </section>
        <!-- Portfolio Grid-->
        <section class="page-section" id="portfolio">
            <div class="text-center">
                <h2 class="section-heading text-uppercase">Past UFC Events</h2>
                <h3 class="section-subheading text-muted">Discover results from the latest bouts</h3>
            </div>
            <div id="demo-flat" class="demo">
                <div id="flat">
                <ul>''', file=f)

    ##This section needs to produce the Past UFC Events
    #############################################################
    # nrows = len(poster_url)

    i = PAST_EVENTS - 1 
    length_of_loop = PAST_EVENTS - SCHED_EVENTS
    while i >= length_of_loop:
        print('<li data-flip-title="%s">' % (event_name[i]), file=f)
        print('<a href="%s" class="Button Block">' %(fight_card_url[i]), file=f)
        # print('<tr><td><a href="%s">' % (fight_card_url[i]), file=f)
        print('<img src="%s" alt="UFC event poster for %s"><br>' % (poster_url[i], event_name[i]), file=f)
        print('</a></li>', file=f)
        i -= 1
        # print '<img src="images/Small_Wikipedia_logo.png">'

    print('''
                               </ul>
                </div>
            
            <script>
                var flat = $("#flat").flipster({
                    style: 'flat',
                    spacing: -0.25,
                    start: 'left'
                    
                });
            </script>
            </div>
            </section>
<!--Bellator Section -->
        <!-- Bellator Upcoming Events-->
        <section class="page-section" id="bellatorup">
            <div class="container">
                <div class="text-center">
                    <h2 class="section-heading text-uppercase">Upcoming Bellator Events</h2>
                    <h3 class="section-subheading text-muted">Next up from Bellator</h3>
                </div>
                <div class="row text-center">
                    <div class="col-lg-12 col-md-12">
                        <div class="features_ara">
                        <p>''', file=f)

    # This section needs to produce the Bellator Upcoming Events
    #############################################################
    # nrows = len(poster_url)

    for x in range((BELLATOR_TOTAL_EVENTS - BELLATOR_SCHED_EVENTS) + 1, (BELLATOR_TOTAL_EVENTS + 1)):
        event_container_string = bellator_event_name[x]
        modified_string = event_container_string.replace(" ", "_")
        print('<div class="event-container" id="%s">' % (modified_string), file=f)
        print('<tr><th><h2>%s</h2></th></tr><br>' % (bellator_event_name[x]), file=f)
        print('<tr><th><h6>%s</h6></th></tr><br>' % (bellator_event_date[x]), file=f)
        
        if(bellator_event_fight_poster_url[x]=="https:"):
            print('<img src="https://fights.today/images/bellator_placeholder.png" alt="Bellator event poster for %s"><br>' % (bellator_event_name[x]), file=f)
        else:
            print('<img src="%s" alt="Bellator event poster for %s"><br>' % (bellator_event_fight_poster_url[x],bellator_event_name[x]), file=f)
        print('<div class="event-section">', file=f)
        #print('<img src="https://cdn.mmaweekly.com/wp-content/uploads/2017/01/Bellator-173-and-BAMMA-28-Fight-Poster.jpg"><br>', file=f)
        # str1 = urlify(event_name[x])
        # str2 = dateify(event_date[x])
        ## print '<a href="https://www.google.com/calendar/render?action=TEMPLATE&text=%s&dates=%s/%s&details=&location=&sf=true&output=xml">Add to Google Calendar</a>'%(str1, str2, str2)
        # print('<p>%s %s %s ' % (str1, str2, str2), file=f)
        ## http://www.google.com/calendar/event?action=TEMPLATE&text=Event1&dates=20140905/20140905&details=&location=&trp=false&sprop=&sprop=name:
        ## print '<img src="images/Small_Wikipedia_logo.png">'
        print('</td></tr><br>', file=f)
        print('</div>', file=f)
        print('</div>', file=f)
        print('<p>', file=f)

    print('''
                        </p>
                </div>
            </div>
        </section>
        <!-- Portfolio Grid-->
        <section class="page-section" id="bellatorpast">

            <div class="text-center">
                <h2 class="section-heading text-uppercase">Past Bellator Events</h2>
                <h3 class="section-subheading text-muted">Check out these historic results</h3>
            </div>
            <div id="demo-flat" class="demo">
                <div id="flat2">
                    <ul>
''', file=f)


    #z = BELLATOR_PAST_EVENTS - 1
    z = BELLATOR_PAST_EVENTS 
    length_of_loop2 = BELLATOR_PAST_EVENTS - BELLATOR_SCHED_EVENTS
    while z >= length_of_loop2:
        print('<li data-flip-title="%s">' %  (bellator_event_name[z]), file=f)
        print('<a href="%s" class="Button Block">' %(bellator_event_fight_card_url[z]), file=f)
        if(bellator_event_fight_poster_url[z] == "https:"):
            print('<img src="https://fights.today/images/bellator_placeholder.png" alt="Bellator event poster for %s"><br>' % (bellator_event_name[z]), file=f)
        else:
            print('<img src="%s" alt="Bellator event poster for %s"><br>' % (bellator_event_fight_poster_url[z],bellator_event_name[z]), file=f)
        #print('<img src="https://cdn.mmaweekly.com/wp-content/uploads/2017/01/Bellator-173-and-BAMMA-28-Fight-Poster.jpg">', file=f)
        # print '<img src="images/Small_Wikipedia_logo.png">'
        print('</a></li>', file=f)
        z-=1

    print('''
                    </ul>
                </div>
            
            <script>
                var flat = $("#flat2").flipster({
                    style: 'flat',
                    spacing: -0.25,
                    start: 'left'
                    
                });
            </script>
            <script>
            // Get the modal and modal content elements
const modal = document.getElementById("eventModal");
const modalContent = document.querySelector("#eventModal .modal-content");
const closeModalButton = document.querySelector("#eventModal .close-modal");

// Function to open the modal and display the content
function openModal(content) {
  modal.style.display = "block";
  modalContent.innerHTML = content;
}

// Function to close the modal
function closeModal() {
  modal.style.display = "none";
}

// Attach click event to the close button
closeModalButton.addEventListener("click", closeModal);

// Attach click event to the window outside of the modal
window.addEventListener("click", function (event) {
  if (event.target === modal) {
    closeModal();
  }
});





let isModalClosed = false; // Flag to track if the modal was just closed

// Create a mapping to store original content for each container
const originalContentMap = {};

// Get all container elements with class "event-container"
const containers = document.querySelectorAll('.event-container');

// Iterate over each container
containers.forEach(container => {
  // Check if event listener is already attached
  if (!container.hasAttribute('data-event-listener')) {
    // Store the original content for each container
    originalContentMap[container.id] = container.innerHTML;

    // Add click event to each container
    container.addEventListener('click', toggleContent);

    // Set attribute to mark that event listener is attached
    container.setAttribute('data-event-listener', true);
  }
});

function toggleContent(event) {
  // Prevent event propagation
  event.stopPropagation();
  const clickedElement = event.target;

  // Check if the clicked element is an <img> within an event-container
  if (clickedElement.tagName === 'IMG' && clickedElement.closest('.event-container')) {
    const clickedContainer = clickedElement.closest('.event-container');
    const isContentVisible = (clickedContainer.innerHTML !== originalContentMap[clickedContainer.id]);

    if (isContentVisible) {
      // Revert to the original content
      clickedContainer.innerHTML = originalContentMap[clickedContainer.id];
    } else {
      // Fetch the event data from the PHP file
      const xhr = new XMLHttpRequest();
      xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
          if (xhr.status === 200) {
            // Parse the JSON response
            const response = JSON.parse(xhr.responseText);
            // Update the modal content with the extracted HTML
            modalContent.innerHTML = response.html;
            // Open the modal only if it was not just closed
            if (!isModalClosed) {
              openModal(response.html);
            } else {
              isModalClosed = false; // Reset the flag
            }
          } else {
            console.error('Error:', xhr.status);
          }
        }
      };

      // Get the container ID and send it to get_event_data.php as a parameter
      const eventName = clickedContainer.id.replace(/_/g, ' '); // Replace underscores with spaces
      const url = `get_event_data.php?eventName=${encodeURIComponent(eventName)}`;
      xhr.open('GET', url);
      xhr.send();
    }
  }
}

            </script>
            </div>
            </section>
         <!-- More -->
        <section class="page-section" id="more">
            <div class="container">
                <div class="text-center">
                    <h2 class="section-heading text-uppercase">More</h2>
                    <h3 class="section-subheading text-muted"> Learn about what else we have to offer.</h3>
                </div>
                <ul class="timeline">
                    <li>
                        <div class="timeline-image"><img class="rounded-circle img-fluid" src="assets/img/about/1.jpg" alt="" /></div>
                        <div class="timeline-panel">
                            <div class="timeline-heading">
                                <h4>My Picks</h4>
                                <h4 class="subheading">Track your fighting IQ</h4>
                            </div>
                            <div class="timeline-body"><p class="text-muted">We're constantly evolving and you can join us and play along hassle free! All thats required is to use one of our third party authentication methods and use your already existing account to log your picks! We don't ever send communications to our users and we do not store or use your information in any way. Please see our Terms of Service for more.</p></div>
                        </div>
                    </li>
                    <li class="timeline-inverted">
                        <div class="timeline-image"><img class="rounded-circle img-fluid" src="assets/img/about/2.jpg" alt="" /></div>
                        <div class="timeline-panel">
                            <div class="timeline-heading">
                                <h4>iCal</h4>
                                <h4 class="subheading">Never miss a fight again!</h4>
                            </div>
                            <div class="timeline-body"><p class="text-muted">Easily add fights.Today's iCal link as a subscription in your cell phone to stay up to date with all upcoming events! Supporting any app that can use iCal. More information check out the <a href="https://fights.today/ical/">iCal section</a>.</p></div>
                        </div>
                    </li>
                    <li>
                        <div class="timeline-image"><img class="rounded-circle img-fluid" src="assets/img/about/3.jpg" alt="" /></div>
                        <div class="timeline-panel">
                            <div class="timeline-heading">
                                <h4>Community</h4>
                                <h4 class="subheading">See what your fellow fight fans are discussing</h4>
                            </div>
                            <div class="timeline-body"><p class="text-muted">Coming soon - News, <a href="https://fights.today/socials/">Social Media</a> and Community Discussions </p></div>
                        </div>
                    </li>
                    <li class="timeline-inverted">
                        <div class="timeline-image">
                            <h4>
                                What are
                                <br />
                                The Fights
                                <br />
                                Today!
                            </h4>
                        </div>
                    </li>
                </ul>
            </div>
        </section>
        <!-- Footer-->
        <footer class="footer py-4">
            <div class="container">
                <div class="row align-items-center">
                    <div class="col-lg-4 text-lg-left">Copyright © fights.Today 2023</div>
                    <div class="col-lg-4 my-3 my-lg-0">
                        <a class="btn btn-dark btn-social mx-2" href="https://twitter.com/fights_Today"><i class="fab fa-twitter"></i></a>
                        <a class="btn btn-dark btn-social mx-2" href="#!"><i class="fab fa-facebook-f"></i></a>
                        <a class="btn btn-dark btn-social mx-2" href="#!"><i class="fab fa-linkedin-in"></i></a>
                    </div>
                    <div class="col-lg-4 text-lg-right">
                        <a class="mr-3" href="#!">Privacy Policy</a>
                        <a href="#!">Terms of Use</a>
                    </div>
                </div>
            </div>
        </footer>
        <!-- Bootstrap core JS-->
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.bundle.min.js"></script>
        <!-- Third party plugin JS-->
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery-easing/1.4.1/jquery.easing.min.js"></script>
        <!-- Contact form JS-->
        <script src="assets/mail/jqBootstrapValidation.js"></script>
        <script src="assets/mail/contact_me.js"></script>
        <!-- Core theme JS-->
        <script src="js/scripts.js"></script>
        <!--flipper shit-->
        <script src="/js/jquery.min.js"></script>
        <script src="/js/jquery.flipster.min.js"></script>
    </body>
</html>
''', file=f)


# Database Connection
# db = MySQLdb.connect(host="markpereira.com", user="mark5463_ft_test", passwd="fttesting", db="mark5463_ft_prod")
#db = MySQLdb.connect(host="dev-mysql.markpereira.com", user="root", passwd="fttesting", db="mark5463_ft_prod")
#local docker mysql
#db = MySQLdb.connect(host="192.168.1.96", user="root", passwd="fttesting", port=3308, db="mark5463_ft_prod", charset="utf8")
#prodlike mysql
db = MySQLdb.connect(
    host=os.environ['MYSQL_HOST'],
    user=os.environ['MYSQL_ID'],
    passwd=os.environ['MYSQL_PASSWORD'],
    db="mark5463_ft_prod",
    charset="utf8"
)



# Cursor object. It will let you execute the queries
cur = db.cursor()

# This section will delete the information on the table, for a clean run.
# cur.execute("TRUNCATE mma_events_wiki_poster ")


# This section will query the database and return all data in the table
cur.execute("SELECT event_fight_poster_url, event_id, event_fight_card_url, event_date, event_name from wiki_mma_events_poster where event_org = 'UFC' ")

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


# Bellator query
cur.execute("SELECT event_fight_poster_url, event_id, event_fight_card_url, event_date, event_name from wiki_mma_events_poster where event_org = 'Bellator'")

bellator_event_fight_poster_url = []
bellator_event_id = []
bellator_event_fight_card_url = []
bellator_event_date = []
bellator_event_name = []


for row2 in cur.fetchall():
    bellator_event_fight_poster_url.append(row2[0])
    bellator_event_id.append(row2[1])
    bellator_event_fight_card_url.append(row2[2])
    bellator_event_date.append(row2[3])
    bellator_event_name.append(row2[4])

if __name__ == "__main__":
    f = open("index.php", "a")
    main(event_fight_poster_url, event_id, event_fight_card_url, event_date, event_name, bellator_event_fight_poster_url, bellator_event_id, bellator_event_fight_card_url, bellator_event_date, bellator_event_name)
    f.close()

