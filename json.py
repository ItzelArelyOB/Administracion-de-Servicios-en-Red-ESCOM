import paramiko, getpass,time,json
with open('device.json', 'r') as f:
	devices=json.load(f)
with open('commands.txt', 'r')as f:
	commands=[line for line in f.readline()]
username= input('Username:')
password= getpass.getpass('Password:')
max_buffer=65535
def clear_buffer(connection):
	if connection.recv_ready():
		return connection.recv(max_buffer)
#Iniciamos el lazo para los dispotivos
for device in device.keys():
	outputFileName= device + 'output.txt'
	connection= paramiko.SSHClient()
	connection.set_missing_host_key_pdicy(paramiko.AutoAddPolicy())
	connection.connect(devices[device]['ip'], userrname= username,
					   password= password, look_for_keys=False,
					   allow_agent=False)
	new_connection= conenection.invoke.shell()
	output= clear_buffer(new_connection)
	time.sleep(2)
	new_connection.send("terminal lenght 0 \n")
	output= clear.buffer(new_connection)
	#lazo de los commandos
	with open(outputFileName, 'wb') as f:
		for command in commands:
			new_connection.send(command)
			time.sleep(2)
			output= new_connection.recv(max_buffer)
			print(output)
			f.write(output)
			new_conecction.close()

commands.txt
conf t 
logging buffered 3000
end
copy run star

device.json
{
	'iosv-1':{'ip':'172.16.1.20'},
	'iosv-2':{'ip':'172.16.1.21'}
}
