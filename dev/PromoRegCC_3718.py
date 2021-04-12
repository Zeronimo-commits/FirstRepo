#!/usr/bin/env python

import os
import connector 
import pandas as pd
from datetime import datetime

if __name__ == '__main__':
    os.environ["NLS_LANG"] = ".AL32UTF8"
    datetime_now = datetime.now().strftime("%Y%m%d%H%M%S")
    #Название файла
    filename = 'PromoReg_MTSCB200'+datetime_now+'.csv'
    #Путь к нужной папке на remoteserver
    remotepath_part = '/opt/reports/Old/'
    

    a=connector.DbList()
    #Открываем Коннект к Mysql
    ConnectionMySql = a.selectYourDb('mysql')   
    mysql_select = '''
        
        SELECT t1.entityId AS "ENTITY_ID",
        t2.`value` AS "MSISDN",
        t1.`value` AS "RegPromocode",
        MIN(t3.dateFrom) AS "RegDate"
        -- DATEDIFF(ch.RequestDate, MIN(t3.dateFrom)) AS "DifferenceDay"
        FROM CUST.EntityPropertyValue t1
        LEFT JOIN CUST.EntityPropertyValue t2 ON t1.entityId = t2.entityId
        LEFT JOIN CUST.EntityPropertyValue t3 ON t1.entityId = t3.entityId
        LEFT JOIN CUST.`{ChargeCashbackHistory}` ch on t1.entityId = ch.EntityId
        AND LEFT(HEX(ch.ChargeAmount), 6) != '000000'
        AND RIGHT(HEX(ch.ChargeAmount), 4) = '4030'
        WHERE 1 = 1
        AND t1.entityPropertyKindId = '1084310034'
        AND t1.`value` = 'MTSCB200'
        AND t2.entityPropertyKindId = '2050'
        AND t3.entityPropertyKindId = '2084'
        GROUP BY t1.entityId,
        t2.`value`,
        t1.`value`; 

    '''      
   
    sqlDf = pd.read_sql(mysql_select,ConnectionMySql)

    #Открываем Коннект к Oracle
    ConnectionOra = a.selectYourDb('ora')
    OraDF = pd.DataFrame()
    
    for i in sqlDf['ENTITY_ID']:
        try :
            ora_select = ''' 
                SELECT
                	amo.ENTITY_ID as ENTITY_ID,
                	amo.ACCOUNT as MSISDN,
                	amo.REQUEST_DATE as PurchaseDate,
                	amo.AMOUNT as PurchaseAmount,
                	amo.QUANTITY as Cashback 
                FROM
                	CHARGE_HISTORY_CASH_BACK amo
                JOIN (
                	SELECT
                		ENTITY_ID , ACCOUNT, min(REQUEST_DATE) AS mindate
                	FROM
                		CHARGE_HISTORY_CASH_BACK
                	WHERE
                		1 = 1
                		AND ENTITY_ID IN ({0})
                		AND CASHBACK_STATUS_ID = 2
                		AND OPERATION_TYPE_CODE = 'C'
                		AND AMOUNT >= 500
                		GROUP BY ENTITY_ID , ACCOUNT ) chcb 
                	ON chcb.ENTITY_ID = amo.ENTITY_ID AND CHCB.mindate = amo.REQUEST_DATE
                WHERE
                	1 = 1
                	AND amo.ENTITY_ID IN ({0})
                	AND amo.CASHBACK_STATUS_ID = 2
                	AND amo.OPERATION_TYPE_CODE = 'C'
                	AND amo.AMOUNT >= 500
                '''.format(i)            
            oraOnce = pd.read_sql(ora_select,ConnectionOra)
            OraDF = OraDF.append(oraOnce)
        except Exception as err:
            print(err)
            pass
        
    
    ConnectionOra.close() 
    print("Db Oracle: Connection Closed") 
    ConnectionMySql.close() 
    print("DB MySQL: Connection Closed")     

    #Результат в файл   
    os.chdir('/data/scripts/dev/temp')
    request = (pd.merge(sqlDf, OraDF, on=['ENTITY_ID'], how="left"))
    request.to_csv(filename, sep = ';')
    #отправка на сервер
    a.delivery_to_server(filename, remotepath_part)

    #Параметры для письма на почту
    emails = ["aadrobin@mts.ru"]
    subject = "Регистрация с кодом MTSCB200"
    #zipFname = filename + datetime_now + '.csv' + '.zip'
    body_text = "Link to the file: " + 'http://10.73.44.17/Old/' + filename
    #Отправка на почту 
    a.send_email(emails, subject, body_text)













        