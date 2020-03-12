import tkinter as tk
from tkinter import ttk

from urllib.request import urlopen
from bs4 import BeautifulSoup

import mysql.connector as mysql

import pandas as pd

def analizar():
    operacion.execute(f"INSERT IGNORE INTO paginas values('{v_pag.get()}', 0)")
    conexion.commit()
    url=urlopen(str(v_pag.get()))
    i=1
    paux=v_pag.get()
    impri=tk.Tk()
    impri.title("A N A L S I S   D E   P A G I  N A S")
    impri.geometry('500x500')
    impri.configure(background='black')
    l_1=ttk.Label(impri, text="--> P A G I N A   I N I C I A L : "+v_pag.get()+"\n", background='black', foreground='gold')
    l_1.grid(column=0, row=0)
    bs=BeautifulSoup(url.read(), 'html.parser')
    con=0
    print("Nmero de paginas analizadas: \n")

    ana=False
    while(ana==False):
        i=i+1
        con+=1
        for enlaces in bs.find_all("a"):
            textimp="href: {}".format(enlaces.get("href"))
            paginax=str(enlaces.get("href"))
            if str(paginax)[:3]=="htt":
                operacion.execute(f"INSERT IGNORE INTO paginas values('{paginax}', 0)")
                conexion.commit()
                pipo=ttk.Label(impri, text=textimp, background='black', foreground='gold')
                pipo.grid(column=0, row=i, sticky=tk.W)
            i=i+1
        fis=ttk.Label(impri, text="\nFIN DE PAGINA: " +str(con) ,background='black', foreground='gold' )
        fis.grid(column=0, row=i)  
        operacion.execute(f"update paginas set ok=1 where pag='{paux}'")
        paux=""
        operacion.execute( "SELECT * FROM paginas" )
        for Pagina, Status in operacion.fetchall():
            if(Status==0):
                ana=False
                break
            else:
                ana=True    
        if ana==False:   
            paux=Pagina
            url = urlopen(paux)
            bs = BeautifulSoup(url.read(), 'html.parser')
        else:
            if i==20:
                ana=True

        print(con)



ven = tk.Tk()
ven.title("S C A N")
ven.geometry('450x100')
ven.configure(background='black')

conexion = mysql.connect( host='localhost', user= 'root', passwd='', db='scan' )
operacion = conexion.cursor()

l_pag = tk.Label(ven, text="Ingrese la dirección de la página: ", bg= 'black', fg='gold')
l_pag.place(x=10, y=10)
v_pag = tk.StringVar()
e_pag = tk.Entry(ven, width=20, textvariable= v_pag) 
e_pag.place(x=250, y=10)

b_pag = tk.Button(ven, text="Analizar", command=analizar)
b_pag.place(x=250, y= 40)





ven.mainloop()