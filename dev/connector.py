#!/usr/bin/env python
import os
from configparser import ConfigParser , ExtendedInterpolation 
import mysql.connector
import cx_Oracle
import psycopg2
import paramiko
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class DbList():
    __confParser = ConfigParser()
    def __init__(self):    
        self.__confParser.read('./dev/config.ini')
        #self.__confParser.read('/data/scripts/dev/config.ini')


    #MySQL DB Connect
    def get_mysql_connect(self):
        try:        
            connection_mysql = mysql.connector.connect(
                user = self.__confParser.get('mysql', 'user'),
                passwd = self.__confParser.get('mysql', 'password'),
                host = self.__confParser.get('mysql', 'host'),
                #charset = self.__confParser.get('mysql', 'charset'),
            )
            print ('DB MySQL: Connected')
            return connection_mysql  
        except Exception as err1:
            print(err1)
            print ('DB MySQL: Connection Error')
#        finally:
#            #connection_mysql.close()  #TODO НЕ ЗАБЫТЬ УБРАТЬ 
#            print("DB MySQL: Connection Closed")  

    #Oracle DB Connect
    def ora_db_connect(self):
        try:            
            connection_oracle = cx_Oracle.connect(self.__confParser.get('ora', 'user'), self.__confParser.get('ora','password'), self.__confParser.get('ora','host'))
            print ("Db Oracle: Connected")    
            return connection_oracle
        except Exception as err2:
            print(err2)
            print ("Db Oracle: Connection Error") 
#        finally:
#            #connection_oracle.close()  #TODO НЕ ЗАБЫТЬ УБРАТЬ 
#            print("Db Oracle: Connection Closed")  

    #PostgreSQL Connect
    def pgsql_connect(self):
        try:
            coonection_postrgeSQL = psycopg2.connect(
                host = self.__confParser.get('pgsql', 'host'),
                database = self.__confParser.get('pgsql', 'db_name'),
                user = self.__confParser.get('pgsql', 'user'),
                password = self.__confParser.get('pgsql', 'password'),
            )
            print("Db PostgreSQL: Connected") 
            return coonection_postrgeSQL
        except Exception as err3:
            print(err3)
            print("Db PostgreSQL: Connection Error")
#        finally:
#            #coonection_postrgeSQL.close()  #TODO НЕ ЗАБЫТЬ УБРАТЬ 
#            print("Db PostgreSQL: Connection Closed") 
        

    def selectYourDb(self, dbname):
        #print(self.__confParser.get('mysql', 'password'))
        if self.__confParser.has_section(dbname):
            if dbname == 'ora':
                return self.ora_db_connect()
            elif dbname == 'mysql':
                return self.get_mysql_connect()
            elif dbname == 'pgsql':
                return self.pgsql_connect()    
        else:
            print('Unknown DB type')
        
        
    #SFTP для отчетов
    #Пример remotepath_path = '/opt/reports/Old/'
    def delivery_to_server(self, filename, remotepath_path):
        try:
            transport = paramiko.Transport(self.__confParser.get('remote', 'hostname'),int(self.__confParser.get('remote', 'port')))
            transport.connect(username=self.__confParser.get('remote', 'user'), password=self.__confParser.get('remote', 'password'))
            print('SFTP connect : OK')
            sftp = paramiko.SFTPClient.from_transport(transport)
            localpath = filename
            file_name = os.path.basename(filename)
            remotepath = remotepath_path + file_name
            sftp.put(localpath, remotepath)
        except Exception as err:
            print(err)
        finally: 
            sftp.close()
            transport.close()

    # отправка письма (шапка , тема , список получателей)
    # Функция Ольги Спириной, необходимо ,как будет желание, изучить подробнее(возможно доработать)
    def send_email(self, emails, subject, body_text):
        try:
            host = self.__confParser.get('send_mail', 'host')
            from_addr = self.__confParser.get('send_mail', 'from_addr')
            # create the message
            msg = MIMEMultipart()
            msg["From"] = from_addr
            msg["Subject"] = subject
            if body_text:
                msg.attach( MIMEText(body_text) )
            msg["To"] = ', '.join(emails)
            server = smtplib.SMTP(host)
            server.sendmail(from_addr, emails, msg.as_string())
        except Exception as mailerr:
            print(mailerr)
        finally:
            server.quit()   


if __name__ == '__main__':
    a=DbList()
    con = a.selectYourDb('pgsql')
    print(con)
    con.close()






