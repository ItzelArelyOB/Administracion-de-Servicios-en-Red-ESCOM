import getpass
from pexpect import pxssh
device={'iosv-1':{'prompt':'iosv_1#','ip':'172.16.1.20'},
		'iosv-2':{'prompt':'iosv_2#','ip':'172.16.1.21'}}
commands=['term lenght 0', 'show version', 'show run']
username=input('Username:')
password= getpass.getpass('Password:')
#Iniciamos el lazo para los dispositivos
for devices in device.key():
	outputFileName= device + '_output.txt'
	device_prompt= devices[devices]['prompt']
	child= pxssh.pxssh()
	child.login(devices[device]['ip'], username.strip(), password.strip(),auto_prompt_reset=false)
	#Iniciamos el lazo para comandos y el archivo de salida
	with open(outputFileName,'wb')as f:
		for command in commands:
			child.sendline(command)
			child.expect(device_prompt)
			f.write(child.before)
	child.logout()