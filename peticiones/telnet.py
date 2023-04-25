#*********************SE LLAMA A LOS ARCHIVOS/LIBRERÍAS REQUERIDAS***************
import librerias
import domainstatus
import os
import shutil
#**********************************************************************************

#*******************se declara el nombre del archivo a generar:*********************
filename = 'telnetlogs_DP_1.json'
filename2 = 'telnetlogs_DP_'
respuesta_final=[]
respuesta_final2=[]
#***********************************************************************************

#****************SE CALCULA EL TAMAÑO DE LOS DATAPOWER A EVALUAR:*******************************

#se asigna la url con base en el archivo librerías, que a su vez contiene información de la url a usar

#esta variable se usa para obtener la cantidad de servidores a iterar
total_targets = len(librerias.hosts.ipaddr)

#esta variable se usa para obtener la cantidad de elementos del body a iterar
total_bodies=len(librerias.hosts.body)

#*********************************************************************

#**********FUNCIÓN QUE LIMPIA LOS DIRECTORIOS, ESTO SE MODIFICA SEGÚN LOS REQURIMIENTOS*********
#se guarda la ruta del archivo y se le concatena el nombre del mismo


def valida_dir_file(filename,filename_final):
    #se guarda la ruta del archivo y se le concatena el nombre del mismo
    path_archivo_dp1 = librerias.os.path.join(librerias.telnetlogs, filename)
    path_archivo_dp2 = librerias.os.path.join(librerias.telnetlogs, filename_final)

    #se hace la comprobación para verificar si existe el archivo filename

    #se hace la comprobación para verificar si existe el archivo, si existe, lo elimina
    for file in [path_archivo_dp1, path_archivo_dp2]:
        if os.path.exists(file):
            os.remove(file)
    
    #copiamos el archivo a sus respectivo director
    shutil.copy(filename, librerias.telnetlogs)
    shutil.copy(filename_final, librerias.telnetlogs)
    
    #limpiamos el directorio peticiones
    for file in [filename, filename_final]:
        if os.path.exists(file):
            os.remove(file)

#*****************************************************************************************


#****************SE CALCULA EL TAMAÑO DE LOS DISPOSITIVOS:*******************************

#se asigna la url con base en el archivo librerías, que a su vez contiene información de la url a usar

#esta variable se usa para obtener la cantidad de servidores a iterar
total_targets = len(librerias.hosts.ipaddr)
#*********************************************************************

#********************SE SEJECUTA LA PETICIÓN***********************************************
#Obtenemos el contenido del response del script domainstatus.py
#comenzamos a iterar el total de datapower
for i in range(total_targets):
    #asignamos los cabeceros en función del elemento en iteración
    headers = librerias.cabeceros.headersprd[i]

    #con este ciclo, ingresamos al diccionario para leer el nombre de todos los dominios y luego 
    #irlos iterando uno a uno hasta recorrerlos todos.
    #esto sirve para hacer la invocación a cada url concatenando el dominio
    url =  librerias.hosts.ipaddr[i] + librerias.hosts.actionqueuedef

    #este ciclo define cuántos request enviaremos por datapower, en este caso, dependerá del número
    #de elementos que tenga el body
    for j in range(total_bodies):

        #evaluamos, para saber si es el primer request que estamos ejecutando
        if j==0:

            #si es así, asignamos el primer elemento del body encontrado
            body = librerias.hosts.body[0]
            
        else:

            #en caso contrario, asignamos el segundo
            body= librerias.hosts.body[1]
            
        #ejecutamos el request y guardamos la respuesta
        response = librerias.requests.post(url,headers=headers, verify=False, data=body)

        #cargamos el contenido del body en formato json
        parsed_body=librerias.json.loads(body)

        #generamos el nombre de archivo para cada datapower
        filename_final =f"{filename2}{i+1}.json"

        #guardamos el valor que se encuentre en remote host y remote port dentro de TCPConnectionTest
        remote_host = parsed_body['TCPConnectionTest']['RemoteHost']
        remote_port = parsed_body['TCPConnectionTest']['RemotePort']
        
        #se valida si la respuesta fue un http 200
        if response.status_code == 200:
            #generamos el mensaje que se modificará para dar visibilidad de la prueba que se hizo
            response_modificado = {"Origen" : "127.0.0.1", "Destino" : remote_host, "Puerto": remote_port, "Resultado:" : "La prueba se completo de manera exitosa"}  
             
            #esta condición permite identificar si es la primera ejecución, entonces corresponde al dp1
            if i==0:              
                
                #respuesta_final.append(response_modificado)   
                #se guarda el archivo completo en formato json con el sufijo del dp1 
                respuesta_final.append(response_modificado)   
                with open(filename, 'w') as f:
                   librerias.json.dump(respuesta_final,f)

            #en caso contrario, significa que no es el primer dp iterado
            else:

                respuesta_final2.append(response_modificado)           
                #se guarda el archivo completo en formato json con el sufijo del dp iterado
                with open(filename_final, 'w') as f:
                    librerias.json.dump(respuesta_final2,f)            

                
        else:
            #se obtiene el contenido de mensaje de error
            mensaje_error = response.json()['error']

            #generamos el mensaje que se modificará para dar visibilidad de la prueba que se hizo
            response_modificado = {"Origen" : librerias.hosts.ipaddr[i], "Destino" : remote_host, "Puerto": remote_port, "Resultado:" : "La prueba se completo de manera exitosa"} 
        
            #se guarda el archivo completo en formato json con el sufijo del dp iterado
            with open(filename_final, 'w') as f:
                librerias.json.dump(response_modificado, f)  

#con los archivos generados, se limipia el directorio y se mueve al respectivo
#es una función que se le pasan como parámetros los nombres de los archivos para validarlos
#si existen, los sobre escribe, si no, lo crea
valida_dir_file(filename, filename_final)  
#********************************FIN************************************************