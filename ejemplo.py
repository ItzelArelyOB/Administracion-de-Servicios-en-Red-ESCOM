import pexpect
dispositivos={'iosv-1':{'promt':'iosv-1#','ip':'172.16.1.20'},
			  'iosv-2':{'promt':'iosv-2#', 'ip':'172.16.1.21'}}

usuario='cisco'
password='cisco'

for d in dispositivos.keys()
	d_prompt=dispositivos[d]['promt']
	hijo=pexpect.spawn('telnet'+devices[d]['ip'])
	hijo.expect('Username:')
	hijo.sendline(usuario)
	hijo.expect('Password:')
	hijo.sendline(password)
	hijo.expect(d_promt)
	hijo.sendline('show version| i V')
	hijo.expect('d_promt')
	print(hijo.before)
	hijo.sendline('exit')



codigo en python que me levante la sesión en ssh
	
