#*********************SE LLAMA A LOS ARCHIVOS/LIBRERÍAS REQUERIDAS***************
import librerias
import os
import shutil
#**********************************************************************************

#*******************se declara el nombre del archivo a generar:*********************
filename = 'networkInterfaces_DP_1.json'
filename2 = 'networkInterfaces_DP_'
#***********************************************************************************

#****************SE CALCULA EL TAMAÑO DE LOS DATAPOWER A EVALUAR:*******************************

#se asigna la url con base en el archivo librerías, que a su vez contiene información de la url a usar

#esta variable se usa para obtener la cantidad de servidores a iterar
total_targets = len(librerias.hosts.ipaddr)

#*********************************************************************

#**********FUNCIÓN QUE LIMPIA LOS DIRECTORIOS, ESTO SE MODIFICA SEGÚN LOS REQURIMIENTOS*********
#se guarda la ruta del archivo y se le concatena el nombre del mismo


def valida_dir_file(filename,filename_final):
    #se guarda la ruta del archivo y se le concatena el nombre del mismo
    path_archivo_dp1 = librerias.os.path.join(librerias.default, filename)
    path_archivo_dp2 = librerias.os.path.join(librerias.default, filename_final)

    #se hace la comprobación para verificar si existe el archivo, si existe, lo elimina
    for file in [path_archivo_dp1, path_archivo_dp2]:
        if os.path.exists(file):
            os.remove(file)
    
    #copiamos el archivo a sus respectivo directorio
    shutil.copy(filename, librerias.default)
    shutil.copy(filename_final, librerias.default)

    #limpiamos el directorio peticiones
    for file in [filename, filename_final]:
        if os.path.exists(file):
            os.remove(file)

#*************************************************************************************

#********************SE SEJECUTA LA PETICIÓN***********************************************
#Obtenemos el contenido del response del script domainstatus.py
#comenzamos a iterar el total de datapower
for i in range(total_targets):
    #asignamos los cabeceros en función del elemento en iteración
    headers = librerias.cabeceros.headersprd[i]

    #con este ciclo, ingresamos al diccionario para leer el nombre de todos los dominios y luego 
    #irlos iterando uno a uno hasta recorrerlos todos.
    #esto sirve para hacer la invocación a cada url concatenando el dominio
    url = librerias.hosts.ipaddr[i] + librerias.hosts.defaultstat + 'NetworkInterfaceStatus'
    
    #ejecutamos el request y guardamos la respuesta
    response = librerias.requests.get(url,headers=headers, verify=False)
     
    #convertimos la respuesta en formato json
    parsed_response = response.json()['NetworkInterfaceStatus'] 
         

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
        
