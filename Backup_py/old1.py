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
print("Open database successfully")
c = conn.cursor()
SQL_UPDATE_ONE_DATA = "UPDATE Data SET title = '{}', notes = '{}' , note_group = {} where created = '{}' "
SQL_DEL_ONE_DATA = "DELETE FROM Data where created ='{}'"

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

def Read() :
	cursor = c.execute("SELECT created,title,notes,note_group  from Data")		#SELECT
	i = 1
	res = []
	print("")
	for row in cursor:
		print("id :" , i)
		print( "create: " , row[0])
		print("title: " , row[1])
		res.insert(i,row[2])
		print("note_group: " , row[3], "\n")
		i += 1
	while True :
		n = input("Please input the note you want to read	([0]quit)\n")
		if ( int(n) == 0 ) :
			break
		print("\n" , res[int(n)] , sep = '' )

def List() :
	cursor = c.execute("SELECT created,title,notes,note_group  from Data")		#SELECT
	i = 1
	print('')
	for row in cursor:
		print("id: " , i)
		print( "create: " , row[0])
		print("title: " , row[1] , "\n" )
		i += 1

def update() :
	date = []
	cursor = c.execute("SELECT created,title,notes,note_group  from Data")		#SELECT
	i = 1
	for row in cursor:
		date.insert(i,row[0])
		print("------------")
		print("i:" , i , "row:" , row[0] , "date:" , date )
		i += 1
	return date

def Write() :
	n = int(input("[1]New Notes , [2]Edit Notes\n"))
	list1 = update()
	print ("\n" , list1)

	if ( n == 1 ) :																#write new notes
		t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		co = input("Please input your notes\n")
		temp = co[:8]
		n_g = int(input("please input your notes's group\n"))
		c.execute("INSERT INTO Data (created,title,notes,note_group) \
    		VALUES ( ? , ? , ? , ? )" , ( t , temp , co , n_g ))
		conn.commit()
		print("Write database successfully")

	elif ( n == 2 ) :															#update
		List()
		n = int(input("please input your notes' id which you want to edit\n"))
		co = input("Please input your notes\n")
		temp = co[:8]
		n_g = int(input("please input your notes's group\n"))
		#print("date=" , date)
		sql_update = SQL_UPDATE_ONE_DATA.format( temp , co , n_g , list1[n-1] )
		c.execute(sql_update)
		conn.commit()
		print("Edit notes successfully")
		print("Total number of rows updated :" , conn.total_changes , '\n ')
	else :
		ERROR()
		
#Read()

while True :
	n = int(input("\n[0]Quit , [1]Read Notes , [2]Write Notes , [3]Delete Notes\n"))
	if ( n == 2 ) :																	#Write
		Write()
	elif ( n == 1 ) :																#Read
		Read()
	elif ( n == 3 ) :
		List()
		list2 = update()
		n = int(input("please input your notes' id which you want to delete\n"))
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
conn.close()