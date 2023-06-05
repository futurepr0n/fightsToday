import ftplib
ftp_host = "ftp.markpereira.com"
ftp_user = os.environ['FTP_ID']
ftp_password = os.environ['FTP_PASSWORD']
session = ftplib.FTP(ftp_host, ftp_user, ftp_password)
file = open('index.php','rb')                  # file to send
session.storbinary('STOR index.php', file)     # send the file
file.close()                                    # close file and FTP
file = open('all_events.ics','rb')                  # file to send
session.storbinary('STOR all_events.ics', file)     # send the file
file.close()     
session.quit()
