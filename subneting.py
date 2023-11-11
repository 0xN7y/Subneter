import sys



try:
	q = sys.argv[1]
except:
	print("\n\tUsage: python3 subneting.py '140.178.43.240/27'\n")
	exit()


def ipformat(ip):
        try:
            if len(ip.split('.')) == 4:
                ind = ip.split('.')
                for i in ind:
                    if i.isnumeric():
                        pass
                    else:
                        return False
                return True
            else:
                return False
        except:
            return False



def format_(q):
	if '/' in q:
		cidr = q.split('/')[-1]
		ip = q.split('/')[0]
		if ipformat(ip):
			pass
		else:
			print("Invalid Format")
			exit()
		if int(cidr) >= 25 or int(cidr) <= 32:
			pass 
		else:
			print("Only work with range in /25 to /32")
			exit()
		# print(cidr)
	else:
		print("Invalid Format")
		exit()

format_(q)

# /32 to /25
groupsize_to_subnet = {
	128 : 128,
	64 : 192,
	32 : 224,
	16 : 240,
	8 : 248,
	4 : 252,
	2 : 254,
	1 : 255,

}

cidr_to_subnet  = { 
	'/25' : 128,
	'/26' : 192,
	'/27' : 224,
	'/28' : 240,
	'/29' : 248,
	'/30' : 252,
	'/31' : 254,
	'/32' : 255,
}






"""
Network ip : the first ip of subnetwork
broadcaset ip : the last ip of subnet

fist host ip : the ip next to network ip
last host ip : the ip before broadcast ip

number of ip addr : the total number of ip in each subnetwork
cidr / subnet : cidr -> subnet

"""


# q = '10.1.1.37/29'
# q = '10.2.2.199/26'
# q = '10.2.2.111/25'
# q = '10.2.2.20/30'
# q = '140.178.43.240/27'


print(f"\n \tSubneting {q}\n")

lastofsubnet = '/' +q.split('/')[-1]
ip = q.split('/')[0]
last_octate = ip.split('.')[-1]


subnet_mask = '255.255.255.' + str(cidr_to_subnet[lastofsubnet]) # subnetmask


lsubet = q.split('/')[-1]
groupsize = [i for i in groupsize_to_subnet if groupsize_to_subnet[i] == cidr_to_subnet[lastofsubnet]][0]






possible_value = []
possible_value_ip = []
rotate = False

# while i <= int(last_octate):
# 	i = i + groupsize
# 	print(i)

def checkif(by,until):
	st = 0
	last = []
	while st <= until:
		st = st + by
		last.append(st)
	# print(last)
	if last[-1] > 255:
		return True
	else:
		return False





def check255(ip):
	spip = ip.split('.')
	index_of255s = [spip.index(i) for i in spip if int(i) > 255]
	# print(index_of255s)
	if index_of255s:
		return index_of255s,True	
	else:
		return index_of255s,False


def fix255s(ip):
	ind,val = check255(ip)
	if val:
		spip = ip.split('.')
		for i in ind:
			overby = int(spip[i]) - 255	
			# print(f"{overby=}")		
			spip[i] = str(-1 + overby)
			spip[i-1] = str(int(spip[i-1])+1)
			ret = '.'.join(spip)
			return ret
			# print(spip)
	else:
		return ip







i = 0
i_first = 0

while i <= int(last_octate):
	if checkif(groupsize,int(last_octate)):
		if i > 255:
			# i = i + groupsize
			# print("255 rched st ifrom 0")
			pass
			
			# tr_octat = ip.split('.')[:-1]
		else:
			if i_first == 0:
				al = ip.split('.')[:-1]
				al.append(str(0))
				inc_ = '.'.join(al)
				possible_value_ip.append(inc_)
			i = i + groupsize
			al = ip.split('.')[:-1]
			al.append(str(i))
			inc_ = '.'.join(al)
			
			possible_value_ip.append(inc_)
			if i_first == 0:
				possible_value.append(0)
			possible_value.append(i)
	else:
		if i_first == 0:
			al = ip.split('.')[:-1]
			al.append(str(0))
			inc_ = '.'.join(al)
			possible_value_ip.append(inc_)
		i = i + groupsize
		al = ip.split('.')[:-1]
		al.append(str(i))
		inc_ = '.'.join(al)
		
		possible_value_ip.append(inc_)
		if i_first == 0:
			possible_value.append(0)
		possible_value.append(i)

	
	i_first = i_first + 1

# print(possible_value_ip)
# print(possible_value)
fixed_ip = []

for i in possible_value_ip:
	fixed_ip.append(fix255s(i))

# print(f"{fixed_ip=}")
possible_value_ip = fixed_ip


network_id = str(possible_value_ip[-2])
# network_id = fix255s(network_id)

next_network = str(possible_value_ip[-1])
# next_network = fix255s(next_network)


frist_host_ip = '.'.join(network_id.split('.')[:3])+'.'+str(int(network_id.split('.')[-1]) + 1) # add one network_id
# frist_host_ip = fix255s(frist_host_ip)
broadcast_ip = '.'.join(possible_value_ip[-1].split('.')[:3])+'.'+ str(int(str(possible_value[-1]).split('.')[-1])-1)
# broadcast_ip = fix255s(broadcast_ip)

last_host_ip = '.'.join(broadcast_ip.split('.')[:3])+'.'+str(int(broadcast_ip.split('.')[-1]) -1)
# last_host_ip = fix255s(broadcast_ip)

total_num_ofip = groupsize



print(f'Network ID : {network_id}')
print(f'Next Network :{next_network}')
print(f'Broadcast IP : {broadcast_ip}')
print(f'First IP : {frist_host_ip}')
print(f'Last IP : {last_host_ip}')
print(f'Total number of IP : {total_num_ofip}')
print(f'Total number of usable IP : {total_num_ofip -2}')
print(f'Subnetmask : {subnet_mask=}')
