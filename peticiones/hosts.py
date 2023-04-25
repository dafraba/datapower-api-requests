
#interfaz en prod
ipaddr = ["https://192.168.1.79:5554"]

#remote target para tcp-connections:
body=['{"TCPConnectionTest" : {"RemoteHost" : "192.168.1.79","RemotePort" : "9090"}}',
      '{"TCPConnectionTest" : {"RemoteHost" : "192.168.1.79","RemotePort" : "5550"}}']



#uri para obtener el default log
defaultlog = "/mgmt/filestore/default/logtemp/cli-log"
speicache = '/mgmt/filestore/default/logtemp/ad-desarrollo/SpeiCache.log'
checkerror = '/mgmt/filestore/default/logtemp/checkError.log'

#base de uri para obtener status en dominio default
defaultstat='/mgmt/status/default/'

#se estable la uri base para status, los dominios son asignados dinámicamente
status="/mgmt/status/"


#acciones
actionqueuedef = '/mgmt/actionqueue/default'
traceroute = '/mgmt/actionqueue/default/operations/TraceRoute'