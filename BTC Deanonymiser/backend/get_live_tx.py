import time
import MySQLdb
import time
import MySQLdb
from distutils.util import strtobool
import commands
import os
import requests
import subprocess
import json
conn = MySQLdb.connect(host= "127.0.0.1",
				  user="root",
				  passwd="root",
				  db="ihlp",
				  port=3306)
x = conn.cursor()
'''
CREATE TABLE `get_tx_id` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tx_id` text ,
  `peer_id` text ,
  `block_id` text ,
  `priority` int(11) DEFAULT NULL,
  `tx_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
)
'''
def get_asn_info(peer_ip):
        asn_request="http://ip-api.com/json/"+peer_ip
        response = requests.get(asn_request)
        asn_data = json.loads(response.text)
        return asn_data


def get_previous_block():
	result = commands.getoutput("/home/hbp53/bitcoin-core/bin/./bitcoin-cli getblockchaininfo")
	bitcoin_net_info=json.loads(result)
	return bitcoin_net_info['blocks']
peer_list_dict={}

def get_peer_list_max_tx():
	conn = MySQLdb.connect(host= "127.0.0.1",
                                  user="root",
                                  passwd="root",
                                  db="ihlp",
                                  port=3306)
        x = conn.cursor()
	query="select * from live_tx;"
	x.execute(query)
	record = x.fetchall()
	count=len(record)
	count=len(record)
	print count
	limit=2000
	if count>limit:
		query='DELETE FROM live_tx ORDER BY tx_time ASC limit '+str(count-limit)
		x.execute(query)
		conn.commit()
		time.sleep(3)

#print peer_list_dict
def get_peer_list():
	#block_id=get_previous_block()
        result = commands.getoutput("/home/hbp53/bitcoin-core/bin/./bitcoin-cli getpeerinfo")
        peer_list=json.loads(result)
        for peer in peer_list:
                #print peer
		time.sleep(1)
                peer_ip=str(peer['addr']).split(":")[0]
		peer_id=peer['id']
                if peer_id not in peer_list_dict: #we can use ip but when that ip reconnects we need to consider that too.
                        #print asn_data['status']
			try:	
				asn_data=get_asn_info(peer_ip)
                        	if asn_data['status']=="success":
                                	peer_list_dict[peer_id]=peer
                                	local_add=str(peer['addrlocal']).split(":")[0]
                                	services=str(peer['services'])
	                                isconnected=strtobool(str(peer['inbound']))
        	                        subver=str(peer['subver'])
                	                pingtime=str(peer['pingtime'])
                        	        asn_data=get_asn_info(peer_ip)
                                	asn=asn_data['as'].split()[0]
					peer_city=str(asn_data['city'])
					peer_country=str(asn_data['country'])
					peer_isp=str(asn_data['isp'])
					peer_zip_code=str(asn_data['zip'])
					peer_org=str(asn_data['org'])
					peer_lat=str(asn_data['lat'])
					peer_lon=str(asn_data['lon'])
	                                print asn
        	                        peer_id=peer['id']
                	                x.execute("""INSERT INTO peer_list (peer_ip,local_add,services,isconnected,subver,pingtime,asn,peer_id,peer_city,peer_country,peer_isp,peer_zip_code,peer_org,peer_lat,peer_lon) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(peer_ip,local_add,services,isconnected,subver,pingtime,asn,peer_id,peer_city,peer_country,peer_isp,peer_zip_code,peer_org,peer_lat,peer_lon))
                        	        conn.commit()
			except Exception as e:
				print str(e)
        #print peer_list_dict

END_FLAG=1
def get_latest_peer():
	while END_FLAG:
		get_peer_list()
		time.sleep(60) 
#get_peer_list()
def follow(thefile):
	thefile.seek(0,2)
	while True:
		line = thefile.readline()
		if not line:
			time.sleep(0.1)
			continue
		yield line
def get_txid():
	logfile = open("/home/hbp53/.bitcoin/debug.log","r")
	output_file=open("output.log","a")
	dict1={}
	loglines = follow(logfile)
	TX_id1=""
	flag=1
	block_id=int(get_previous_block())+1
	#loglines=logfile.readlines()
	for line in loglines:
		try:
			if "AcceptToMemoryPool" in line:
				TX_id1=line.split("accepted")[1].split("(")[0].strip()
				peer_id=line.split("peer=")[1].split(":")[0]
				dict1[TX_id1]=1
				flag=-1
				print TX_id1
				output_file.write(line)
				#x.execute("""INSERT INTO get_tx_id VALUES (%s,%s)""",(188,90))
				x.execute("""INSERT INTO get_tx_id(tx_id,peer_id,block_id,priority) VALUES (%s,%s,%s,%s)""",(TX_id1,peer_id,str(block_id),dict1[TX_id1]))
        	                conn.commit()
				print "file written"
				#break
			elif "got inv" in line and dict1[line.split("tx")[1].split()[0]]:
				#print "finding "+ TX_id1
				TX_id1=line.split("tx")[1].split()[0]
				if TX_id1 in line:
					dict1[TX_id1]+=1
					output_file.write(line)
					print "written "+ TX_id1
					peer_id=line.split("peer=")[1].split(":")[0]
					x.execute("""INSERT INTO get_tx_id(tx_id,peer_id,block_id,priority) VALUES (%s,%s,%s,%s)""",(TX_id1,peer_id,str(block_id),dict1[TX_id1]))
					conn.commit()
			elif "Successfully reconstructed block" in line:
				END_FLAG=-1
				break
		except Exception as e:
			print str(e)
			output_file.write(str(e))
	return TX_id1
#output_file.write(line)
#TX_id=get_txid()
import threading
thread1 = threading.Thread(target=get_latest_peer, args=())
thread2 = threading.Thread(target=get_txid, args=())
#x.execute('update peer_list set peer_lat=%s,peer_lon=%s where peer_id=%s',(3.4,5.6,1))
#conn.commit()
#thread1.start()
#thread2.start()
#get_peer_list_db()
#print peer_list_dict
while(True):
	get_peer_list_max_tx()
	time.sleep(3)
#thread1.join()
#thread2.join()

