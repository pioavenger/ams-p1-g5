import os
import cherrypy
import json
import sqlite3 as sql

class App(object):

    def __init__(self):
        pass

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def signup(self,mname,password1,password2,email,carplate):
        mail_sections1 = email.split('@')
        if len(mail_sections1) == 1 or mail_sections1[0] == "": 
            return [{"error": "WRONG_EMAIL_FORMAT_ERROR"}]
        mail_sections2 = mail_sections1[1].split('.')
        
        for char in mail_sections2[0]:
            if not char.isalpha():
                return [{"error": "WRONG_EMAIL_FORMAT_ERROR"}]
        
        for char in mail_sections2[1]:
            if not char.isalpha():
                return [{"error": "WRONG_EMAIL_FORMAT_ERROR"}]

        carplate_sections = carplate.split('-')

        for char in carplate_sections[0]:
            if not char.isalnum():
                return [{"error": "WRONG_CARPLATE_FORMAT_ERROR"}]

        for char in carplate_sections[1]:
            if not char.isalnum():
                return [{"error": "WRONG_CARPLATE_FORMAT_ERROR"}]

        for char in carplate_sections[2]:
            if not char.isalnum():
                return [{"error": "WRONG_CARPLATE_FORMAT_ERROR"}]

        db = sql.connect("database.db")

        emails = db.execute('SELECT email FROM members')

        for mail in emails:
            if email == mail:
                return [{"error": "EMAIL_USED_ERROR"}]

        if password1 != password2:
            return [{"error": "PASSWORD_MISMATCH_ERROR"}]

        db.execute('INSERT INTO members(mname,email,password,carplate,role,online,confirmed) VALUES (?,?,?,?,?,?,?)',(mname, email, password1, carplate, "Member", 0, 1))

        #send confirmation email

        # pmid = db.execute('SELECT pmid FROM members WHERE email=?',(email,))

        db.commit()
        db.close()

        #return [{"error": "OK", "pmid": pmid, "mname": mname, "email": email, "password": password1, "carplate": carplate, "role": "Member", "online": 0, "confirmed": 0}]
        # simplified for 1st delivery
        return [{"error": "OK", "mname": mname, "email": email}]

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def signin(self,email,password):
        db = sql.connect("database.db")

        emails = db.execute('SELECT email FROM members')

        found = False
        for mail in emails:
            if email == mail[0]:
                found = True
                break

        if not found:
            return [{"error": "USER_NOT_FOUND_ERROR"}]

        log_pass = db.execute('SELECT password FROM members WHERE email=?', (email,))

        if password != log_pass.fetchone()[0]:
            return [{"error": "INCORRECT_PASSWORD_ERROR"}]

        ison = db.execute('SELECT online FROM members WHERE email=?',(email,))

        if ison.fetchone()[0] == 1:
            return [{"error": "MEMBER_ALREADY_ONLINE_ERROR"}]

        db.execute('UPDATE members SET online=? WHERE email = ?',(1,email))

        mname = db.execute('SELECT mname FROM members WHERE email=?',(email,)).fetchone()[0];

        db.commit()
        db.close()

        # return [{"error": "OK", "email": email, "password": password,}]
        # simplified for 1st delivery
        return [{"error": "OK", "mname": mname, "email": email}]

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def signout(self,email):
        db = sql.connect("database.db")

        ison = db.execute('SELECT online FROM members WHERE email=?',(email,))

        if ison.fetchone()[0] == 0:
            return [{"error": "MEMBER_ALREADY_OFFLINE_ERROR"}]

        db.execute('UPDATE members SET online=? WHERE email=?',(0,email))

        db.commit()
        db.close()

        return [{"error": "OK"}]

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def browse(self,email,sort_type,recent):

	# Sort types:
	# 0 - Price     - not yet implemented
	# 1 - Distance	- not yet implemented
	# 2 - Rating    - not yet implemented

	# Recent:
	# 0 - no
	# 1 - yes

	db = sql.connect("database.db")








    @cherrypy.expose
    @cherrypy.tools.json_out()
    def book(self,email,cc,valid,save,use_saved,sid):
        db = sql.connect("database.db")

        digit_count = 0
        for number in cc:
            digit_count += 1
            if not number.isdigit():
                return [{"error": "WRONG_CREDITCARD_FORMAT_ERROR"}]

        if digit_count != 16:
            return [{"error": "WRONG_CREDITCARD_FORMAT_ERROR"}]

        valid_sections = valid.split('/')

        for number in valid_sections[0]:
            if not number.isdigit():
                return [{"error": "WRONG_VALIDITY_FORMAT_ERROR"}]

        for number in valid_sections[1]:
            if not number.isdigit():
                return [{"error": "WRONG_VALIDITY_FORMAT_ERROR"}]

        if int(valid_sections[0]) > 12 or int(valid_sections[0]) < 1:
            return [{"error": "WRONG_VALIDITY_FORMAT_ERROR"}]

        tmp_mid = db.execute('SELECT pmid FROM members WHERE email=?',email)

        if use_saved:
            saved_info = db.execute('SELECT mid,cc,valid FROM creditinfo')

            for member in saved_info:
                if member[0] == tmp_mid:
                    #bank verifies cc here
                    #do the payment here

                    db.execute('UPDATE spaces SET free=? WHERE psid=?',(0,sid))
                    db.execute('INSERT INTO bookings(mid,sid) VALUES (?,?)',(tmp_mid,sid))

                    pid_free = db.execute('SELECT providers.ppid,providers.pfree FROM providers,bookings,spaces WHERE providers.ppid=spaces.pid AND spaces.psid=transactions.sid AND transactions.sid=?',sid)
                    db.execute('UPDATE providers SET pfree=? WHERE ppid=?',(pid_free[1]-1,pid_free[0]))

                    db.commit()
                    db.close()

                    return [{"error": "OK", "mid": tmp_mid, "cc": cc, "valid": valid, "ppid": pid_free[0], "pfree": pid_free[1]}]

	    return [{"error": "NO_SAVED_CREDITCARD_ERROR"}]

        if save:
            creditcards = db.execute('SELECT cc FROM creditinfo')

            found = False
            for card in creditcards:
                if cc == card:
                    found = True
                    break

            if not found:
                emails = db.execute('SELECT members.email FROM members,creditinfo WHERE members.pmid = creditinfo.mid')

                found = False
                for mail in emails:
                    if email == mail:
                        found = True
                        db.execute('UPDATE creditinfo SET cc=? AND valid=? WHERE mid=?',(cc,valid,tmp_mid))
                        break

                if not found:
                    db.execute('INSERT INTO creditinfo(mid,cc,valid) VALUES (?,?,?)',(tmp_mid,cc,valid))

        #bank verifies cc here
        #do the payment here

        db.execute('UPDATE spaces SET free=? WHERE psid=?',(0,sid))
        db.execute('INSERT INTO bookings(mid,sid) VALUES (?,?)',(tmp_mid,sid))

        pid_free = db.execute('SELECT providers.ppid,providers.pfree FROM providers,bookings,spaces WHERE providers.ppid=spaces.pid AND spaces.psid=transactions.sid AND transactions.sid=?',sid)
        db.execute('UPDATE providers SET pfree=? WHERE ppid=?',(pid_free[1]-1,pid_free[0]))

        db.commit()
        db.close()

        return [{"error": "OK", "mid": tmp_mid, "cc": cc, "valid": valid, "ppid": pid_free[0], "pfree": pid_free[1]}]

config={
        '/': {
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './static'
        }
}

import sys
ip = "127.0.0.1"
port = 8000
if len(sys.argv) == 2:
    ip = sys.argv[1]
elif len(sys.argv) == 3:
    ip = sys.argv[1]
    port = int(sys.argv[2])

cherrypy.config.update({'server.socket_host': ip,
                        'server.socket_port': port,
                       })

cherrypy.quickstart(App(), "/",config)
