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

        if len(mail_sections1) != 2 or mail_sections1[0] == "" or mail_sections1[1] == "":
            return [{"error": "WRONG_EMAIL_FORMAT_ERROR"}]

        mail_sections2 = mail_sections1[1].split('.')

        if not mail_sections2[0].isalpha():
            return [{"error": "WRONG_EMAIL_FORMAT_ERROR"}]

        if not mail_sections2[0].isalpha():
            return [{"error": "WRONG_EMAIL_FORMAT_ERROR"}]

        carplate_sections = carplate.split('-')

        if not carplate_sections[0].isalnum():
            return [{"error": "WRONG_CARPLATE_FORMAT_ERROR"}]

        if not carplate_sections[1].isalnum():
            return [{"error": "WRONG_CARPLATE_FORMAT_ERROR"}]

        if not carplate_sections[2].isalnum():
            return [{"error": "WRONG_CARPLATE_FORMAT_ERROR"}]

        db = sql.connect("database.db")

        emails = db.execute('SELECT * FROM members WHERE email=?',(email,)).fetchall()

        if len(emails) == 1:
	    return [{"error": "EMAIL_USED_ERROR"}]
	elif len(emails) > 1:
	    return [{"error": "EMAIL_DATABASE_ERROR"}]

        if password1 != password2:
            return [{"error": "PASSWORD_MISMATCH_ERROR"}]

        db.execute('INSERT INTO members(mname,email,password,carplate,role,mxpos,mypos,online,confirmed) VALUES (?,?,?,?,?,?,?,?,?)',(mname, email, password1, carplate, "Member", -1, -1, 0, 0))

	self.api_confacc(email)

        pmid = db.execute('SELECT pmid FROM members WHERE email=?',(email,)).fetchone()[0]

        db.commit()
        db.close()

        return [{"error": "OK", "pmid": pmid, "mname": mname, "email": email, "password": password1, "carplate": carplate, "role": "Member", "mxpos": -1, "mypos": -1, "online": 0, "confirmed": 0}]

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def signin(self,email,password):
        db = sql.connect("database.db")

        m_info = db.execute('SELECT password,online FROM members WHERE email=?',(email,)).fetchall()

	if len(m_info) == 0:
	    return [{"error": "INCORRECT_EMAIL_ERROR"}]
	elif len(m_info) > 1:
	    return [{"error": "EMAIL_DATABASE_ERROR"}]

        if password != m_info[0][0]:
            return [{"error": "INCORRECT_PASSWORD_ERROR"}]

        if m_info[0][1] == 1:
            return [{"error": "MEMBER_ALREADY_ONLINE_ERROR"}]
	elif m_info[0][1] != 0:
	    return [{"error": "ISON_DATABASE_ERROR"}]

        db.execute('UPDATE members SET online=? WHERE email = ?',(1,email))

        mname = db.execute('SELECT mname FROM members WHERE email=?',(email,)).fetchone()[0]

	tmp_x, tmp_y = self.randomxy()

	db.execute('UPDATE members SET mxpos=? AND mypos=? WHERE email=?',(tmp_x,tmp_y,email))
	conf = db.execute('SELECT confirmed FROM members WHERE email=?',(email,)).fetchone()[0]

        db.commit()
        db.close()

        return [{"error": "OK", "mname": mname, "email": email, "password": password, "mxpos": tmp_x, "mypos": tmp_y, "online": 1, "confirmed": conf}]

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def signout(self,email):
        db = sql.connect("database.db")

	m_info = db.execute('select online from members where email=?',(email,)).fetchall()

	if len(m_info) == 0:
	    return [{"error": "INCORRECT_EMAIL_ERROR"}]
	elif len(m_info) > 1:
	    return [{"error": "EMAIL_DATABASE_ERROR"}]

        if m_info[0][0] == 0:
            return [{"error": "MEMBER_ALREADY_OFFLINE_ERROR"}]
	elif m_info[0][0] != 1:
	    return [{"error": "ISON_DATABASE_ERROR"}]

        db.execute('UPDATE members SET online=? WHERE email=?',(0,email))

        db.commit()
        db.close()

        return [{"error": "OK", "email": email, "online": 0}]

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def browse(self,email,filter_type,recent):
        filter_type = int(filter_type)
	# Sort types:
	# 0 - Price
	# 1 - Distance
	# 2 - Rating

	# Recent:
	# 0 - no
	# 1 - yes

	db = sql.connect("database.db")

	tmp_member = db.execute('SELECT online FROM members WHERE email=?',(email,)).fetchall()

	if len(tmp_member) == 0:
	    return [{"error": "EMAIL_NOT_REGISTERED_ERROR"}]
	elif len(tmp_member) > 1:
	    return [{"error": "EMAIL_DATABASE_ERROR"}]

	if tmp_member[0][0] == 0:
	    return [{"error": "MEMBER_OFFLINE_ERROR"}]
	elif tmp_member[0][0] != 1:
	    return [{"error": "ISON_DATABASE_ERROR"}]

	#if not str(filter_type).isnumeric():
	#    return [{"error": "WRONG_FILTER_ERROR"}]

	if int(filter_type) < 0 or int(filter_type) > 2:
	    return [{"error": "WRONG_FILTER_ERROR"}]

	#if not str(recent).isnumeric():
	#    return [{"error": "WRONG_RECENT_ERROR"}]

	#if int(recent) != 0 or int(recent) != 1:
	#    return [{"error": "WRONG_RECENT_ERROR"}]

	mxpos, mypos = db.execute('SELECT mxpos,mypos FROM members WHERE email=?',(email,)).fetchone()

	if int(recent) == 1:
	    #sort by recent

	    tmp_mid = db.execute('SELECT pmid FROM members WHERE email=?',(email,)).fetchone()[0]
	    recent_list = db.execute('SELECT sid FROM bookings WHERE terminated=? AND mid=?',(1,tmp_mid)).fetchall()

	    tmp_json = {"error": "OK", "email": email}
    	    sl_json = []

	    for space in recent_list:
		sp_info = db.execute('SELECT pid,sxpos,sypos,cpmin,rating FROM spaces WHERE psid=?',(space[0],)).fetchone()

		tmp_dis = math.sqrt( (mxpos-sp_info[1])*(mxpos-sp_info[1]) + (mypos-sp_info[2])*(mypos-sp_info[2]) )
                tmp_dis = int(tmp_dis)
		prov = db.execute('SELECT providers.pname FROM providers,spaces WHERE providers.ppid=spaces.pid AND spaces.pid=?',(space[0],)).fetchone()[0]
		ap_json = {"sid": space[0], "provider": prov,"rating": float(sp_info[4]), "cpmin": sp_info[3], "distance": tmp_dis}
		sl_json.append(ap_json)

	    sl_json.reverse()

            response = {}
            response["sl"] = sl_json
            response["email"] = tmp_json["email"]
            response["error"] = tmp_json["error"]

            db.close()

            return response

	else:
	    if int(filter_type) == 0:
		#filter by price

		sp_info = db.execute('SELECT psid,pid,sxpos,sypos,cpmin,rating FROM spaces ORDER BY cpmin ASC').fetchall()
		tmp_json = {"error": "OK", "email": email}
    		sl_json = []

		for space in sp_info:
        	    tmp_dis = math.sqrt( (mxpos-space[2])*(mxpos-space[2]) + (mypos-space[3])*(mypos-space[3]) )
                    tmp_dis = int(tmp_dis)
		    prov = db.execute('SELECT providers.pname FROM providers,spaces WHERE providers.ppid=spaces.pid AND spaces.pid=?',(space[1],)).fetchone()[0]
		    ap_json = {"sid": space[0], "provider": prov, "rating": float(space[5]), "cpmin": space[4], "distance": tmp_dis}
		    sl_json.append(ap_json)

                response = {}
                response["sl"] = sl_json
                response["email"] = tmp_json["email"]
                response["error"] = tmp_json["error"]

                db.close()

		return response

	    elif int(filter_type) == 1:
		#filter by distance

		sp_info = db.execute('SELECT psid,pid,sxpos,sypos,cpmin,rating FROM spaces').fetchall()

		sl_json = []
		tmp_json = {"error": "OK", "email": email}

		for space in sp_info:
		    tmp_dis = math.sqrt( (mxpos-space[2])*(mxpos-space[2]) + (mypos-space[3])*(mypos-space[3]) )
                    tmp_dis = int(tmp_dis)
		    prov = db.execute('SELECT providers.pname FROM providers,spaces WHERE providers.ppid=spaces.pid AND spaces.pid=?',(space[1],)).fetchone()[0]
		    ap_json = {"sid": space[0], "provider": prov, "rating": float(space[5]), "cpmin": space[4], "distance": tmp_dis}
		    sl_json.append(ap_json)

		sorted_distances = sorted(sl_json, key=lambda k: k['distance'])

                response = {}
                response["sl"] = sorted_distances
                response["email"] = tmp_json["email"]
                response["error"] = tmp_json["error"]

		db.close()

		return response

	    elif int(filter_type) == 2:
		#filter by rating

		sp_info = db.execute('SELECT psid,pid,sxpos,sypos,cpmin,rating FROM spaces').fetchall()

		tmp_json = {"error": "OK", "email": email}
    	        sl_json = []

	        for space in sp_info:
		    tmp_dis = math.sqrt( (mxpos-space[2])*(mxpos-space[2]) + (mypos-space[3])*(mypos-space[3]) )
                    tmp_dis = int(tmp_dis)
		    prov = db.execute('SELECT providers.pname FROM providers,spaces WHERE providers.ppid=spaces.pid AND spaces.pid=?',(space[1],)).fetchone()[0]
       		    ap_json = {"sid": space[0], "provider": prov, "rating": float(space[5]), "cpmin": space[4], "distance": tmp_dis}
		    sl_json.append(ap_json)

		sorted_ratings = sorted(sl_json, key=lambda k: k['rating'])
		sorted_ratings.reverse()

                response = {}
                response["sl"] = sorted_ratings
                response["email"] = tmp_json["email"]
                response["error"] = tmp_json["error"]

		db.close()

                return response

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def book(self,email,cc,valid,save,use_saved,sid,book_time):
        db = sql.connect("database.db")

	tmp_member = db.execute('SELECT online,confirmed FROM members WHERE email=?',(email,)).fetchall()

	if len(tmp_member) == 0:
	    return [{"error": "EMAIL_NOT_REGISTERED_ERROR"}]
	elif len(tmp_member) > 1:
	    return [{"error": "EMAIL_DATABASE_ERROR"}]

	if tmp_member[0][0] == 0:
	    return [{"error": "MEMBER_OFFLINE_ERROR"}]
	elif tmp_member[0][0] != 1:
	    return [{"error": "ISON_DATABASE_ERROR"}]

	if tmp_member[0][1] == 0:
	    return [{"error": "NOT_CONFIRMED_ERROR"}]
	elif tmp_member[0][1] != 1:
	    return [{"error": "CONF_DATABASE_ERROR"}]

	if len(cc) != 16:
            return [{"error": "WRONG_CREDITCARD_FORMAT_ERROR"}]

        if not cc.isnumeric():
            return [{"error": "WRONG_CREDITCARD_FORMAT_ERROR"}]

        valid_sections = valid.split('/')

        if not valid_sections[0].isnumeric():
            return [{"error": "WRONG_VALIDITY_FORMAT_ERROR"}]

        if not valid_sections[1].isnumeric():
            return [{"error": "WRONG_VALIDITY_FORMAT_ERROR"}]

        if int(valid_sections[0]) > 12 or int(valid_sections[0]) < 1:
            return [{"error": "WRONG_VALIDITY_FORMAT_ERROR"}]

	if not str(save).isnumeric():
	    return [{"error": "WRONG_SAVE_ERROR"}]

	if not str(use_saved).isnumeric():
	    return [{"error": "WRONG_USESAVED_ERROR"}]

	if int(save) != 0 and int(save) != 1:
	    return [{"error": "WRONG_SAVE_ERROR"}]

	if int(use_saved) != 0 and int(use_saved) != 1:
	    return [{"error": "WRONG_USESAVED_ERROR"}]

	if not str(book_time).isnumeric():
	    return [{"error": "WRONG_BOOKTIME_ERROR"}]

	if int(book_time) < 0:
	    return [{"error": "WRONG_BOOKTIME_ERROR"}]

	if not str(sid).isnumeric():
	    return [{"error": "WRONG_SID_ERROR"}]

	if int(sid) < 0:
	    return [{"error": "WRONG_SID_ERROR"}]

        tmp_mid = db.execute('SELECT pmid FROM members WHERE email=?',email).fetchone()[0]

        if int(use_saved):
            saved_info = db.execute('SELECT mid,cc,valid FROM creditinfo').fetchall()

            for member in saved_info:
                if member[0] == tmp_mid:
                    #bank verifies cc here
                    #do the payment here

                    db.execute('UPDATE spaces SET free=? WHERE psid=?',(0,int(sid)))
                    db.execute('INSERT INTO bookings(mid,sid,terminated) VALUES (?,?,?)',(tmp_mid,int(sid),0))

                    pid_free = db.execute('SELECT providers.ppid,providers.pfree FROM providers,bookings,spaces WHERE providers.ppid=spaces.pid AND spaces.psid=bookings.sid AND bookings.sid=? AND bookings.terminated=?',(int(sid),0)).fetchone()
                    db.execute('UPDATE providers SET pfree=? WHERE ppid=?',(pid_free[1]-1,pid_free[0]))

                    db.commit()
                    db.close()

                    return [{"error": "OK", "mid": tmp_mid, "cc": cc, "valid": valid, "ppid": pid_free[0], "pfree": pid_free[1]}]

	    db.close()

	    return [{"error": "NO_SAVED_CREDITCARD_ERROR"}]

        if int(save):
            creditcards = db.execute('SELECT cc FROM creditinfo').fetchall()

            found = False
            for card in creditcards:
                if cc == card[0]:
                    found = True
                    break

            if not found:
                emails = db.execute('SELECT members.email FROM members,creditinfo WHERE members.pmid = creditinfo.mid').fetchall()

                found = False
                for mail in emails:
                    if email == mail[0]:
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

	to_pay = db.execute('SELECT cpmin FROM spaces WHERE psid=?',(int(sid),)).fetchone()[0] * int(book_time)

        #bank does the payment here

        db.execute('UPDATE spaces SET free=? WHERE psid=?',(0,int(sid)))
        db.execute('INSERT INTO bookings(mid,sid,terminated) VALUES (?,?,?)',(tmp_mid,int(sid),0))

        pid_free = db.execute('SELECT providers.ppid,providers.pfree FROM providers,bookings,spaces WHERE providers.ppid=spaces.pid AND spaces.psid=transactions.sid AND transactions.sid=? AND bookings.terminated=?',(int(sid),0)).fetchone()
        db.execute('UPDATE providers SET pfree=? WHERE ppid=?',(pid_free[1]-1,pid_free[0]))

        db.commit()
        db.close()

        return [{"error": "OK", "mid": tmp_mid, "cc": cc, "valid": valid, "ppid": pid_free[0], "pfree": pid_free[1]}]

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def updatedatabase(self,email,sid,field,data):

	# Fields:
	# 0 - sxpos
	# 1 - sypos
	# 2 - cpmin
	# 3 - free

	db = sql.connect("database.db")

	tmp_prov = db.execute('SELECT role,confirmed FROM members WHERE email=?',(email,)).fetchall()

	if len(tmp_prov) == 0:
	    return [{"error": "EMAIL_NOT_REGISTERED_ERROR"}]
	elif len(tmp_prov) > 1:
	    return [{"error": "EMAIL_DATABASE_ERROR"}]

	if tmp_prov[0][1] == 0:
	    return [{"error": "NOT_CONFIRMED_ERROR"}]
	elif tmp_prov[0][1] != 1:
	    return [{"error": "CONF_DATABASE_ERROR"}]

	if tmp_prov[0][0] != "Provider":
	    return [{"error": "PERMISSION_DENIED_ERROR"}]

	if not str(field).isnumeric():
	    return [{"error": "WRONG_FIELD_ERROR"}]

	if int(field) < 0 or int(field) > 3:
	    return [{"error": "WRONG_FIELD_ERROR"}]

	if not str(sid).isnumeric():
	    return [{"error": "WRONG_SID_ERROR"}]

	if int(sid) < 0:
	    return [{"error": "WRONG_SID_ERROR"}]

	if not str(data).isnumeric():
	    return [{"error": "WRONG_DATA_ERROR"}]

	if int(data) < 0:
	    return [{"error": "WRONG_DATA_ERROR"}]

	if int(field) == 0:
	    #update sxpos

	    try:
		int(data)
	    except ValueError:
		return [{"error": "WRONG_DATA_ERROR"}]

	    db.execute('UPDATE spaces SET sxpos=? WHERE sid=?',(int(data),int(sid)))
	    db.commit()
	    db.close()
	    return [{"error": "OK", "email": email, "sid": sid, "sxpos": int(data)}]

	elif int(field) == 1:
	    #update sypos

	    try:
		int(data)
	    except ValueError:
		return [{"error": "WRONG_DATA_ERROR"}]

	    db.execute('UPDATE spaces SET sypos=? WHERE sid=?',(int(data),int(sid)))
	    db.commit()
	    db.close()
	    return [{"error": "OK", "email": email, "sid": sid, "sypos": int(data)}]

	elif int(field) == 2:
	    #update cpmin

	    try:
		int(data)
	    except ValueError:
		return [{"error": "WRONG_DATA_ERROR"}]

	    db.execute('UPDATE spaces SET cpmin=? WHERE sid=?',(int(data),int(sid)))
	    db.commit()
	    db.close()
	    return [{"error": "OK", "email": email, "sid": sid, "cpmin": int(data)}]

	elif int(field) == 3:
	    #update free

	    try:
		int(data)
	    except ValueError:
		return [{"error": "WRONG_DATA_ERROR"}]

	    if int(free) != 0 and int(free) != 1:
		return [{"error": "WRONG_DATA_ERROR"}]

	    db.execute('UPDATE spaces SET free=? WHERE sid=?',(int(data),int(sid)))
	    db.commit()
	    db.close()
	    return [{"error": "OK", "email": email, "sid": sid, "free": int(data)}]

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

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def api_sendconfmail(self,email):
	pass

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def api_bankverifycc(self,cc):
	pass

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def api_bankpayment(self,cc,valid):
	pass

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def api_confacc(self,email):
	db = sql.connect("database.db")

	tmp_member = db.execute('SELECT confirmed FROM members WHERE email=?',(email,)).fetchall()

	if len(tmp_member) == 0:
	    return [{"error": "EMAIL_NOT_REGISTERED_ERROR"}]
	elif len(tmp_member) > 1:
	    return [{"error": "EMAIL_DATABASE_ERROR"}]

	if tmp_member[0][0] == 1:
	    return [{"error": "ALREADY_CONFIRMED_ERROR"}]
	elif tmp_member[0][0] != 0:
	    return [{"error": "CONF_DATABASE_ERROR"}]

	db.execute('UPDATE members SET confirmed=? WHERE email=?',(1,email))
	db.commit()
	db.close()

    def randomxy(self):
        return (random.randint(1,1000),random.randint(1,1000))

config={
        '/': {
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './static'
        }
}
# uncomment to run locally
# import sys
# ip = "127.0.0.1"
# port = 8000
# if len(sys.argv) == 2:
#     ip = sys.argv[1]
# elif len(sys.argv) == 3:
#     ip = sys.argv[1]
#     port = int(sys.argv[2])
#
# cherrypy.config.update({'server.socket_host': ip,
#                         'server.socket_port': port,
#                        })
#
# cherrypy.quickstart(App(), "/",config)

# our WSGI application
wsgiapp = cherrypy.tree.mount(App())
# Disable the autoreload which won't play well
cherrypy.config.update({'engine.autoreload.on': False})
# let's not start the CherryPy HTTP server
cherrypy.server.unsubscribe()
# use CherryPy's signal handling
cherrypy.engine.signals.subscribe()
# Prevent CherryPy logs to be propagated
# to the Tornado logger
cherrypy.log.error_log.propagate = False
# Run the engine but don't block on it
cherrypy.engine.start()
