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
print("\nOpen database successfully")
c = conn.cursor()

SQL_UPDATE_ONE_DATA = "UPDATE Data SET title = '{}', notes = '{}' , note_group = {} where created = '{}' "
SQL_DEL_ONE_DATA = "DELETE FROM Data where created ='{}'"
AGTT = True
STM = 0

with open('Automatically_get_the_time.txt', 'r') as file:
    if file.read() == '0':
        AGTT = False

with open('Sort_method.txt', 'r') as file:
    STM = int(file.read())

if not jud:
    c.execute('''
    CREATE TABLE IF NOT EXISTS Data
    (
        created TEXT PRIMARY KEY NOT NULL,
        title TEXT NOT NULL,
        notes TEXT NOT NULL,
        note_group INT
    );
    ''')
    print ("Creat database successfully")
    conn.commit()

def ERROR() :
	print ("Error")

def list_data():
    print()
    cursor = c.execute("SELECT created, title, notes, note_group FROM Data")  		# SELECT
    i = 1
    for row in cursor:
        print("id:", i)
        print("created:", row[0])
        print("title:", row[1], "\n")
        i += 1

def refresh():
    global index_max
    index_max = 0
    date = []
    cursor = c.execute("SELECT created,title,notes,note_group from Data")  			# SELECT
    for row in cursor:
        date.append(row[0])
        index_max += 1
    return date

def load():
    cursor = c.execute("SELECT created,title,notes,note_group from Data")
    data = [row[2] for row in cursor]
    return data

def read():

    refresh()
    i = 1
    res = []
    print()
    
    if STM == 1 :
        cursor = c.execute("SELECT created, title, notes, note_group FROM Data ORDER BY created ASC")
        print("Sort by time (Ascending order)\n")
    elif STM == 2 :
        cursor = c.execute("SELECT created, title, notes, note_group FROM Data ORDER BY created DESC")
        print("Sort by time (Descending order)\n")
    elif STM == 3 :
        cursor = c.execute("SELECT created, title, notes, note_group FROM Data ORDER BY note_group ASC")
        print("Sort by note_group (Ascending order)\n")
    elif STM == 4 :
        cursor = c.execute("SELECT created, title, notes, note_group FROM Data ORDER BY note_group DESC")
        print("Sort by note_group (Descending order)\n")

    for row in cursor:
        print("id:", i)
        print("create:", row[0])
        print("title:", row[1])
        print("note_group:", row[3], "\n")
        res.append(row[2])
        i += 1
    
    while True:
        n = input("Please input the note you want to read ([0]quit):   ")
        if n == '':
            ERROR()
            continue
        elif int(n) == 0:
            break
        elif int(n) > index_max:
            ERROR()
            continue
        print('\n' , res[int(n)-1] , '\n' , sep='')

def write() :
	while True :
		list1 = refresh()
		n = input("[0]Quit , [1]New Notes , [2]Edit Notes:   ")
		print()
		if n == '' :
			ERROR()
			continue
		n = int(n)

		if n == 1 :																	#write new notes
			if AGTT == True :
				time_temp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
			else :
				print("Please input the time you creat your notes:   \n")
				YY = input("[YY]:   ")
				MM = input("[MM](0X):   ")
				DD = input("[DD](0X):   ")
				HH = input("[HH](0X):   ")
				mm = input("[mm](0X):   ")
				SS = input("[SS](0X):   ")
				time_temp = YY + '-' + MM + '-' + DD + ' ' + HH + ':' + mm + ':' + SS
				print()
			
			file = open( "temp.txt", mode='x', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None)
			file.close()
			print("Please input your notes into this application and save")
			os.system('notepad temp.txt')
			file = open('temp.txt' , 'rb') 
			co = file.read()
			file.close()
			os.system('del /q temp.txt')
			tmp = co.decode('utf-8')
			temp = tmp[:8]
			n_g = int(input("Please input your notes's group:   "))
			c.execute("INSERT INTO Data (created,title,notes,note_group) \
    			VALUES ( ? , ? , ? , ? )" , ( time_temp , temp , tmp + '\n' + "Created: " + time_temp , n_g ))
			conn.commit()
			print("Write database successfully\n")
		
		elif n == 2 :																#edit
			list_data()
			n = int(input("Please input your notes' id which you want to edit:   "))

			if n > index_max :
				ERROR()
				continue

			list2 = load()
			tmp = list2[n-1]
			file = open( "temp.txt" , mode='wb' )
			file.write(tmp.encode(encoding='gbk'))
			file.close()
			os.system('notepad temp.txt')
			file = open('temp.txt' , 'r')
			co = file.read()														#notes
			file.close()
			os.system('del /q temp.txt')
			temp = co[:8]															#title
			n_g = int(input("Please input your notes's group:   "))

			if AGTT == True :
				time_temp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
			else :
				print("Please input the time you edit your notes:   ")
				YY = input("[YY]:   ")
				MM = input("[MM](0X):   ")
				DD = input("[DD](0X):   ")
				HH = input("[HH](0X):   ")
				mm = input("[mm](0X):   ")
				SS = input("[SS](0X):   ")
				time_temp = YY + '-' + MM + '-' + DD + ' ' + HH + ':' + mm + ':' + SS
				print()

			sql_update = SQL_UPDATE_ONE_DATA.format( temp , co + '\n' + "Edited:  " + time_temp , n_g , list1[n-1] )
			c.execute(sql_update)
			conn.commit()
			print("Edit notes successfully")
			print("Total number of rows updated:   " , conn.total_changes , '\n ')

		elif n == 0 :
			break
		
		else :
			ERROR()
		

def setting() :
	lang = input("\nPlease input the language you want to use: [1]EN , [2]CN :   ")
	print()
	if lang == '' :
		ERROR()

	elif lang == '1' :
		print("(Sort by time) [1]Ascending order , [2]Descending order")
		print("(Sort by note_group) [3]Ascending order , [4]Descending order\n")
		n = input("Please input the number you want to sort:   ")
		print()
		file = open("Sort_method.txt","w")
		file.write(n)
		file.close()
		m = input("Please input the method of getting the time [1]Automatically , [0]Manually :   ")
		file = open("Automatically_get_the_time.txt","w")
		file.write(m)
		file.close()

	elif lang == '2' :
		print("(按时间排序) [1]升序 , [2]降序")
		print("(按笔记分组) [3]升序 , [4]降序\n")
		n = input("请输入你选择的方式:   ")
		file = open("Sort_method.txt","w")
		file.write(n)
		file.close()
		m = input("要自动设置时间吗? [1]是, [0]否:   ")
		file = open("Automatically_get_the_time.txt","w")
		file.write(m)
		file.close()

	else :
		ERROR()

read()

while True :
	n = input("\n[0]Quit , [1]Read Notes , [2]Write Notes , [3]Delete Notes , [4]Setting:   ")
	print()
	if n == '' :
		ERROR()
		continue
	n = int(n)

	if n == 0 :
		break
	elif n == 1 :																	#Read
		read()
	elif n == 2 :																	#Write
		write()
	elif n == 3 :
		list_data()
		list2 = refresh()
		n = input("Please input your notes' id which you want to delete:   ")
		if n == '' :
			ERROR()
			continue
		n = int(n)
		if n > index_max :
			ERROR()
			continue
		sql_del = SQL_DEL_ONE_DATA.format(list2[n-1])
		c.execute(sql_del)
		m = (input("\nSure? [y/n]:   "))
		if m == 'y' :
			conn.commit()
			print("\nDelete notes successfully")
			print("Total number of rows deleted :" , conn.total_changes )
	elif n == 4 :
		setting()
		break
	else :
		ERROR()
		continue

conn.close()