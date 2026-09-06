import ftplib
import os
ftp_host = "ftp.markpereira.com"
ftp_user = os.environ['FTP_ID']
ftp_password = os.environ['FTP_PASSWORD']
session = ftplib.FTP(ftp_host, ftp_user, ftp_password)
file = open('all_events.ics','rb')                  # file to send
session.storbinary('STOR all_events.ics', file)     # send the file
file.close()     
file = open('all_events_test.ics','rb')                  # file to send
session.storbinary('STOR all_events_test.ics', file)     # send the file
file.close()

# The generated site itself. Only uploaded when generate-html.py actually
# produced it, so a failed generation cannot blank the live page.
if os.path.exists('index.php') and os.path.getsize('index.php') > 0:
    with open('index.php', 'rb') as f:
        session.storbinary('STOR index.php', f)
    print('Uploaded index.php (%d bytes)' % os.path.getsize('index.php'))
else:
    print('index.php missing or empty - not uploading')

session.quit()
