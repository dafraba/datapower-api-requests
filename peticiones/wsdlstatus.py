#*********************SE LLAMA A LOS ARCHIVOS/LIBRERÍAS REQUERIDAS***************
import librerias
import domainstatus
#**********************************************************************************

#*******************se declara el nombre del archivo a generar:*********************
filename = 'wsdlstatus_DP1.json'
filename2 = 'wsdlstatus_DP'
respuesta_final =[]
respuesta_final2 = []
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
    path_archivo_dp1 = librerias.os.path.join(librerias.servicesdir, filename)
    path_archivo_dp2 = librerias.os.path.join(librerias.servicesdir, filename_final)
    #se hace la comprobación para verificar si existe el archivo filename
    if librerias.os.path.exists(path_archivo_dp1):
    
        #si el archivo existe, se elimina para sobrescribir
        librerias.os.remove(path_archivo_dp1)
        librerias.os.remove(path_archivo_dp2)

        #se mueve el archivo de la ruta actual a la ruta final
        librerias.shutil.move(filename, librerias.servicesdir)
        librerias.shutil.move(filename_final, librerias.servicesdir)

    else:
        #print("el archivo no existe dentro de la ruta indicada, generando archivo....")
        librerias.shutil.move(filename, librerias.servicesdir)
        librerias.shutil.move(filename_final, librerias.servicesdir)

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
    for diccionario in datos:

        #se guarda el nombre del dominio extraído del diccionario
        domainname=diccionario["Domain"]

        #se construye la url con base el archivo hosts para la ip,
        #se concatena la base de la uri para status
        #se concatena el nombre del dominio (obtenido de recorrer el diccionario con este ciclo for)
        #por último se concatena el resto de la uri
        url= librerias.hosts.ipaddr[i] + librerias.hosts.status + domainname + "/WSWSDLStatusSimpleIndex"
        #print(url)
        #ejecutamos el request y guardamos la respuesta
        response = librerias.requests.get(url,headers=headers, verify=False)
        
        parsed_response = response.json()
        
        #generamos el nombre de archivo para cada datapower
        filename_final =f"{filename2}{i+1}.json"

        #se valida si la respuesta fue un http 200
        if response.status_code == 200:   
            #esta condición permite identificar si es la primera ejecución, entonces corresponde al dp1
            if i==0:

                respuesta_final.append(parsed_response)
                #se guarda el archivo completo en formato json con el sufijo del dp1 
                with open(filename, 'w') as f:
                    librerias.json.dump(respuesta_final, f)          

            #en caso contrario, significa que no es el primer dp iterado
            else:
                
                respuesta_final2.append(parsed_response)
                #se guarda el archivo completo en formato json con el sufijo del dp iterado
                with open(filename_final, 'w') as f:
                    librerias.json.dump(respuesta_final2, f)                      
            
        else:
                print('Error en la solicitud', response.status_code)
                response.raise_for_status()

#con los archivos generados, se limipia el directorio y se mueve al respectivo
#es una función que se le pasan como parámetros los nombres de los archivos para validarlos
#si existen, los sobre escribe, si no, lo crea
valida_dir_file(filename, filename_final)  
        
         
#*********************************************************************************

