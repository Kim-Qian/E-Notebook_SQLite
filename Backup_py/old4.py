'''
** 2023-07-5
** By Kim Qian
** The author disclaims copyright to this source code.  In place of
** a legal notice, here is a blessing:
**
**    May you do good and not evil.
**    May you find forgiveness for yourself and forgive others.
**    May you share freely, never taking more than you give.
**
*************************************************************************
'''

import sqlite3
import os
import time

jud = os.path.isfile("enotebook.db")
conn = sqlite3.connect('enotebook.db')
conn.text_factory = str
print("Open database successfully")
c = conn.cursor()
#index_max = 0
SQL_UPDATE_ONE_DATA = "UPDATE Data SET title = '{}', notes = '{}' , note_group = {} where created = '{}' "
SQL_DEL_ONE_DATA = "DELETE FROM Data where created ='{}'"

AGTT = True
file = open('Automatically_get_the_time.txt' , 'r')
if ( file.read() == '0' ):
	AGTT = False

if ( jud == False ) :
    c.execute('''CREATE TABLE Data
    	( created TEXT PRIMARY KEY     NOT NULL,
        title           TEXT    NOT NULL,
        notes           TEXT     NOT NULL,
        note_group      INT);''')
    print ("Creat database successfully")
    conn.commit()

def ERROR() :
	print ("Error")

def List() :
	cursor = c.execute("SELECT created,title,notes,note_group  from Data")		#SELECT
	i = 1
	print('')

	for row in cursor:
		print("id: " , i)
		print( "create: " , row[0])
		print("title: " , row[1] , "\n" )
		i += 1

def refresh() :
	global index_max
	index_max = 0
	date = []
	cursor = c.execute("SELECT created,title,notes,note_group  from Data")		#SELECT
	i = 1
	for row in cursor:
		date.insert(i,row[0])
		index_max += 1
		i += 1
	#print("--------\n" , index_max )
	return date

def load() :
	data = []
	cursor = c.execute("SELECT created,title,notes,note_group  from Data")		#SELECT
	i = 1

	for row in cursor:
		data.insert(i,row[2])
		i += 1

	return data


def Read() :
	refresh()
	cursor = c.execute("SELECT created,title,notes,note_group  from Data")		#SELECT
	i = 1
	res = []
	print("")
	for row in cursor:
		print("id :" , i)
		print( "create: " , row[0])
		#temp = 
		#temp = row[1].decode('gbk').encode('utf-8')
		print("title: " , row[1])
		res.insert(i,row[2])
		print("note_group: " , row[3], "\n")
		i += 1

	while True :
		n = input("Please input the note you want to read	([0]quit)\n")
		if ( n == '' ) :
			ERROR()
			continue
		elif ( int(n) == 0 ) :
			break
		elif ( int(n) > index_max ) :
			ERROR()
			continue
		print("\n" , res[int(n)-1] , sep = '' )

def Write() :
	while True :
		list1 = refresh()
		#print("index_max = " , index_max )
		n = input("[0]Quit , [1]New Notes , [2]Edit Notes\n")
		if ( n == '' ) :
			ERROR()
			continue
		n = int(n)
		if ( n == 1 ) :																#write new notes

			if ( AGTT == True ):
				time_temp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

			else :
				print("Please input the time you creat your notes\n")
				YY = input("[YY]\n")
				MM = input("[MM](0X)\n")
				DD = input("[DD](0X)\n")
				HH = input("[HH](0X)\n")
				mm = input("[mm](0X)\n")
				SS = input("[SS](0X)\n")
				time_temp = YY + '-' + MM + '-' + DD + ' ' + HH + ':' + mm + ':' + SS
			
			file = open( "temp.txt", mode='x', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None)
			file.close()
			print("Please input your notes into this application and save")
			os.system('notepad temp.txt')
			file = open('temp.txt' , 'rb') 
			co = file.read()
			tmp = co.decode('utf-8')
			temp = tmp[:8]
			n_g = int(input("please input your notes's group\n"))
			c.execute("INSERT INTO Data (created,title,notes,note_group) \
    			VALUES ( ? , ? , ? , ? )" , ( time_temp , temp , tmp + '\n' + "Created: " + time_temp , n_g ))
			conn.commit()
			print("Write database successfully")
			file.close()
			os.system('del /q temp.txt')
		
		elif ( n == 2 ) :															#edit
			List()
			n = int(input("please input your notes' id which you want to edit\n"))
			if ( n > index_max ) :
				ERROR()
				continue
			list2 = load()
			tmp = list2[n-1]
			file = open( "temp.txt" , mode='wb' )
			file.write(tmp.encode(encoding='gbk'))
			file.close()
			os.system('notepad temp.txt')
			file = open('temp.txt' , 'r')
			co = file.read()
			file.close()
			os.system('del /q temp.txt')
			#tmp2 = co.decode('utf-8')												#notes
			temp = co[:8]															#title
			n_g = int(input("please input your notes's group\n"))
			if ( AGTT == True ):
				time_temp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
			else :
				print("Please input the time you edit your notes\n")
				YY = input("[YY]\n")
				MM = input("[MM](0X)\n")
				DD = input("[DD](0X)\n")
				HH = input("[HH](0X)\n")
				mm = input("[mm](0X)\n")
				SS = input("[SS](0X)\n")
				time_temp = YY + '-' + MM + '-' + DD + ' ' + HH + ':' + mm + ':' + SS
			sql_update = SQL_UPDATE_ONE_DATA.format( temp , co + '\n' + "Edited:  " + time_temp , n_g , list1[n-1] )
			c.execute(sql_update)
			conn.commit()
			print("Edit notes successfully")
			print("Total number of rows updated :" , conn.total_changes , '\n ')

		elif ( n == 0 ) :
			break
		
		else :
			ERROR()
		
#Read()

while True :
	n = input("\n[0]Quit , [1]Read Notes , [2]Write Notes , [3]Delete Notes\n")
	if ( n == '' ) :
		ERROR()
		continue
	n = int(n)
	if ( n == 2 ) :																	#Write
		Write()
	elif ( n == 1 ) :																#Read
		Read()
	elif ( n == 3 ) :
		List()
		list2 = refresh()
		n = input("please input your notes' id which you want to delete\n")
		if ( n == '' ) :
			ERROR()
			continue
		n = int(n)
		if ( n > index_max ) :
			ERROR()
			continue
		sql_del = SQL_DEL_ONE_DATA.format(list2[n-1])
		c.execute(sql_del)
		m = (input("\nSure? [y/n]\n"))
		if ( m == 'y' ) :
			conn.commit()
			print("\nDelete notes successfully")
			print("Total number of rows deleted :" , conn.total_changes )
	elif ( n == 0 ) :
		break
	else :
		ERROR()
		continue
conn.close()