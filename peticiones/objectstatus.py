#*********************SE LLAMA A LOS ARCHIVOS/LIBRERÍAS REQUERIDAS***************
import librerias
import domainstatus
import os
import shutil
#**********************************************************************************

#*******************se declara el nombre del archivo a generar:*********************
filename = 'objectStatus_DP_1.json'
filename2 = 'objectStatus_DP_'
respuesta_final =[]
#***********************************************************************************

#****************SE CALCULA EL TAMAÑO DE LOS DATAPOWER A EVALUAR:*******************************

#se asigna la url con base en el archivo librerías, que a su vez contiene información de la url a usar

#esta variable se usa para obtener la cantidad de servidores a iterar
total_targets = len(librerias.hosts.ipaddr)

#esta variable guardará el nombre de los dominios que obtiene de la ejecución de domainstatus.py
datos = domainstatus.parsed_response

#*********************************************************************

#**********FUNCIÓN QUE LIMPIA LOS DIRECTORIOS, ESTO SE MODIFICA SEGÚN LOS REQURIMIENTOS*********
#se guarda la ruta del archivo y se le concatena el nombre del mismo


def valida_dir_file(filename,filename_final):
    #se guarda la ruta del archivo y se le concatena el nombre del mismo
    path_archivo_dp1 = librerias.os.path.join(librerias.objstatus, filename)
    path_archivo_dp2 = librerias.os.path.join(librerias.objstatus, filename_final)
    #se hace la comprobación para verificar si existe el archivo filename

    #se hace la comprobación para verificar si existe el archivo, si existe, lo elimina
    for file in [path_archivo_dp1, path_archivo_dp2]:
        if os.path.exists(file):
            os.remove(file)
    
    #copiamos el archivo a sus respectivo director
    shutil.copy(filename, librerias.objstatus)
    shutil.copy(filename_final, librerias.objstatus)
    
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
    for diccionario in datos:

        #se guarda el nombre del dominio extraído del diccionario
        domainname=diccionario["Domain"]

        #se construye la url con base el archivo hosts para la ip,
        #se concatena la base de la uri para status
        #se concatena el nombre del dominio (obtenido de recorrer el diccionario con este ciclo for)
        #por último se concatena el resto de la uri
        url= librerias.hosts.ipaddr[i] + librerias.hosts.status + domainname + "/ObjectStatus"
        
        #ejecutamos el request y guardamos la respuesta
        response = librerias.requests.get(url,headers=headers, verify=False)

        #convertimos el response en un objeto json
        parsed_response = response.json()['ObjectStatus'] 

        #generamos el nombre de archivo para cada datapower
        filename_final =f"{filename2}{i+1}.json"
      
        #se valida si la respuesta fue un http 200
        if response.status_code == 200:

            #esta condición permite identificar si es la primera ejecución, entonces corresponde al dp1
            if i==0:

                #se guarda el archivo completo en formato json con el sufijo del dp1 
                with open(filename, 'w') as f:
                    librerias.json.dump(parsed_response, f)          

            #en caso contrario, significa que no es el primer dp iterado
            else:
                
                #se guarda el archivo completo en formato json con el sufijo del dp iterado
                with open(filename_final, 'w') as f:
                    librerias.json.dump(parsed_response, f)                      
            
        else:
                print('Error en la solicitud', response.status_code)
                response.raise_for_status()

#con los archivos generados, se limipia el directorio y se mueve al respectivo
#es una función que se le pasan como parámetros los nombres de los archivos para validarlos
#si existen, los sobre escribe, si no, lo crea
valida_dir_file(filename, filename_final)      
         
#*********************************************************************************


