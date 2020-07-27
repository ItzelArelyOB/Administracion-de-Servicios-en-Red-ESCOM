import paramiko,time,re,json
import netaddr
max_buffer = 65535
data={}
data['Router']=[]
consultadas=[]
def clear_buffer(connection):
 if connection.recv_ready():
 return connection.recv(max_buffer)
def connection_ssh(user,password,ip):
 connection = paramiko.SSHClient()
 connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
 connection.connect(ip, username=user, password=password,look_for_keys=False,allow_age
nt=False)
 new_connection=connection.invoke_shell()
 time.sleep(2)
 output=clear_buffer(new_connection)
 return new_connection
def StringIP4(ip):
 return str(netaddr.IPAddress(ip))
def Network(ip):
 ip_net=netaddr.IPNetwork(ip)
 return ip_net
def getIp(cadena):
 ip_route=re.findall("[0-9]{,3}\.[0-9]{,3}\.[0-9]{,3}\.[0-9]{,3}\/[0-9]{,2}",cadena)
 return ip_route
def send_Command(command,connection):
 connection.send(command)
 time.sleep(1)
 return clear_buffer(connection)
def Close_Connection(connection):
 connection.close()
def showVlan(id,connection):
 command='show int vlan '+str(id)+'\n'
 msg=send_Command(command,connection)
 ip_net=getIp(msg)
 net=Network(ip_net[0])
 command="show vlan-switch id "+str(id)+"\n"
 msg=send_Command(command,connection)
 print "--------------------------------------------------------------------"
 print msg[len(command):-4]
 print ("ID de red: "+ StringIP4(net.network))
 print ("Mascara: "+ StringIP4(net.netmask))
 print ("Gateway: "+ StringIP4(net.ip))
 print "--------------------------------------------------------------------"
def GetVlans(user,password,ip):
 connection=connection_ssh(user,password,ip)
 command='show vlan-switch | include Vlan\n'
 msg=send_Command(command,connection)
 vlans=re.findall("Vlan[0-9]{1,3}",msg)
 for vlan in vlans:
 showVlan(vlan.replace("Vlan",""),connection)
 Close_Connection(connection)
def Create_Vlan(user,password):
 id = int(input("Ingrese el id de la nueva Vlan\n"))
 name =raw_input("Ingrese el nombre de la nueva Vlan\n")
 ip_str=raw_input("Ingrese la ip con la mascara ejemplo:\n 192.168.0.1/24\n")
 ip=Network(ip_str)
 list_ips=list(ip)
 gateway=ip[1]
 print "La puerta de enlace de esta Vlan sera : "+ StringIP4(gateway)
 option=raw_input("Quiere Agregar una interfaz o interfaces?(si/no)\n")
 if("si"==option):
 interfaces=raw_input("Ingrese las infaces separadas por una coma\n").split(",")
 else:
 interfaces={}
 connection=connection_ssh(user,password,'192.168.1.11')
 send_Command("conf t\n",connection)
 send_Command("int vlan "+str(id)+"\n",connection)
 send_Command("ip add "+StringIP4(gateway)+" "+StringIP4(ip.netmask)+"\n",connection)
 send_Command("no sh \n",connection)
 send_Command("exit\n",connection)
 if ( len(interfaces) > 0 ):
 for interface in interfaces:
 send_Command("int "+interface+"\n",connection)
 send_Command("switchport mode trunk\n",connection)
 send_Command("switchport access vlan "+str(id)+"\n",connection)
 send_Command("exit\n",connection)
 send_Command("end\n",connection)
 send_Command("vlan database\n",connection)
 send_Command("vlan "+str(id)+" name "+name+"\n",connection)
 time.sleep(3)
 send_Command("exit\n",connection)
 Close_Connection(connection)
 print "switch 1"
 #################################################################
 connection=connection_ssh(user,password,'192.168.1.12')
 send_Command("conf t\n",connection)
 if ( len(interfaces) > 0 ):
 for interface in interfaces:
 send_Command("int "+interface+"\n",connection)
 send_Command("switchport mode trunk\n",connection)
 send_Command("switchport access vlan "+str(id)+"\n",connection)
 send_Command("exit\n",connection)
 send_Command("end\n",connection)
 send_Command("vlan database\n",connection)
 send_Command("vlan "+str(id)+" name "+name+"\n",connection)
 send_Command("apply\n",connection)
 send_Command("exit\n",connection)
 Close_Connection(connection)
 print "switch 2"
 ####################################################################
 connection=connection_ssh(user,password,'192.168.1.13')
 send_Command("conf t\n",connection)
 if ( len(interfaces) > 0 ):
 for interface in interfaces:
 send_Command("int "+interface+"\n",connection)
 send_Command("switchport mode trunk\n",connection)
 send_Command("switchport access vlan "+str(id)+"\n",connection)
 send_Command("exit\n",connection)
 send_Command("end\n",connection)
 send_Command("vlan database\n",connection)
 send_Command("vlan "+str(id)+" name "+name+"\n",connection)
 send_Command("apply\n",connection)
 send_Command("exit\n",connection)
 Close_Connection(connection)
 print "switch 3"
 #####################################################################
 connection=connection_ssh(user,password,'192.168.1.1')
 send_Command("conf t\n",connection)
 send_Command("int f0/0."+str(id)+"\n",connection)
 send_Command("encapsulation dot1Q "+str(id)+"\n",connection)
 send_Command("ip add "+StringIP4(gateway)+" "+StringIP4(ip.netmask)+"\n",connection)
 send_Command("end\n",connection)
 Close_Connection(connection)
 print "router"
def Delete(user,password):
 id=int(input("Ingrese el id de la Vlan que desee eliminar\n"))
 connection=connection_ssh(user,password,'192.168.1.11')
 command='show vlan-switch | include Vlan'+str(id)+'\n'
 msg=send_Command(command,connection)
 interfaces=re.findall("Fa[0-9]{1,3}/[0-9]{1,3}",msg)
 Close_Connection(connection)
 connection=connection_ssh(user,password,'192.168.1.1')
 send_Command("conf t\n",connection)
 send_Command("int f0/0."+str(id)+"\n",connection)
 send_Command("ip add\n",connection)
 send_Command("no encapsulation dot1Q "+str(id)+"\n",connection)
 send_Command("exit\n",connection)
 send_Command("no int f0/0."+str(id)+"\n",connection)
 send_Command("end\n",connection)
 Close_Connection(connection)
 #######################################################################
 connection=connection_ssh(user,password,'192.168.1.13')
 send_Command("conf t\n",connection)
 if ( len(interfaces) > 0 ):
 for interface in interfaces:
 send_Command("int "+interface+"\n",connection)
 send_Command("switchport access vlan 1\n",connection)
 send_Command("exit\n",connection)
 send_Command("end\n",connection)
 Close_Connection(connection)
 print "switch 3"
 ##########################################################################
 connection=connection_ssh(user,password,'192.168.1.12')
 send_Command("conf t\n",connection)
 if ( len(interfaces) > 0 ):
 for interface in interfaces:
 send_Command("int "+interface+"\n",connection)
 send_Command("switchport access vlan 1\n",connection)
 send_Command("exit\n",connection)
 send_Command("end\n",connection)
 Close_Connection(connection)
 ##########################################################################
 connection=connection_ssh(user,password,'192.168.1.11')
 send_Command("conf t\n",connection)
 if ( len(interfaces) > 0 ):
 for interface in interfaces:
 send_Command("int "+interface+"\n",connection)
 send_Command("switchport access vlan 1\n",connection)
 send_Command("exit\n",connection)
 send_Command("no int vlan "+str(id)+"\n",connection)
 send_Command("end\n",connection)
 send_Command("vlan database\n",connection)
 send_Command("no vlan "+str(id)+"\n",connection)
 send_Command("exit\n",connection)
 Close_Connection(connection)
while True:
 print "Escriba la opcion que desee realizar"
 print "1.Mostrar Vlans"
 print "2.Crear Vlan"
 print "3.Eliminar Vlan"
 print "4.Salir"
 opcion=int(input(""))
 if opcion==1:
 GetVlans('cisco','cisco','192.168.1.11')
 if opcion==2:
 Create_Vlan('cisco','cisco')
 if opcion==3:
 Delete('cisco','cisco')
 if opcion==4:
 break