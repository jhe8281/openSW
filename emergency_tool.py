import json
import sqlite3
import bcrypt
import hashlib
import threading

from func import *
from mark import load_conn2, namumark

json_data = open('set.json').read()
set_data = json.loads(json_data)

conn = sqlite3.connect(set_data['db'] + '.db', check_same_thread = False)
curs = conn.cursor()

load_conn(conn)

print('1. backlink reset')
print('2. recaptcha delete')
print('3. ban delete')
print('4. change port')
print('5. change skin')
print('6. change password')
print('7. reset version')

print('select : ', end = '')
what_i_do = input()

if what_i_do == '1':
    def parser(data):
        namumark(data[0], data[1], 1)

    curs.execute("delete from back")
    conn.commit()

    curs.execute("select title, data from data")
    data = curs.fetchall()
    num = 0

    for test in data:
        num += 1

        t = threading.Thread(target = parser, args = [test])
        t.start()
        t.join()

        if num % 10 == 0:
            print(num)
elif what_i_do == '2':
    curs.execute("delete from other where name = 'recaptcha'")
    curs.execute("delete from other where name = 'sec_re'")
elif what_i_do == '3':
    print('ip or name : ', end = '')
    user_data = input()

    if re.search("^([0-9]{1,3}\.[0-9]{1,3})$", user_data):
        band = 'O'
    else:
        band = ''

        curs.execute("insert into rb (block, end, today, blocker, why, band) values (?, ?, ?, ?, ?, ?)", [user_data, load_lang('release', 1), get_time(), load_lang('tool', 1) + ':emergency', '', band])
    curs.execute("delete from ban where block = ?", [user_data])
elif what_i_do == '4':
    print('port : ', end = '')
    port = input()

    curs.execute("update other set data = ? where name = 'port'", [port])
elif what_i_do == '5':
    print('skin name : ', end = '')
    skin = input()

    curs.execute("update other set data = ? where name = 'skin'", [skin])
elif what_i_do == '6':
    print('1. sha256')
    print('2. bcrypt')
    print('select : ', end = '')
    what_i_do = input()

    print('user name : ', end = '')
    user_name = input()

    print('user password : ', end = '')
    user_pw = input()

    if what_i_do == '1':
        hashed = hashlib.sha256(bytes(user_pw, 'utf-8')).hexdigest()
    elif what_i_do == '2':
        hashed = bcrypt.hashpw(bytes(user_pw, 'utf-8'), bcrypt.gensalt()).decode()
       
    curs.execute("update user set pw = ? where id = ?", [hashed, user_name])
elif what_i_do == '7':
    curs.execute("update other set data = '00000' where name = 'ver'")

conn.commit()

print('ok')