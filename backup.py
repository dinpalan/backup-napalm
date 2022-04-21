#!/usr/bin/python
try:
    import napalm, re, datetime, os
except:
    print("pip install napalm")

path = os.getcwd()

try:
	os.stat(path+'/backup_config')
except:
	os.mkdir(path+'/backup_config')

driver = napalm.get_network_driver('ios')

#Device list to backup configuration
device_list = ['192.168.10.101','192.168.10.102']

#username, password and secret key to login
user = 'admin'
passwd = 'cisco123'
optional_args={'secret': 'cisco123'}

def main():
    for ips in device_list:
            device = driver(hostname=ips, username=user, password=passwd, optional_args=optional_args)
            device.open()
            config = device.get_config(retrieve='running')
            facts = device.get_facts()
            run_conf = config['running']
            #remove lines with "Current Configuration", "Building configuration" & "end"
            run_config = re.sub(r'Building configuration.*|Current configuration.*|end','',run_conf)
            date = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
            hostname = facts['hostname']
            #create file with running config in backup_config folder
            file = open(path+'/backup_config/'+hostname+'_'+date+'_'+'running-config','w')
            file.write(run_config)
            file.close()
            device.close()
main()
