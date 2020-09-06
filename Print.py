# coding:utf8  
import sys  
import xlwt  
#import MySQLdb
import pymysql as MySQLdb
import datetime  

host = '127.0.0.1'  
user = 'root'  
pwd = '123456'  
db = 'parking_system'  
#sql = 'select * from parking_history_table'  
sheet_name = 'building'  
out_path = 'one.xls'

def printCarIfo(starttime,endtime,out_path=out_path):
    strstarttime = starttime.strftime("%Y-%m-%d %H:%M:%S")
    strendtime = endtime.strftime("%Y-%m-%d %H:%M:%S")
    sql = "select * from parking_history_table where history_entry_time>%s and history_out_time<%s"
    conn = MySQLdb.connect(host,user,pwd,db,charset='utf8')  
    cursor = conn.cursor()  
    count = cursor.execute(sql,(strstarttime,strendtime))  
    print(count)  

    #cursor.scroll(0,mode='absolute')  
    results = cursor.fetchall()  
    fields = cursor.description  
    workbook = xlwt.Workbook()  
    sheet = workbook.add_sheet(sheet_name,cell_overwrite_ok=True)  

    for field in range(0,len(fields)):  
        sheet.write(0,field,fields[field][0])  

    row = 1  
    col = 0  
    for row in range(1,len(results)+1):  
        for col in range(0,len(fields)):  
            sheet.write(row,col,u'%s'%results[row-1][col])  

    workbook.save(out_path)