# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 17:45:15 2024

@author: Emiliano
"""

import serial,time,collections
import matplotlib.pyplot as plt
import matplotlib.animation as anim
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from threading import Thread
from tkinter import Tk, Frame, StringVar, Label, Button, Entry
import numpy as np
import scipy.signal as signal

estaRecibiendo= False
estaEjecutandose = True
datos = [0]*8
arreglo = [0]*8
muestraD = 100

data1 = collections.deque([0]*muestraD, maxlen=muestraD)
data2 = collections.deque([0]*muestraD, maxlen=muestraD)
data3 = collections.deque([0]*muestraD, maxlen=muestraD)
data4 = collections.deque([0]*muestraD, maxlen=muestraD)
data5 = collections.deque([0]*muestraD, maxlen=muestraD)
data6 = collections.deque([0]*muestraD, maxlen=muestraD)
data7 = collections.deque([0]*muestraD, maxlen=muestraD)
data8 = collections.deque([0]*muestraD, maxlen=muestraD)
data_time = []

xmin = 0
xmax = muestraD
ymin = -5
ymax = 140

#Para el filtro
N_coef = 1024  #Propuesto por el doctor Aron Jazilevich
fc = 5.554*10**(-4)   #Propuesta por el doctor Aron Jazilevich
h = signal.firwin(N_coef, fc, window='hamming')    #Ventana hamming

# Filtro
buffer_size = N_coef
MinDatosFiltro = int(buffer_size/2)
vo = collections.deque([0]*(muestraD - MinDatosFiltro), maxlen=(MinDatosFiltro))
data_rest = collections.deque([0]*(muestraD - MinDatosFiltro), maxlen=(MinDatosFiltro))
contador = MinDatosFiltro
input_buffer = np.zeros(buffer_size)
def filtro_tiempo_real(nuevo_dato):
    input_buffer[:-1] = input_buffer[1:]
    input_buffer[-1] = nuevo_dato
    if (input_buffer[-MinDatosFiltro] != 0):
        output = np.convolve(input_buffer, h, mode='valid')
    else:
        output = [0]
    return output[-1]


#Comunicación con arduino
try:
    arduino = serial.Serial("COM5", 9600, timeout=1)

    def Salir():
        global estaEjecutandose
        estaEjecutandose = False
        if thread1.is_alive():
            thread1.join(timeout=0.8)
        if thread.is_alive():
            thread.join(timeout=0.8)
        arduino.close()
        time.sleep(1)
        raiz.destroy()
        raiz.quit()
        print("proceso finalizado")

    def Iniciar():
        global arreglo
        global datos
        global estaRecibiendo
        global estaEjecutandose
        estaEjecutandose = True
        estaRecibiendo = True
        animacion = anim.FuncAnimation(fig, plotData, fargs=(muestraD, MinDatosFiltro, contador, lines1, lines2, lines3, lines4, lines5, lines6, lines7, lines8), interval=1000, blit=False)
        plt.legend()
        plt.show()
        global thread
        thread = Thread(target=DatosA)
        thread.start()
        time.sleep(0.2)


    def DatosA():
        time.sleep(0.2)
        arduino.reset_input_buffer()
        while (estaEjecutandose):
            global estaRecibiendo
            global datos
            global arreglo
            global input_buffer
            try:
                datos = arduino.readline().decode('utf-8').strip()
                arreglo = list(map(float, datos.split()))
                print("Ejecutandose con normalidad")
                print(arreglo)
            except:
                time.sleep(0.2)
                Iniciar
                print("Reiniciando")

            time.sleep(0.2)
            estaRecibiendo = True

    def plotData(self,muestraD, MinDatosFiltro, contador1, lines1, lines2, lines3, lines4, lines5, lines6, lines7, lines8):
        #Guardado de datos leidos
        data1.append(arreglo[0])
        data2.append(arreglo[1])
        data3.append(arreglo[2])
        data4.append(arreglo[3])
        data5.append(arreglo[4])
        data6.append(arreglo[5])
        data7.append(arreglo[6])
        data8.append(arreglo[7])
        #print(data1)

        #Filtro
        #datoFiltrado = filtro_tiempo_real(datos)
        #contador1 = contador1 - 1
        #if (datoFiltrado == 0):
            #print("Cargando datos para el filtro...")
            #print("Faltan {} datos mas" .format(contador1))
        #else:
            #vo.append(datoFiltrado)

            # Resta de los datos
            #resta = data[-MinDatosFiltro] - datoFiltrado
            #data_rest.append(resta)

        lines1.set_data(range(muestraD), data1)
        lines2.set_data(range(muestraD), data2)
        lines3.set_data(range(muestraD), data3)
        lines4.set_data(range(muestraD), data4)
        lines5.set_data(range(muestraD), data5)
        lines6.set_data(range(muestraD), data6)
        lines7.set_data(range(muestraD), data7)
        lines8.set_data(range(muestraD), data8)
        #lines2.set_data(range((muestraD - MinDatosFiltro)), vo)
        #lines3.set_data(range((muestraD - MinDatosFiltro)), data_rest)
        mu = '\u03BC'
        labelx.set(str(datos) + " " + mu + "g/m^3")


    def Terminar():
        global estaEjecutandose
        global estaRecibiendo
        estaEjecutandose = False
        estaRecibiendo = False
        time.sleep(0.5)
        if thread.is_alive():
            thread.join(timeout=0.8)
        #thread1.join(timeout=0.8)
        #arduino.close()
        arreglo = [0.0]*8

    def limpiar():
        ax.clear()

    def TerminarGuardar():
        global estaGuardando
        estaGuardando = False
        time.sleep(0.5)
        if thread1.is_alive():
            thread1.join(timeout=0.8)

    # , figsize=(6, 5)   tamaño / , dpi=75  zoom / plt.cla()  borra  nombres x e y /
    fig = plt.figure(facecolor="0.55",figsize=(7.5, 5), clear=False, dpi=100)
    ax = plt.axes(xlim=(xmin,xmax),ylim=(ymin,ymax))
    plt.title("Gráfica detección partículas PM2.5", size=16, family="Tahoma")
    ax.set_xlabel("No. Medición")
    ax.set_ylabel("Concentración $\mu g/m^3$")
    lines1 = ax.plot([], [], 'b', label = "Señal sensor 1")[0]
    lines2 = ax.plot([], [], 'r', label = "Señal sensor 2")[0]
    lines3 = ax.plot([], [], '#5CFE05', label = "Señal sensor 3")[0]
    lines4 = ax.plot([], [], '#FD7E14', label="Señal sensor 4")[0]
    lines5 = ax.plot([], [], '#6F42C1', label="Señal sensor 5")[0]
    lines6 = ax.plot([], [], '#343A40', label="Señal sensor 6")[0]
    lines7 = ax.plot([], [], '#E83E8C', label="Señal sensor 7")[0]
    lines8 = ax.plot([], [], '#17A2B8', label="Señal sensor 8")[0]

    def Guardar():
        global estaGuardando
        estaGuardando = True
        fecha = time.strftime("%Y_%m_%d_hora_%H_%M_%S")
        nombre_archivo = f"C:\\Users\\Emiliano\\OneDrive\\Escritorio\\DatosSensor\\datosSensorPM2_5_{fecha}.txt"
        archivo = open(nombre_archivo, 'w')
        time.sleep(0.2)
        archivo.write("Tiempo" + "," + "Concentracion" + "\n")
        while (estaGuardando):
            time.sleep(1)
            archivo.write(str(round(time.time())) + "," + str(datos) + "\n")


    def GuardarBoton():
        global thread1
        thread1 = Thread(target=Guardar)
        thread1.start()
        print("Guardando datos")

    raiz = Tk()
    raiz.protocol("WM_DELETE_WINDOW", Salir)
    raiz.config(bg = "black")
    raiz.title("  \t\t\t\t GRÁFICA TIEMPO REAL SENSOR PM 2.5")
    raiz.geometry("1038x502")
    raiz.resizable(1,1)

    lienzo = FigureCanvasTkAgg(fig, master = raiz)
    lienzo._tkcanvas.grid(row = 0,column = 0, padx = 1,pady = 1)
    frame = Frame(raiz, width = 450,height = 502, bg = "#7003FC")
    frame.grid(row = 0,column = 1, padx = 1,pady = 2)
    frame.grid_propagate(False)
    frame.config(relief = "sunken")
    frame.config(cursor = "arrow")
    mu = '\u03BC'
    labelx = StringVar(raiz, "Concentración: 0.0 " + mu + "g/m^3")

    label = Label(frame,textvariable = labelx, bg= "#5CFE05",fg="black", font="Helvetica 13 bold",width=25, justify="center")
    label.grid(row=0,column=0, padx=40,ipady=8, pady=10)
    Iniciar = Button(frame,command= Iniciar, text= "Iniciar ",bg="blue",fg="white", font="Helvetica 14 bold",width=12,justify="center")
    Iniciar.grid(row=1,column=0, padx=40,pady=5)
    terminar = Button(frame,command= Terminar, text= "Terminar",bg="blue",fg="white", font="Helvetica 14 bold",width=12)
    terminar.grid(row=2,column=0, padx=40,pady=5)
    guardarb = Button(frame,command= GuardarBoton, text= "Guardar",bg="blue",fg="white", font="Helvetica 14 bold",width=12,justify="center")
    guardarb.grid(row=3,column=0, padx=5,pady=5)
    terminarguardarb = Button(frame,command= TerminarGuardar, text= "Term Guardar",bg="blue",fg="white", font="Helvetica 14 bold",width=12,justify="center")
    terminarguardarb.grid(row=4,column=0, padx=5,pady=5)
    #limpiarfig = Button(frame,command= limpiar, text= "Limpiar",bg="blue",fg="white", font="Helvetica 14 bold",width=12,justify="center")
    #limpiarfig.grid(row=5,column=0, padx=5,pady=5)
    salir = Button(frame,command= Salir, width=12 ,text= "SALIR",bg="red", font="Helvetica 14 bold",justify="center")
    salir.grid(row=6,column=0, padx=5,pady=45)
    raiz.mainloop()

except:
    print("Error de conexión con el puerto")
