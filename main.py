# -*- coding: utf-8 -*-
'''
    @author: juanpablotoledogavagnin
    Maintained by:
        juliandavidmr <https://github.com/juliandavidmr>
'''
import os
from ftplib import FTP
import time
import git
from conf import config

ftp = FTP()

# Vars globals logs
listErrors = []
numErrors = 0
numFolders = 0
numFiles = 0
log = open(os.path.join(os.getcwd(), 'logFTP.log'), 'w')


def connect():
    ftp.connect(config.get("host"), config.get("port"))
    ftp.login(config.get("user"), config.get("pass"))
    print('Connected to server')
    print(str(ftp.welcome))
    return


def downloadRecursive(ruta):
    """
    Download files recursive
    """
    global numErrors, numFolders, numFiles
    global log
    # Nos movemos a la ruta en el servidor
    ftp.cwd(ruta)
    print 'Actual route:', ruta
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
            # print "Folder: ", name
            listFolders.append(name)
        else:
            # print "File:", name.decode('utf-8')
            listFiles.append(name)

    # Fill num files and folders
    numFiles += len(listFiles)
    numFolders += len(listFolders)

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
    # print('\tLista de Archivos: ' + str(listFiles))
    # print('\tLista de Carpetas: ' + str(listFolders))

    '''
    Si la ruta actual no tiene su equivalente local, creamos la carpeta a nivel local
    '''
    if not os.path.exists(config.get("dest") + ruta):
        os.makedirs(config.get("dest") + ruta)
    '''
    Los elementos de la lista de archivo se proceden a descargar de forma secuencial en la ruta
    '''
    for elemento in listFiles:
        print('\tDescargando ' + elemento + ' en ' + config.get("dest") + ruta)
        try:
            ftp.retrbinary(
                "RETR " + elemento, open(os.path.join(config.get("dest") + ruta, elemento.decode('utf-8')), "wb").write)
            # listFiles.remove(elemento)
        except:
            ex = 'Error al descargar ' + elemento + \
                ' ubicado en ' + config.get("dest") + ruta
            print ex
            listErrors.append('Archivo ' + elemento +
                              ' ubicado en ' + config.get("dest") + ruta)
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


def prepareLog():
    global numErrors, log, listErrors
    print 'Errors detected = ', str(numErrors)
    log.write('Errors detected = ' + str(numErrors))
    for el in listErrors:
        log.write(str(el))


# Main
print 'Run backup FTP', config.get("host")
connect()
downloadRecursive(config.get("route"))
prepareLog()

# Create commit & push
msgcommit = ", ".join([
    str(int(time.time())),
    str(numErrors) + " Errors",
    str(numFiles) + " Files",
    str(numFolders) + " Folders"])
print "[GIT]\tPrepare commit", msgcommit
git.commit(config.get("folderdest"), msgcommit)
