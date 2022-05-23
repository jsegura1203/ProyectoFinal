def normalizacion(var):
    import numpy as n

    archivo = open(var)
    contenido = archivo.readlines()

    lectura = []
    for i in contenido:
        lectura.append(i.split(","))
    encabezados = lectura[0]
    del lectura[0]

    instancia = [ list(map(float,x[:len(x)])) for x in lectura ]

    normalizacion = []

    instancia = n.array(instancia)

    for j in range(len(instancia[0]-3)):
        columna=[]
        min= n.min(instancia[:, j])
        max=n.max(instancia[:, j])
        for i in range (len(lectura)):
            columna.append(round((instancia[i][j]-min)/(max-min),3))
        normalizacion.append(columna)

    normalizacion = n.array(normalizacion)
    normalizacion= normalizacion.T

    complemento = []

    for i in range (len(lectura)):
        linea=[]
        for j in range (len(instancia[0])-3):
            linea.append(round(1-normalizacion[i][j],3))
        complemento.append(linea)

    salida = open("nuevo.csv","w")

    for i in range(len(normalizacion)):
        renglon=""
        for j in range(len(instancia[0])-1):
            if(j<2):
                renglon+=str(normalizacion[i][j])+","
            else:
                renglon+=str(instancia[i][j])+","
        renglon+=str(instancia[i][4])
        salida.write(renglon+"\n")

    salida.close()