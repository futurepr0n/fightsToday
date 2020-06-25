import ftplib
session = ftplib.FTP('ftp.markpereira.com','fights@markpereira.com','fights2dayftp')
file = open('../index.html','rb')                  # file to send
session.storbinary('STOR index.html', file)     # send the file
file.close()                                    # close file and FTP
file = open('../all_events.ics','rb')                  # file to send
session.storbinary('STOR all_events.ics', file)     # send the file
file.close()     
session.quit()