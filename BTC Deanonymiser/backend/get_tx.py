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
def get_peer_list():
	#block_id=get_previous_block()
        result = commands.getoutput("/home/hbp53/bitcoin-core/bin/./bitcoin-cli getpeerinfo")
        peer_list=json.loads(result)
        for peer in peer_list:
                #print peer
		time.sleep(1)
                peer_ip=str(peer['addr']).split(":")[0]
                if peer_ip not in peer_list_dict:
                        asn_data=get_asn_info(peer_ip)
                        #print asn_data['status']
			try:
                        	if asn_data['status']=="success":
                                	peer_list_dict[peer_ip]=peer
                                	local_add=str(peer['addrlocal']).split(":")[0]
                                	services=str(peer['services'])
	                                isconnected=strtobool(str(peer['inbound']))
        	                        subver=str(peer['subver'])
                	                pingtime=str(peer['pingtime'])
                        	        asn_data=get_asn_info(peer_ip)
                                	asn=asn_data['as'].split()[0]
	                                print asn
        	                        peer_id=peer['id']
                	                x.execute("""INSERT INTO peer_list (peer_ip,local_add,services,isconnected,subver,pingtime,asn,peer_id) values (%s,%s,%s,%s,%s,%s,%s,%s)""",(peer_ip,local_add,services,isconnected,subver,pingtime,asn,peer_id))
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
#thread1 = threading.Thread(target=get_latest_peer, args=())
#thread2 = threading.Thread(target=get_txid, args=())
#thread1.start()
#thread2.start()

#thread1.join()
#thread2.join()
get_txid()
time.sleep(30)
get_txid()
time.sleep(30)
get_txid()
time.sleep(30)
get_txid()
time.sleep(30)
get_txid()
time.sleep(30)
get_txid()
time.sleep(30)
get_txid()
time.sleep(30)
get_txid()
time.sleep(30)
