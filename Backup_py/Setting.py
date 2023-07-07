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
import os

lang = input("Please input the language you want to use: [0]EN , [1]CN : ")
if ( lang == "0" ):
    print("(Sort by time) 0: Ascending order, 1: Descending order")
    print("(Sort by note_group) 2: Ascending order, 3: Descending order\n")
    n = input("Please input the number you want to sort: ")
    file = open("Sort_method.txt","w")
    file.write(n)
    file.close()
    m = input("Please input the method of getting the time [1]Automatically , [0]Manually :   ")
    file = open("Automatically_get_the_time.txt","w")
    file.write(m)
    file.close()
else :
    print("(按时间排序) 0: 升序,1: 降序")
    print("(按笔记分组) 2: 升序,3: 降序\n")
    n = input("请输入你选择的方式: ")
    file = open("Sort_method.txt","w")
    file.write(n)
    file.close()
    m = input("要自动设置时间吗? [1]是, [0]否:  ")
    file = open("Automatically_get_the_time.txt","w")
    file.write(m)
    file.close()