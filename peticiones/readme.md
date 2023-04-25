
instalar python para windows 10 (en este caso)
abrir la terminal de bash para winows o powershell y ejecutar:
pip install requests
pip install urllib3
Instalar VS Code
Instalar la extensión para python
al ejecutar por primera vez, pedirá seleccionar el intérprete de python, seleccionarlo

modificar el archivo hosts para agregar los servidores dp a monitorear en el siguiente formato:
ipaddr=['https://ip-dp1:5554','https://ip-dp2:5554','https://ip-dp3:5554' ]

Editar el archivo cabeceros.py con el usuario en b64 de tus servidores, puede ser 1 o varios, en formato de lista:
para codificar, debe hacerse de la siguiente forma: 
usuario:password. 
Ejemplo: juan:h0l4!

En caso de que cada servidor requiera un usuario y pwd diferente, se pueden agregar en forma de lista:
[
    {"Authorization" : "Basic YWRtaW46MXFhejJ3c3g=", "Content-Type" : "application/json"},
    {"Authorization" : "Basic thaweenlwaekriwernn=", "Content-Type" : "application/json"},
    {"Authorization" : "Basic kldrabwenrlkwernllwk=", "Content-Type" : "application/json"},
    {"Authorization" : "Basic naeryoianaknwernwern=", "Content-Type" : "application/json"},
    {"Authorization" : "Basic lkwaenrnbernweiooiew=", "Content-Type" : "application/json"}

    ]

adicional, si se desean agregar los cabeceros de otros ambientes, entonces deberá agregarse una variable que contenga la misma estructura.
