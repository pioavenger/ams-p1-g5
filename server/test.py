import os
import json
import sqlite3 as sql
import math
import random

def randomxy():
	return (random.randint(1,1000),random.randint(1,1000))

def inttest(str):
	try:
		int(str)
	except ValueError:
		return [{"error": "NOT_AN_INT_ERROR"}]

	return [{"error": "OK"}]


def test():
    	db = sql.connect('database.db')

    #tmp = db.execute('SELECT mname,carplate FROM members ORDER BY mname ASC').fetchall()

    #print(tmp)

    #tmp_json = {"error": "OK"}
    #sl_json = [] 

    #index = 0
    #for element in tmp:
    #    tmp_json[str(index)] = element
    #	 index += 1
    
    #tmp_json["n"] = index

    #sl_json.append(tmp_json)

    #print(sl_json)

    #v_list = []
    #v_list.append(tmp_json)

    #for element in tmp:
	#ap_json = { element[0]: element[1] }
	#v_list.append(ap_json)

    #print(v_list)

    #print(v_list[1][tmp[0][0]])

    #mxpos = db.execute('SELECT mxpos FROM members WHERE pmid=?',(1,)).fetchone()
    #mypos = db.execute('SELECT mypos FROM members WHERE pmid=?',(1,)).fetchone()

    #sxposs = db.execute('SELECT sxpos FROM spaces').fetchall()
    #syposs = db.execute('SELECT sypos FROM spaces').fetchall()

    #sids = db.execute('SELECT psid FROM spaces').fetchall()

    #distances = []

    #print("tester " + str(sxposs[0][0]))

    #index = 0
    #for space in sids:	    
	#tmp_dis = math.sqrt( (mxpos[0]-sxposs[index][0])*(mxpos[0]-sxposs[index][0]) + (mypos[0]-syposs[index][0])*(mypos[0]-syposs[index][0]) )
	#tmp_json = {"sid": sids[index][0], "distance": tmp_dis }
	#distances.append(tmp_json)
      #  index += 1

    #print(distances)

    #sorted_distances = sorted(distances, key=lambda k: k['distance']) 

    #print(sorted_distances)

	mxpos,mypos = db.execute('SELECT mxpos,mypos FROM members WHERE pmid=?',(1,)).fetchone()

	#tmp_mid = 1
	#recent_list = db.execute('SELECT sid FROM bookings WHERE terminated=? AND mid=?',(1,tmp_mid)).fetchall()

	#sl_json = [] 

	#for element in recent_list:
	#	sp_info = db.execute('SELECT sxpos,sypos,cpmin,rating FROM spaces WHERE psid=?',(element[0],)).fetchone()
#
	#	tmp_dis = math.sqrt( (mxpos-sp_info[0])*(mxpos-sp_info[0]) + (mypos-sp_info[1])*(mypos-sp_info[1]) )
#
	#	ap_json = {"sid": element[0], "rating": float(sp_info[3]), "cpmin": sp_info[2], "distance": tmp_dis}
	#	sl_json.append(ap_json)
	
	#sl_json.reverse()

	#print(sl_json)

	#sorted_list = db.execute('SELECT psid,sxpos,sypos,cpmin,rating FROM spaces ORDER BY cpmin ASC').fetchall()
	#tmp_json = {"error": "OK", "email": email}
	#sl_json = [] 

	#for element in sorted_list:
	#    tmp_dis = math.sqrt( (mxpos-element[1])*(mxpos-element[1]) + (mypos-element[2])*(mypos-element[2]) )
#
	#    ap_json = {"sid": element[0], "rating": float(element[4]), "cpmin": element[3], "distance": tmp_dis}
	#    sl_json.append(ap_json)

	#sl_json.append(tmp_json)
	
	#print(sl_json)

	#sp_list = db.execute('SELECT psid,sxpos,sypos,cpmin,rating FROM spaces').fetchall()

	#sl_json = []
	#tmp_json = {"error": "OK", "email": email}

	#for space in sp_list:
	 #   tmp_dis = math.sqrt( (mxpos-space[1])*(mxpos-space[1]) + (mypos-space[2])*(mypos-space[2]) )
#
	 #   ap_json = {"sid": space[0], "rating": float(space[4]), "cpmin": space[3], "distance": tmp_dis}
	 #   sl_json.append(ap_json)

	#sorted_distances = sorted(sl_json, key=lambda k: k['distance']) 
	#sorted_distances.append(tmp_json)

	#print(sorted_distances)

	#sp_info = db.execute('SELECT psid,sxpos,sypos,cpmin,rating FROM spaces').fetchall()		

	#tmp_json = {"error": "OK", "email": email}
        #sl_json = [] 

        #for space in sp_info:
	 #   tmp_dis = math.sqrt( (mxpos-space[1])*(mxpos-space[1]) + (mypos-space[2])*(mypos-space[2]) )
#
#	    ap_json = {"sid": space[0], "rating": float(space[4]), "cpmin": space[3], "distance": tmp_dis}
#	    sl_json.append(ap_json)
#
#	sorted_ratings = sorted(sl_json, key=lambda k: k['rating'])
#	sorted_ratings.reverse()
        #sorted_ratings.append(tmp_json)

 #       print(sorted_ratings)

	#emails = db.execute('SELECT email FROM members').fetchall()

	#for mail in emails:
	#	if mail[0] == "ac@hotmail.com":
	#		print("found")

	#print("done")

	#test_list = db.execute('SELECT * FROM members WHERE email=?',("test@hotmail.com",)).fetchall()

	#print(test_list)	
	#print(len(test_list))

	#mytmpx, mytmpy = randomxy()

	#print(mytmpx)
	#print(mytmpy)

	#print(mxpos)
	#print(mypos)	

	#testingl = db.execute('SELECT online FROM members WHERE pmid=?',(1,)).fetchall()
	#print(testingl[0])
	#print(testingl[0][0])

	#numb = 5
	#varb = 1
	#if int(varb):
	#	print(numb)
	#	print(int(numb))
	
	str1 = "5"
	str2 = "5.4"
	str3 = "4.5.4"
	str4 = "hi"

	print(inttest(str1))
	print(inttest(str2))
	print(inttest(str3))
	print(inttest(str4))

test()
