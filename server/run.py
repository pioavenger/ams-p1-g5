import os
import cherrypy
import json
import sqlite3 as sql
import random
import math

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

        emails = db.execute('SELECT email FROM members').fetchall()

        for mail in emails:
            if email == mail:
                return [{"error": "EMAIL_USED_ERROR"}]

        if password1 != password2:
            return [{"error": "PASSWORD_MISMATCH_ERROR"}]

        db.execute('INSERT INTO members(mname,email,password,carplate,role,mxpos,mypos,online,confirmed) VALUES (?,?,?,?,?,?,?,?,?)',(mname, email, password1, carplate, "Member", -1, -1, 0, 1))

        #send confirmation email

        pmid = db.execute('SELECT pmid FROM members WHERE email=?',(email,)).fetchone()[0]

        db.commit()
        db.close()

        return [{"error": "OK", "pmid": pmid, "mname": mname, "email": email, "password": password1, "carplate": carplate, "role": "Member", "mxpos": -1, "mypos": -1, "online": 0, "confirmed": 0}]

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def signin(self,email,password):
        db = sql.connect("database.db")

        emails = db.execute('SELECT email FROM members').fetchall()

        found = False
        for mail in emails:
            if email == mail:
                found = True
                break

        if not found:
            return [{"error": "USER_NOT_FOUND_ERROR"}]

        log_pass = db.execute('SELECT password FROM members WHERE email=?', (email,)).fetchone()[0]

        if password != log_pass:
            return [{"error": "INCORRECT_PASSWORD_ERROR"}]

        ison = db.execute('SELECT online FROM members WHERE email=?',(email,)).fetchone()[0]

        if ison == 1:
            return [{"error": "MEMBER_ALREADY_ONLINE_ERROR"}]

        db.execute('UPDATE members SET online=? WHERE email = ?',(1,email))

        mname = db.execute('SELECT mname FROM members WHERE email=?',(email,)).fetchone()[0]

	tmp_x = random.randint(1,1000)
	tmp_y = random.randint(1,1000)

	db.execute('UPDATE members SET mxpos=? AND mypos=? WHERE email=?',(tmp_x,tmp_y,email))

	conf = db.execute('SELECT confirmed FROM members WHERE email=?'(email,)).fetchone()[0]

        db.commit()
        db.close()

        # return [{"error": "OK", "mname": mname, "email": email, "password": password, "online": 1, "confirmed": conf}]
        # simplified for 1st delivery
        return [{"error": "OK", "mname": mname, "email": email}]

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def signout(self,email):
        db = sql.connect("database.db")

        ison = db.execute('SELECT online FROM members WHERE email=?',(email,)).fetchone()[0]

        if ison == 0:
            return [{"error": "MEMBER_ALREADY_OFFLINE_ERROR"}]

        db.execute('UPDATE members SET online=? WHERE email=?',(0,email))

        db.commit()
        db.close()

        return [{"error": "OK", "email": email, "online": 0}]

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def browse(self,email,filter_type,recent):

	# Sort types:
	# 0 - Price     - not yet implemented
	# 1 - Distance	- not yet implemented
	# 2 - Rating    - not yet implemented

	# Recent:
	# 0 - no
	# 1 - yes

	db = sql.connect("database.db")

	#add online check here		<---------------------------------------
	#add registry check here 	<---------------------------------------

	mxpos = db.execute('SELECT mxpos FROM members WHERE email=?',(email,)).fetchone()[0]
	mypos = db.execute('SELECT mypos FROM members WHERE email=?',(email,)).fetchone()[0]

	if recent == 1:
	    tmp_mid = db.execute('SELECT pmid FROM members WHERE email=?',(email,)).fetchone()[0]
	    recent_list = db.execute('SELECT sid FROM bookings WHERE terminated=? AND mid=?',(1,tmp_mid)).fetchall()

	    tmp_json = {"error": "OK", "email": email}
    	    sl_json = [] 

	    for space in recent_list:
		sp_info = db.execute('SELECT sxpos,sypos,cpmin,rating FROM spaces WHERE psid=?',(space[0],)).fetchone()

		tmp_dis = math.sqrt( (mxpos-sp_info[0])*(mxpos-sp_info[0]) + (mypos-sp_info[1])*(mypos-sp_info[1]) )

		ap_json = {"sid": space[0], "rating": float(sp_info[3]), "cpmin": sp_info[2], "distance": tmp_dis}
		sl_json.append(ap_json)

	    sl_json.reverse()
	    sl_json.append(tmp_json)

            db.close()

            return sl_json

	else:
	    if filter_type == 0:
		#filter by price

		sp_info = db.execute('SELECT psid,sxpos,sypos,cpmin,rating FROM spaces ORDER BY cpmin ASC').fetchall()
		tmp_json = {"error": "OK", "email": email}
    		sl_json = [] 

		for space in sp_info:
        	    tmp_dis = math.sqrt( (mxpos-space[1])*(mxpos-space[1]) + (mypos-space[2])*(mypos-space[2]) )

		    ap_json = {"sid": space[0], "rating": float(space[4]), "cpmin": space[3], "distance": tmp_dis}
		    sl_json.append(ap_json)

		sl_json.append(tmp_json)

		db.close()

		return sl_json

	    elif filter_type == 1:
		#filter by distance

		sp_info = db.execute('SELECT psid,sxpos,sypos,cpmin,rating FROM spaces').fetchall()

		sl_json = []
		tmp_json = {"error": "OK", "email": email}

		for space in sp_info:
		    tmp_dis = math.sqrt( (mxpos-space[1])*(mxpos-space[1]) + (mypos-space[2])*(mypos-space[2]) )

		    ap_json = {"sid": space[0], "rating": float(space[4]), "cpmin": space[3], "distance": tmp_dis}
		    sl_json.append(ap_json)

		sorted_distances = sorted(sl_json, key=lambda k: k['distance']) 
		sorted_distances.append(tmp_json)

		db.close()
		
		return sorted_distances

	    elif filter_type == 2:
		#filter by rating

		sp_info = db.execute('SELECT psid,sxpos,sypos,cpmin,rating FROM spaces').fetchall()		

		tmp_json = {"error": "OK", "email": email}
    	        sl_json = [] 

	        for space in sp_info:
		    tmp_dis = math.sqrt( (mxpos-space[1])*(mxpos-space[1]) + (mypos-space[2])*(mypos-space[2]) )

       		    ap_json = {"sid": space[0], "rating": float(space[4]), "cpmin": space[3], "distance": tmp_dis}
		    sl_json.append(ap_json)

		sorted_ratings = sorted(sl_json, key=lambda k: k['rating'])
		sorted_ratings.reverse()

	        sorted_ratings.append(tmp_json)

		db.close()

                return sorted_ratings

	    else:
		db.close()
		return [{"error": "WRONG_FILTER_ERROR"}]

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def book(self,email,cc,valid,save,use_saved,sid,book_time):
        db = sql.connect("database.db")

	#add online check here		  <---------------------------------------
	#add registry check here 	  <---------------------------------------
	#add confirmed account check here <---------------------------------------

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

        tmp_mid = db.execute('SELECT pmid FROM members WHERE email=?',email).fetchone()[0]

        if use_saved:
            saved_info = db.execute('SELECT mid,cc,valid FROM creditinfo').fetchall()

            for member in saved_info:
                if member[0] == tmp_mid:
                    #bank verifies cc here
                    #do the payment here

                    db.execute('UPDATE spaces SET free=? WHERE psid=?',(0,sid))
                    db.execute('INSERT INTO bookings(mid,sid,terminated) VALUES (?,?,?)',(tmp_mid,sid,0))

                    pid_free = db.execute('SELECT providers.ppid,providers.pfree FROM providers,bookings,spaces WHERE providers.ppid=spaces.pid AND spaces.psid=bookings.sid AND bookings.sid=? AND bookings.terminated=?',(sid,0)).fetchone()[0]
                    db.execute('UPDATE providers SET pfree=? WHERE ppid=?',(pid_free[1]-1,pid_free[0]))

                    db.commit()
                    db.close()

                    return [{"error": "OK", "mid": tmp_mid, "cc": cc, "valid": valid, "ppid": pid_free[0], "pfree": pid_free[1]}]

	    db.close()

	    return [{"error": "NO_SAVED_CREDITCARD_ERROR"}]

        if save:
            creditcards = db.execute('SELECT cc FROM creditinfo').fetchall()

            found = False
            for card in creditcards:
                if cc == card:
                    found = True
                    break

            if not found:
                emails = db.execute('SELECT members.email FROM members,creditinfo WHERE members.pmid = creditinfo.mid').fetchall()

                found = False
                for mail in emails:
                    if email == mail:
                        found = True
                        db.execute('UPDATE creditinfo SET cc=? AND valid=? WHERE mid=?',(cc,valid,tmp_mid))
                        break

                if not found:
                    db.execute('INSERT INTO creditinfo(mid,cc,valid) VALUES (?,?,?)',(tmp_mid,cc,valid))

	    else:
		scc_mid = db.execute('SELECT mid FROM creditinfo WHERE cc=?',(cc,)).fetchone()[0]	

		if scc_mid == tmp_mid:
		    db.close()
		    return [{"error": "CREDITCARD_ALREADY_SAVED_ERROR"}]

		else:
		    db.close()
		    return [{"error": "CREDITCARD_USED_BY_ANOTHER_MEMBER_ERROR"}]

        #bank verifies the cc here

	to_pay = db.execute('SELECT cpmin FROM spaces WHERE psid=?',(sid,)).fetchone()[0] * book_time	

        #bank does the payment here

        db.execute('UPDATE spaces SET free=? WHERE psid=?',(0,sid))
        db.execute('INSERT INTO bookings(mid,sid,terminated) VALUES (?,?,?)',(tmp_mid,sid,0))

        pid_free = db.execute('SELECT providers.ppid,providers.pfree FROM providers,bookings,spaces WHERE providers.ppid=spaces.pid AND spaces.psid=transactions.sid AND transactions.sid=? AND bookings.terminated=?',(sid,0)).fetchone()[0]
        db.execute('UPDATE providers SET pfree=? WHERE ppid=?',(pid_free[1]-1,pid_free[0]))

        db.commit()
        db.close()

        return [{"error": "OK", "mid": tmp_mid, "cc": cc, "valid": valid, "ppid": pid_free[0], "pfree": pid_free[1]}]

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def confacc(self,email):
	pass

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def updatedatabase(self,email):
	pass

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def checkdatabase(self,email):
	pass

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def sendnotification(self,email):
	pass

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def togglemaintenance(self,email):
	pass

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def managelogs(self,email):
	pass

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def changeperms(self):
	pass

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def confsystem(self,email):
	pass

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def togglesystem(self,email):
	pass

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
