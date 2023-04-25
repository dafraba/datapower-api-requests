#***************************LIBRERÍAS/ARCHIVOS REQUERIDOS*************************************
#LIBRERÍAS
import pandas as pd #se usa para poder procesar texto
import numpy as np
import requests #se usa para enviar requests vía http
import urllib3 #se usa para el manejo de certificados
import base64 #se usa para el procesamiento en b64
import importlib #se usa para recargar el módulo
import json
import shutil
import os 

#ARCHIVOS NECESARIOS
import hosts
import cabeceros


#************************************************************************************


#****DESHABILITANDO EL SUSDO DE SSL/TLS (SOLO CUANDO HAY CERTIFIADOS AUTOFIRMADOS)*****
urllib3.disable_warnings()
#*************************************************************************************


#la función reload  permite aplicar los cambios efectuados en los scripts manados a llamar
#importlib.reload(hosts)
#importlib.reload(cabeceros)


#definición de los paths
ltdir="miscelaneos\logtargetstatus"
default = "miscelaneos\default"
logsdir= "miscelaneos\systemlogs"
servicesdir= "miscelaneos\domainservices"
telnetlogs="miscelaneos\logstcp"
objstatus = "miscelaneos\objectstatus"