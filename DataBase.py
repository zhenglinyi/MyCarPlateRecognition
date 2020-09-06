import pymysql.cursors
from datetime import datetime
class mysqlUtil(object):
#也可以使用参数进行初始化数据库连接self,host,user,password,db,port,charset
	def __init__(self):
		self.host="127.0.0.1"
		self.user="root"
		self.password="123456"
		self.db="parking_system"
		self.port=3306
		self.charset="utf8"
		self.connection=self.connection()
		if(self.connection):
			self.cursor=self.connection.cursor()
    #连接数据库
	def connection(self):
		connec=False
		try:
			connec=pymysql.Connect(
				host=self.host,
				user=self.user,
				password=self.password,
				db=self.db,
				port=self.port,
				charset=self.charset
			)
		except Exception as e:
			print(e)
			connec=False
		return connec
	#查询方法
	def querySql(self,sql):
		try:
			if sql != "":
				rows_count = self.cursor.execute(sql)
				self.connection.commit()
				if(rows_count > 0):
					return self.cursor.fetchall()
				else:
					return ""
		except Exception as e:
			print(e)
			return ""
	#添加方法
	def insertSql(self,sql,parameter=[]):
		try:
			if sql != '':
				self.cursor.execute(sql,parameter)
				self.connection.commit()
			return True
		except Exception as e:
			print (e)
			return False
	#修改方法
	def updateSql(self,sql):
		try:
			if sql != "":
				self.cursor.execute(sql)
				self.connection.commit()
			return "修改成功"
		except Exception as e:
			print(e)
		return "修改失败"
	#删除方法
	def deleteSql(self,sql):
		try:
			self.cursor.execute(sql)
			self.connection.commit()
			return True
		except Exception as e:
			print (e)
			return False
	#关闭连接
	def closeConnec(self):
		try:
			if type(self.cursor)=='object':
				self.cursor.close()
			if type(self.connection) =='object':
				self.connection.close()
				return True
		except Exception as e:
			print(e)
			return False

class Util():
#检查账号
	def check_password(self,username, password,is_admin):
		self.db = mysqlUtil()
		if(is_admin == True):
			sql = "select admin_password from admin_table where admin_name = \"" + username + "\""
			results = self.db.querySql(sql)
			self.db.closeConnec()
			if(results == ""):
				return False
			else:
				for row in results:  
					userpassword = row[0]
				if(userpassword == password):
					return True
				else:
					return False
		else:
			sql = "select tollman_password from tollman_table where tollman_name = \"" + username + "\""
			results = self.db.querySql(sql)
			self.db.closeConnec()
			if(results == ""):
				return False
			else:
				for row in results:  
					userpassword = row[0]
				if(userpassword == password):
					return True
				else:
					return False
#	car_number varchar(10),
#	entry_time datetime,
#入库
	def car_entry(self,car_number):
		self.db = mysqlUtil()
		nowtime = datetime.now()
		#str_to_date(\'%s\','%%Y-%%m-%%d %%H:%%i:%%s')
		sql = "select * from parking_car_table where car_number = \'" + car_number + "\'"
		results1 = self.db.querySql(sql)
		for row in results1 :  
			get_car_number = row[0]
			entry_time = row[1]
			if(get_car_number == car_number):
				self.db.closeConnec()
				return False
		else:
			sql = "insert into parking_car_table(car_number,entry_time) values(%s,%s)"
			a = [car_number,nowtime.strftime("%Y-%m-%d %H:%M:%S")]
			re1 = self.db.insertSql(sql,a)
			self.db.closeConnec()
			return re1
#	history_car_number varchar(10),
#	history_entry_time varchar(20),
#	history_out_time varchar(20),
#	history_parking_time int(10),
#	history_charge int(10)
#出库
	def car_out(self,car_number):
		self.db = mysqlUtil()
		nowtime = datetime.now()
		print(nowtime.strftime("%Y-%m-%d %H:%M:%S"))
		sql = "select * from parking_car_table where car_number = \'" + car_number + "\'"
		results1 = self.db.querySql(sql)
		for row in results1 :  
			car_number = row[0]
			entry_time = row[1]
		sql = "DELETE FROM parking_car_table WHERE car_number = \'" + car_number + "\'"
		self.db.deleteSql(sql)
		#str_to_date(\'%s\','%%Y-%%m-%%d %%H:%%i:%%s')
		#计算时间差和价格
		entrytime = datetime.strptime(entry_time, "%Y-%m-%d %H:%M:%S")
		print((nowtime-entrytime).seconds)
		second = (nowtime-entrytime).seconds
		days = (nowtime-entrytime).days
		hours = second//(60*60)
		minites = second%(60*60)//60
		parking_history_time = str(days) + "days " + str(hours) + "huors " + str(minites) + "minites"
#	lower60 int(10),
#	lower300 int(10),
#	higher300 int(10)
		chargetime = 0
		if(minites>0):
			chargetime = days * 24 + hours + 1
		else:
			chargetime = days * 24 + hours
		sql = "select * from charge_table"
		results2 = self.db.querySql(sql)
		for row in results2 :  
			lower60 = row[0]
			lower300 = row[1]
			higher300 = row[2]
		if(chargetime <= 1):
			history_charge = lower60
		elif(chargetime<=5):
			history_charge = lower60 + (chargetime-1) * lower300
		elif(chargetime>5):
			history_charge = lower60 + lower300 * 4 + (chargetime-5) * higher300
		print(history_charge)
		sql = "insert into parking_history_table(history_car_number,history_entry_time,history_out_time,history_parking_time,history_charge) values(%s,%s,%s,%s,%s)"
		a = [car_number,entry_time,nowtime.strftime("%Y-%m-%d %H:%M:%S"),parking_history_time,history_charge]
		self.db.insertSql(sql,a)
		self.db.closeConnec()
		return str(days) + "天 " + str(hours) + "小时" + str(minites) + "分钟", history_charge
#设置收费标准，小于1小时，大于1小时小于5小时部分，大于5小时部分
	def set_charge(self,lower60,lower300,higher300):
		self.db = mysqlUtil()
		sql = "select * from charge_table"
		results = self.db.querySql(sql)
		re1 = False
		re2 = False
		if(results == ""):
			sql = "INSERT INTO charge_table(lower60,lower300,higher300) VALUES (%s, %s, %s);"
			a = [lower60,lower300,higher300]
			re1 = self.db.insertSql(sql,a)
		else:
			for row in results :  
				lower60 = row[0]
			sql = "DELETE FROM charge_table WHERE lower60=" + str(lower60)
			print(self.db.deleteSql(sql))
			sql = "INSERT INTO charge_table(lower60,lower300,higher300) VALUES (%s, %s, %s);"
			a = [lower60,lower300,higher300]
			re2 = self.db.insertSql(sql,a)
		self.db.closeConnec()
		if(re1 or re2):
			return True
		else:
			return False

	def query_timecar(self,starttime,endtime):
		self.db = mysqlUtil()
		strstarttime = starttime.strftime("%Y-%m-%d %H:%M:%S")
		strendtime = endtime.strftime("%Y-%m-%d %H:%M:%S")
		sql = "select * from parking_history_table";
		results = self.db.querySql(sql)
		car_count = 0
		charge = 0
		for row in results :  
			car_number = row[0]
			entry_time = row[1]
			out_time = row[2]
			car_charge = row[4]
			if(entry_time>=strstarttime and out_time<=strendtime):
				car_count = car_count + 1
				charge = charge + car_charge
		self.db.closeConnec()
		print(car_count)
		print(charge)
		return car_count,charge
# #测试

# a=datetime.now()
# print('当前时间：',a)
# db = mysqlUtil()
# #插入测试
# #print("------插入测试---------")
# #sql1 = "INSERT INTO admin_table(admin_id,admin_password,admin_name) VALUES (%s, %s, %s);"
# #a = ["18","123456","admin"]
# #db.insertSql(sql1,a)

# #sql12 = "INSERT INTO tollman_table(tollman_id,tollman_password,tollman_name) VALUES (%s, %s, %s);"
# #b = ["18","123456","Alx"]
# #db.insertSql(sql12,b)
# #查询测试
# #print("------查询测试---------")
# #sql2 = "select * from admin_table"  
# #results = db.querySql(sql2)
# #print("admin_id","admin_password","admin_name")  
# ##遍历结果  
# #for row in results :  
# #	id = row[0]  
# #	name = row[1]  
# #	password = row[2]  
# #	print(id,name,password)
# #删除测试
# #print("------删除测试---------")
# #sql3 = "DELETE FROM admin_table WHERE admin_id=\"18\"" 
# #db.deleteSql(sql3)
# #print(db.insertSql(sql1,a))
# #results = db.querySql(sql2)
# #print("admin_id","admin_password","admin_name")  
# ##遍历结果  
# #for row in results :  
# #	id = row[0]  
# #	name = row[1]  
# #	password = row[2]  
# #	print(id,name,password)
# #db.closeConnec()
# #check_password测试
# print("------check_password测试---------")
# ut = Util()
# t1 = ut.check_password("admin","123456",True)
# if(t1 == True):
# 	print("yes")
# else:
# 	print("no")
# t2 = ut.check_password("Alx","123456",False)
# if(t2 == True):
# 	print("yes")
# else:
# 	print("no")
# ut.set_charge(11,9,7)
# #测试car_entry
# print("------car_entry测试---------")
# ut.car_entry("113")
# #测试car_out
# print("------car_out测试---------")
# ut.car_out("113")
# #测试set_charge
# print("------set_charge测试---------")
# ut.set_charge(10,9,7)
# #测试query_timecar
# print("------query_timecar测试------")
# stime = datetime(2019, 10, 22, 0, 0, 0)
# print(stime)
# etime = datetime(2019, 10, 23, 0, 0, 0)
# print(etime)
# ut.query_timecar(stime,etime)