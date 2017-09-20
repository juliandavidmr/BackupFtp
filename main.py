# -*- coding: utf-8 -*-
'''
 # Copyright 2014 Pablo Toledo.
 #
 # Licensed under the Apache License, Version 2.0 (the "License");
 # you may not use this file except in compliance with the License.
 # You may obtain a copy of the License at
 #
 #      http://www.apache.org/licenses/LICENSE-2.0
 #
 # Unless required by applicable law or agreed to in writing, software
 # distributed under the License is distributed on an "AS IS" BASIS,
 # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 # See the License for the specific language governing permissions and
 # limitations under the License.
 Autor inicial:
    @author: juanpablotoledogavagnin
 Mantenido por:
    juliandavidmr <https://github.com/juliandavidmr>
'''

from __future__ import with_statement
import os
from ftplib import FTP

# Var Globals configurations
HOST = 'localhost'
PORT = 54218
USER = 'GeekPrueba'
PASS = ''
ruta = "\\"
destino = os.getcwd() + "\\backup"
ftp = FTP()

# Vars globals logs
listErrors = []
numErrors = 0

def connect():
    ftp.connect(HOST, PORT)
    ftp.login(USER, PASS)
    print('Connected to server')
    print(str(ftp.welcome))
    return


def downloadRecursive(ruta):
    """
    Dowload files recursive
    """
    global numErrors
    # Nos movemos a la ruta en el servidor
    ftp.cwd(ruta)
    print 'En ruta:', ruta
    initialList = []
    ftp.dir(initialList.append)
    # print "Lista inicial:", initialList
    '''
    con dir() obtenemos un string que lista todos los elementos contenido en la ruta
    la estructura obtenida en mi caso fue
     
        drwxr-xr-x    2 362309906  usuario1       4096 Nov  2 15:09 .
        drwxr-x--x    4 362309906  usuario1       4096 Jun  9 08:26 ..
        -rw-r--r--    1 362309906  usuario1        563 Nov  1 17:10 index.html
         
    donde las carpetas comienzan con d y el nombre del archivo/carpeta se ubica al fin
    el string anterior se trata de la siguiente manera:
        -se divide el string en una lista de strings donde cada posicion representa una linea
        -cada posicion de la lista se subdivide tomando como referencia los espacios formando un 
        array bidimensional donde tenemos la informacion separada y podemos consultarla con mas facilidad
    En este caso el array bidimensional tiene en las posiciones:
        -nx0: la informacion relativa a si es un directorio (d) o un archivo (-) y sus pemisos
        -nx8: el nombre de fichero
    '''
    listaIntermedia = []
    for elemento in initialList:
        listaIntermedia.append(str(elemento).split())

    # print "Lista intermedia:", listaIntermedia
    '''
    Tras obtener en listaIntermedia el array bidimensional, generamos dos listas:
        -Una lista de pos[8] (nombres de ficheros) que cumplen que pos[0] no comienza con d
        -Una lista de pos[8] (carpetas) que cumplen que pos[0] comienza con d
    '''
    listFiles = []
    listFolders = []
    for elemento in listaIntermedia:
        name = b""
        for a in elemento[8:]:
            name += a + " "
        name = name.strip()
        if elemento[0].startswith('d'):
            # print "Carpeta: ", name
            listFolders.append(name)
        else:
            # print "File:", name.decode('utf-8')
            listFiles.append(name)
    '''
    Eliminamos de la lista de carpetas . y .. para evitar bucles por el servidor
    '''
    try:
        listFolders.remove('.')
        listFolders.remove('..')
    except:
        pass
    '''
    Listamos los elementos a trabajar de la ruta actual
    '''
    print('\tLista de Archivos: ' + str(listFiles))
    print('\tLista de Carpetas: ' + str(listFolders))

    '''
    Si la ruta actual no tiene su equivalente local, creamos la carpeta a nivel local
    '''
    if not os.path.exists(destino + ruta):
        os.makedirs(destino + ruta)
    '''
    Los elementos de la lista de archivo se proceden a descargar de forma secuencial en la ruta
    '''
    for elemento in listFiles:
        print('\tDescargando ' + elemento + ' en ' + destino + ruta)
        try:
            ftp.retrbinary(
                "RETR " + elemento, open(os.path.join(destino + ruta, elemento.decode('utf-8')), "wb").write)
        except:
            print('Error al descargar ' + elemento +
                  ' ubicado en ' + destino + ruta)
            listErrors.append('Archivo ' + elemento +
                                ' ubicado en ' + destino + ruta)
            numErrors += 1
    '''
    Una vez se termina de descargar los archivos invocamos el metodo actual provocando una solucion
    recursiva, para ello concatenamos la ruta actual con el nombre de la carpeta, realizando tantas
    llamadas al metodo actual como elementos tengamos listados en listFolders
    '''
    for elemento in listFolders:
        # elemento = elemento[2:len(elemento) - 2]
        downloadRecursive(ruta + elemento + "\\")
    return


# Main
print 'Comienza la ejecucion del backup de sitio web ', HOST
connect()
downloadRecursive(ruta)
